from sqlalchemy import create_engine, inspect

from app.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 5},
)


def get_schema_description() -> str:
    inspector = inspect(engine)
    lines = []
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_list = ", ".join(f"{c['name']} {c['type']}" for c in columns)
        lines.append(f"{table_name}({column_list})")

        for constraint in inspector.get_check_constraints(table_name):
            lines.append(f"  CHECK on {table_name}: {constraint['sqltext']}")

    return "\n".join(lines)
