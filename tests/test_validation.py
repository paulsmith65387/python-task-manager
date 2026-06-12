from logic import validate_tasks, normalize_value


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


def test_validate_tasks_rejects_normalized_status_and_priority():
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
    assert result is False


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


def test_validate_tasks_rejects_non_string_status():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": None,
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_non_string_priority():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
            "priority": 54321,
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_non_string_notes():
    tasks = [
        {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
            "priority": "medium",
            "notes": True,
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_non_integer_id():
    tasks = [
        {
            "id": "1",
            "title": "Buy milk",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_empty_title_string():
    tasks = [
        {
            "id": 1,
            "title": "",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_rejects_whitespace_only_title():
    tasks = [
        {
            "id": 1,
            "title": "       ",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is False


def test_validate_tasks_accepts_title_with_surrounding_whitespace():
    tasks = [
        {
            "id": 1,
            "title": "   Buy milk     ",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        }
    ]
    result = validate_tasks(tasks)
    assert result is True