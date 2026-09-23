from typing import Optional, TypedDict

from langgraph.graph import END, StateGraph

from app.rag.answer import answer_question
from app.router.classify import Route, classify
from app.sql_agent.agent import answer_sql_question


class ChatState(TypedDict, total=False):
    question: str
    route: Route
    rag_result: Optional[dict]
    sql_result: Optional[dict]
    answer: str
    sources: list[str]


def classify_node(state: ChatState) -> dict:
    return {"route": classify(state["question"])}


def rag_node(state: ChatState) -> dict:
    return {"rag_result": answer_question(state["question"])}


def sql_node(state: ChatState) -> dict:
    try:
        result = answer_sql_question(state["question"])
    except Exception as exc:
        result = {"answer": f"I couldn't answer that from the database: {exc}", "sql": None, "rows": []}
    return {"sql_result": result}


def finalize_node(state: ChatState) -> dict:
    rag_result = state.get("rag_result")
    sql_result = state.get("sql_result")

    if rag_result and sql_result:
        answer = f"{rag_result['answer']}\n\n{sql_result['answer']}"
        sources = rag_result["sources"]
    elif rag_result:
        answer = rag_result["answer"]
        sources = rag_result["sources"]
    elif sql_result:
        answer = sql_result["answer"]
        sources = []
    else:
        answer = "I couldn't process that question."
        sources = []

    return {"answer": answer, "sources": sources}


def _route_selector(state: ChatState) -> list[str]:
    route = state["route"]
    if route == "document":
        return ["rag_node"]
    if route == "sql":
        return ["sql_node"]
    return ["rag_node", "sql_node"]


def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("classify", classify_node)
    graph.add_node("rag_node", rag_node)
    graph.add_node("sql_node", sql_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("classify")
    graph.add_conditional_edges("classify", _route_selector, ["rag_node", "sql_node"])
    graph.add_edge("rag_node", "finalize")
    graph.add_edge("sql_node", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()


_compiled_graph = build_graph()


def route_question(question: str) -> dict:
    result = _compiled_graph.invoke({"question": question})
    return {"answer": result["answer"], "sources": result.get("sources", [])}
