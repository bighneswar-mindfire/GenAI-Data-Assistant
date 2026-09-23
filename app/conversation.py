MAX_HISTORY_TURNS = 6

_conversations: dict[str, list[dict]] = {}


def get_history(session_id: str) -> list[dict]:
    return _conversations.get(session_id, [])


def append_turn(session_id: str, role: str, content: str) -> None:
    history = _conversations.setdefault(session_id, [])
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY_TURNS * 2:
        del history[: len(history) - MAX_HISTORY_TURNS * 2]
