"""Tests for ff_ai_assistant.database."""

import pytest

from ff_ai_assistant.database import (
    execute_query,
    format_results,
    get_schema,
    validate_sql,
)


def test_execute_query_rejects_non_select():
    with pytest.raises(ValueError):
        execute_query("DROP TABLE player_seasons")


def test_execute_query_rejects_insert():
    with pytest.raises(ValueError):
        execute_query("INSERT INTO player_seasons VALUES (1)")


def test_format_results_empty_list():
    assert format_results([]) == "(No results)"


def test_format_results_single_row():
    rows = [{"player": "CMC", "points": 312.4}]
    result = format_results(rows)
    assert "CMC" in result
    assert "312.4" in result


def test_validate_sql_rejects_read_csv_auto():
    with pytest.raises(ValueError):
        validate_sql("SELECT * FROM read_csv_auto('/etc/passwd')")


def test_validate_sql_rejects_multi_statement():
    with pytest.raises(ValueError):
        validate_sql("SELECT 1; DROP TABLE player_seasons")


def test_validate_sql_rejects_non_whitelisted_table():
    with pytest.raises(ValueError):
        validate_sql("SELECT * FROM secret_table")


def test_validate_sql_rejects_non_select_root():
    with pytest.raises(ValueError):
        validate_sql("DROP TABLE player_seasons")


def test_validate_sql_valid_query():
    validate_sql("SELECT player_name FROM player_seasons")


@pytest.mark.skip(
    reason="requires processed parquets — regenerate with scripts/process_stats.py first"
)
def test_get_schema_contains_table_names():
    schema = get_schema()
    assert "player_seasons" in schema
    assert "weekly_stats" in schema
