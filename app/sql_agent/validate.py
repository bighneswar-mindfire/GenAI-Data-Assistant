import re

FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter", "create", "truncate",
    "grant", "revoke", "copy", "attach", "detach", "vacuum", "call", "do",
}


def validate_select_only(sql: str) -> str:
    cleaned = sql.strip().rstrip(";").strip()
    if not cleaned:
        raise ValueError("Empty SQL query")
    if ";" in cleaned:
        raise ValueError("Multiple statements are not allowed")

    leading_word_match = re.match(r"^\s*(\w+)", cleaned)
    leading_word = leading_word_match.group(1).lower() if leading_word_match else ""
    if leading_word not in ("select", "with"):
        raise ValueError("Only SELECT statements are allowed")

    tokens = set(re.findall(r"[a-zA-Z_]+", cleaned.lower()))
    forbidden = tokens & FORBIDDEN_KEYWORDS
    if forbidden:
        raise ValueError(f"Query contains forbidden keyword(s): {', '.join(sorted(forbidden))}")

    return cleaned
