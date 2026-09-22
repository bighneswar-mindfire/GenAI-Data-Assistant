from sqlalchemy import create_engine, inspect

from app.config import settings

engine = create_engine(settings.database_url)


def get_schema_description() -> str:
    inspector = inspect(engine)
    lines = []
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_list = ", ".join(f"{c['name']} {c['type']}" for c in columns)
        lines.append(f"{table_name}({column_list})")
    return "\n".join(lines)
