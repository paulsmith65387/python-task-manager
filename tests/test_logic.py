from logic import (
    get_final_value,
    plan_update,
    next_id,
    filter_by_status,
    filter_by_priority_level,
    sort_tasks,
    search_by_keywords,
    normalize_value,
    validate_tasks,
)


sort_submenu_tasks = [
    {
        "id": 1,
        "title": "Fix bike brake",
        "status": "done",
        "priority": "high",
        "notes": "Rear brake rubbing slightly",
    },
    {
        "id": 2,
        "title": "Email dentist",
        "status": "done",
        "priority": "medium",
        "notes": "Ask about check-up",
    },
    {
        "id": 3,
        "title": "Buy milk",
        "status": "in progress",
        "priority": "low",
        "notes": "Check fridge first",
    },
    {
        "id": 4,
        "title": "Clean desk",
        "status": "todo",
        "priority": "low",
        "notes": "Clear old papers",
    },
    {
        "id": 5,
        "title": "Book train tickets",
        "status": "in progress",
        "priority": "medium",
        "notes": "London trip",
    },
    {
        "id": 6,
        "title": "Update task manager README",
        "status": "in progress",
        "priority": "low",
        "notes": "Mention priority filtering",
    },
    {
        "id": 7,
        "title": "Apply chain lube",
        "status": "todo",
        "priority": "high",
        "notes": "Bike maintenance",
    },
    {
        "id": 8,
        "title": "Plan coding session",
        "status": "in progress",
        "priority": "high",
        "notes": "Work on sorting submenu",
    },
    {
        "id": 9,
        "title": "Apply chain lube",
        "status": "done",
        "priority": "low",
        "notes": "all weather",
    },
    {
        "id": 10,
        "title": "Apply chain lube",
        "status": "in progress",
        "priority": "low",
        "notes": "",
    },
]

filter_tasks = [
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
        "priority": "low",
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
        "priority": "medium",
        "notes": "Electricity account",
    },
    {
        "id": 6,
        "title": "Plan coding session",
        "status": "in progress",
        "priority": "low",
        "notes": "Test filter_by_status",
    },
]


keyword_search_tasks = [
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


def task_ids(task_list):
    return [t["id"] for t in task_list]


def test_filter_todo_tasks():
    result = filter_by_status(filter_tasks, "todo")
    assert task_ids(result) == [1, 4]


def test_filter_done_tasks():
    result = filter_by_status(filter_tasks, "done")
    assert task_ids(result) == [2, 5]


def test_filter_in_progress_tasks():
    result = filter_by_status(filter_tasks, "in progress")
    assert task_ids(result) == [3, 6]


def test_upper_case_input_works():
    result = filter_by_status(filter_tasks, "TODO")
    assert task_ids(result) == [1, 4]


def test_input_with_whitespace():
    result = filter_by_status(filter_tasks, "    in progress   ")
    assert task_ids(result) == [3, 6]


def test_whitespace_only_status_returns_empty_list():
    result = filter_by_status(filter_tasks, "       ")
    assert task_ids(result) == []


def test_invalid_status_returns_empty_list():
    result = filter_by_status(filter_tasks, "urgent")
    assert task_ids(result) == []


def test_empty_status_returns_empty_list():
    result = filter_by_status(filter_tasks, "")
    assert task_ids(result) == []


def test_filter_low_priority_tasks():
    result = filter_by_priority_level(filter_tasks, "low")
    assert task_ids(result) == [3, 6]


def test_filter_medium_priority_tasks():
    result = filter_by_priority_level(filter_tasks, "medium")
    assert task_ids(result) == [5]


def test_filter_high_priority_tasks():
    result = filter_by_priority_level(filter_tasks, "high")
    assert task_ids(result) == [1, 2, 4]


def test_upper_case_priority_works():
    result = filter_by_priority_level(filter_tasks, "LOW")
    assert task_ids(result) == [3, 6]


def test_input_priority_with_whitespace():
    result = filter_by_priority_level(filter_tasks, "    medium   ")
    assert task_ids(result) == [5]


def test_whitespace_only_priority_returns_empty_list():
    result = filter_by_priority_level(filter_tasks, "       ")
    assert task_ids(result) == []


def test_invalid_priority_returns_empty_list():
    result = filter_by_priority_level(filter_tasks, "high priority")
    assert task_ids(result) == []


def test_empty_string_priority_returns_empty_list():
    result = filter_by_priority_level(filter_tasks, "")
    assert task_ids(result) == []


def test_sorting_by_title():
    result = sort_tasks(sort_submenu_tasks, "title")
    assert task_ids(result) == [7, 10, 9, 5, 3, 4, 2, 1, 8, 6]


def test_sorting_by_status():
    result = sort_tasks(sort_submenu_tasks, "status")
    assert task_ids(result) == [7, 4, 8, 5, 10, 3, 6, 1, 2, 9]


def test_sorting_by_priority():
    result = sort_tasks(sort_submenu_tasks, "priority")
    assert task_ids(result) == [7, 8, 1, 5, 2, 4, 10, 3, 6, 9]


def test_sorting_by_invalid_sort_key_returns_none():
    result = sort_tasks(sort_submenu_tasks, "due date")
    assert result is None


def test_search_finds_keyword_in_title():
    result = search_by_keywords(keyword_search_tasks, "milk")
    assert task_ids(result) == [1]


def test_search_finds_keyword_in_notes():
    result = search_by_keywords(keyword_search_tasks, "rubbing")
    assert task_ids(result) == [4]


def test_search_finds_multiple_matches():
    result = search_by_keywords(keyword_search_tasks, "check")
    assert task_ids(result) == [1, 2]


def test_empty_search_query_returns_empty_list():
    result = search_by_keywords(keyword_search_tasks, "")
    assert task_ids(result) == []


def test_whitespace_search_query_returns_empty_list():
    result = search_by_keywords(keyword_search_tasks, "     ")
    assert task_ids(result) == []


def test_result_not_present_returns_empty_list():
    result = search_by_keywords(keyword_search_tasks, "holiday")
    assert task_ids(result) == []


def test_search_is_case_insensitive():
    result = search_by_keywords(keyword_search_tasks, "MILK")
    assert task_ids(result) == [1]


def test_normalize_leading_caps():
    result = normalize_value("Title")
    assert result == "title"


def test_normalize_all_caps():
    result = normalize_value("TITLE")
    assert result == "title"


def test_normalize_upper_lower_mixture():
    result = normalize_value("TiTlE")
    assert result == "title"


def test_normalize_string_with_whitespace():
    result = normalize_value("    title     ")
    assert result == "title"


def test_normalize_whitespace_only_returns_empty_string():
    result = normalize_value("       ")
    assert result == ""


def test_validate_tasks_accepts_valid_task_list():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is True


def test_validate_tasks_rejects_non_list_input():
    tasks = {
        "id": 1,
        "title": "Buy milk",
        "status": "todo",
        "priority": "medium",
        "notes": "Check fridge",
    }
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_missing_required_key():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_task_that_is_not_dict():
    tasks = ["Buy milk", "still to do", "High priority", "check fridge first"]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_extra_key():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
            "sub-category": "shopping"
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_invalid_status():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "started",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_invalid_priority():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
            "priority": "important",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_accepts_normalized_status_and_priority():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "       ToDo       ",
            "priority": "    hIgH    ",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is True


def test_validate_tasks_rejects_bool_id():
    tasks = [
        {
            "id": True,
            "title": "Buy milk",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_wrong_field_type():
    tasks = [
        {
            "id": 1,
            "title": 123,
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False