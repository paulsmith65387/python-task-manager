from logic import get_final_value, plan_update


def test_blank_input_keeps_old_value():
    result = get_final_value("buy milk", "")
    assert result == ("unchanged", "buy milk")


def test_whitespace_string_keeps_old_value():
    result = get_final_value("buy milk", "    ")
    assert result == ("unchanged", "buy milk")


def test_leading_whitespace_keeps_old_value():
    result = get_final_value("buy milk", "   buy milk")
    assert result == ("unchanged", "buy milk")


def test_new_entry_with_whitespace_gives_normalized_new_value():
    result = get_final_value("buy milk", "   buy eggs    ")
    assert result == ("new_value", "buy eggs")


def test_both_new_values_returns_both():
    result = plan_update("new_value", "new_value")
    assert result == "both"


def test_new_notes_value_returns_notes():
    result = plan_update("unchanged", "new_value")
    assert result == "notes"


def test_new_title_value_returns_title():
    result = plan_update("new_value", "unchanged")
    assert result == "title"


def test_no_changes_returns_none():
    result = plan_update("unchanged", "unchanged")
    assert result is None
