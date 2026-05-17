from logic import get_final_value, plan_update, next_id, filter_by_status

status_filter_tasks = [
    {
        "id": 1,
        "title": "Buy milk",
        "status": "todo",
        "priority": "high",
        "notes": "Check fridge and bread",
    },
    {
        "id": 2,
        "title": "Email dentist",
        "status": "done",
        "priority": "high",
        "notes": "Ask about June check-up",
    },
    {
        "id": 3,
        "title": "Book train tickets",
        "status": "in progress",
        "priority": "high",
        "notes": "London trip with family",
    },
    {
        "id": 4,
        "title": "Fix bike brake",
        "status": "todo",
        "priority": "high",
        "notes": "Rear brake rubbing slightly",
    },
    {
        "id": 5,
        "title": "Submit meter reading",
        "status": "done",
        "priority": "high",
        "notes": "Electricity account",
    },
    {
        "id": 6,
        "title": "Plan coding session",
        "status": "in progress",
        "priority": "high",
        "notes": "Test filter_by_status",
    },
]


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


def test_empty_task_list_returns_1():
    result = next_id([])
    assert result == 1


def test_one_task_id_1_returns_2():
    result = next_id([{"id": 1}])
    assert result == 2


def test_ids_1_and_2_returns_3():
    result = next_id([{"id": 1}, {"id": 2}])
    assert result == 3


def test_gap_at_2_returns_2():
    result = next_id([{"id": 1}, {"id": 3}])
    assert result == 2


def test_missing_1_returns_1():
    result = next_id([{"id": 2}, {"id": 3}])
    assert result == 1


def test_unordered_ids_fills_correct_gap():
    result = next_id([{"id": 2}, {"id": 3}, {"id": 1}, {"id": 4}, {"id": 7}, {"id": 6}])
    assert result == 5


def test_filter_todo_tasks():
    result = [t["id"] for t in filter_by_status(status_filter_tasks, "todo")]
    assert result == [1, 4]


def test_filter_done_tasks():
    result = [t["id"] for t in filter_by_status(status_filter_tasks, "done")]
    assert result == [2, 5]


def test_filter_in_progress_tasks():
    result = [t["id"] for t in filter_by_status(status_filter_tasks, "in progress")]
    assert result == [3, 6]


def test_upper_case_input_works():
    result = [t["id"] for t in filter_by_status(status_filter_tasks, "TODO")]
    assert result == [1, 4]


def test_input_with_whitespace():
    result = [
        t["id"] for t in filter_by_status(status_filter_tasks, "    in progress   ")
    ]
    assert result == [3, 6]


def test_whitespace_only_returns_empty_list():
    result = [t["id"] for t in filter_by_status(status_filter_tasks, "       ")]
    assert result == []


def test_invalid_status_returns_empty_list():
    result = [t["id"] for t in filter_by_status(status_filter_tasks, "urgent")]
    assert result == []


def test_empty_string_returns_empty_list():
    result = [t["id"] for t in filter_by_status(status_filter_tasks, "")]
    assert result == []
