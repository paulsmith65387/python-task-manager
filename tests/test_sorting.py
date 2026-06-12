from logic import sort_tasks


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


def task_ids(task_list):
    return [t["id"] for t in task_list]


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