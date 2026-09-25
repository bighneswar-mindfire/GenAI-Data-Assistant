import pytest

from app.sql_agent.validate import validate_select_only


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT * FROM customers",
        "select * from customers;",
        "WITH t AS (SELECT * FROM orders) SELECT * FROM t",
    ],
)
def test_allows_select_statements(sql):
    assert validate_select_only(sql)


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE customers",
        "DELETE FROM orders WHERE id = 1",
        "UPDATE customers SET name = 'x'",
        "INSERT INTO customers (name) VALUES ('x')",
        "TRUNCATE orders",
        "ALTER TABLE customers ADD COLUMN x TEXT",
    ],
)
def test_blocks_non_select_statements(sql):
    with pytest.raises(ValueError):
        validate_select_only(sql)


def test_blocks_stacked_statements():
    with pytest.raises(ValueError):
        validate_select_only("SELECT * FROM customers; DROP TABLE customers;")


def test_blocks_empty_query():
    with pytest.raises(ValueError):
        validate_select_only("   ")
