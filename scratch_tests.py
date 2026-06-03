from logic import (
    validate_tasks,
    filter_by_status,
    filter_by_priority_level,
    search_by_keywords,
    get_final_value,
    next_id,
    plan_update,
    sort_tasks,
)

all_passed = True


def check_result(name, result, expected):
    if result == expected:
        return True, f"Pass: {name}"
    else:
        return (
            False,
            f"Fail: {name}. Expected: {expected}, received: {result}.",
        )


validate_cases = [
    {
        "name": "valid task list",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "todo",
                "priority": "medium",
                "notes": "Check fridge",
            }
        ],
        "expected": True,
    },
    {
        "name": "not a list",
        "tasks": {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
            "priority": "medium",
            "notes": "Check fridge",
        },
        "expected": False,
    },
    {
        "name": "task is not a dict",
        "tasks": ["not a task dict"],
        "expected": False,
    },
    {
        "name": "missing notes key",
        "tasks": [
            {"id": 1, "title": "Buy milk", "priority": "medium", "status": "todo"}
        ],
        "expected": False,
    },
    {
        "name": "extra due date key",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "todo",
                "priority": "high",
                "notes": "Check fridge",
                "due date": "25.11.2026",
            }
        ],
        "expected": False,
    },
    {
        "name": "id is bool",
        "tasks": [
            {
                "id": True,
                "title": "Buy milk",
                "status": "todo",
                "priority": "high",
                "notes": "Check fridge",
            }
        ],
        "expected": False,
    },
    {
        "name": "status invalid",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "cancelled",
                "priority": "high",
                "notes": "Check fridge",
            }
        ],
        "expected": False,
    },
    {
        "name": "status has uppercase and spaces",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "  TODO  ",
                "priority": "high",
                "notes": "Check fridge",
            }
        ],
        "expected": False,
    },
    {
        "name": "invalid priority",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "todo",
                "priority": "urgent",
                "notes": "Check fridge",
            }
        ],
        "expected": False,
    },
    {
        "name": "mixed case priority level with spaces",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "todo",
                "priority": "    HiGh     ",
                "notes": "Check fridge",
            }
        ],
        "expected": False,
    },
    {
        "name": "missing priority key",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "todo",
                "notes": "Check fridge",
            }
        ],
        "expected": False,
    },
]

print("Testing validate tasks\n")

for t in validate_cases:
    passed, message = check_result(t["name"], validate_tasks(t["tasks"]), t["expected"])
    print(message)
    if not passed:
        all_passed = False


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

status_filter_cases = [
    {"name": "todo", "status": "todo", "expected": [1, 4]},
    {"name": "done", "status": "done", "expected": [2, 5]},
    {"name": "in progress", "status": "in progress", "expected": [3, 6]},
    {"name": "all caps", "status": "TODO", "expected": [1, 4]},
    {"name": "whitespace before/after", "status": "   done   ", "expected": [2, 5]},
    {"name": "not in schema", "status": "cancelled", "expected": []},
    {"name": "empty string", "status": "", "expected": []},
    {"name": "whitespace only", "status": "   ", "expected": []},
]

print("\nTesting filtering by status\n")

for t in status_filter_cases:
    result = filter_by_status(status_filter_tasks, t["status"])
    returned_ids = [r["id"] for r in result]
    passed, message = check_result(t["name"], returned_ids, t["expected"])
    print(message)
    if not passed:
        all_passed = False

print("\nTesting search by keyword\n")

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

search_cases = [
    {"name": "present in task 1", "query": "milk", "expected": [1]},
    {"name": "present in task 2", "query": "dentist", "expected": [2]},
    {"name": "present in task 3", "query": "london", "expected": [3]},
    {"name": "present in task 4", "query": "brake", "expected": [4]},
    {"name": "present in multiple tasks", "query": "check", "expected": [1, 2]},
    {"name": "empty string", "query": "", "expected": []},
    {"name": "whitespace string", "query": "   ", "expected": []},
    {"name": "not present", "query": "holiday", "expected": []},
    {"name": "present term, all caps", "query": "MILK", "expected": [1]},
]

for t in search_cases:
    result = search_by_keywords(keyword_search_tasks, t["query"])
    ids = [task["id"] for task in result]
    passed, message = check_result(t["name"], ids, t["expected"])
    print(message)
    if not passed:
        all_passed = False

print("\nTesting getting final value\n")

final_value_strings = [
    {
        "name": "Empty string",
        "old": "Buy milk",
        "new": "",
        "expected": ("unchanged", "Buy milk"),
    },
    {
        "name": "Whitespace string",
        "old": "Buy milk",
        "new": "   ",
        "expected": ("unchanged", "Buy milk"),
    },
    {
        "name": "Whitespace before",
        "old": "Buy milk",
        "new": "  Buy milk",
        "expected": ("unchanged", "Buy milk"),
    },
    {
        "name": "Different entry and leading/trailing whitespace",
        "old": "Buy milk",
        "new": "   Buy eggs   ",
        "expected": ("new_value", "Buy eggs"),
    },
]

for t in final_value_strings:
    result = get_final_value(t["old"], t["new"])
    print(result)
    passed, message = check_result(t["name"], result, t["expected"])
    print(message)
    if not passed:
        all_passed = False

print("\nTesting next id\n")

next_id_cases = [
    {"name": "empty task list", "tasks": [], "expected": 1},
    {"name": "one task id 1", "tasks": [{"id": 1}], "expected": 2},
    {"name": "ids 1 and 2", "tasks": [{"id": 1}, {"id": 2}], "expected": 3},
    {"name": "gap at 2", "tasks": [{"id": 1}, {"id": 3}], "expected": 2},
    {"name": "gap at 1", "tasks": [{"id": 2}, {"id": 3}], "expected": 1},
    {
        "name": "unordered ids, lowest missing id is 5",
        "tasks": [{"id": 2}, {"id": 3}, {"id": 1}, {"id": 4}, {"id": 7}, {"id": 6}],
        "expected": 5,
    },
]

for t in next_id_cases:
    result = next_id(t["tasks"])
    passed, message = check_result(t["name"], result, t["expected"])
    print(message)
    if not passed:
        all_passed = False

print("\nTesting filtering by priority level\n")

priority_filter_cases = [
    {"name": "low", "priority": "low", "expected": [3, 6]},
    {"name": "medium", "priority": "medium", "expected": [5]},
    {"name": "high", "priority": "high", "expected": [1, 2, 4]},
    {"name": "all caps", "priority": "LOW", "expected": [3, 6]},
    {"name": "whitespace before/after", "priority": "   medium   ", "expected": [5]},
    {"name": "not in schema", "priority": "urgent", "expected": []},
    {"name": "empty string", "priority": "", "expected": []},
    {"name": "whitespace only", "priority": "   ", "expected": []},
]

priority_filter_tasks = [
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

for t in priority_filter_cases:
    result = filter_by_priority_level(priority_filter_tasks, t["priority"])
    returned_ids = [r["id"] for r in result]
    passed, message = check_result(t["name"], returned_ids, t["expected"])
    print(message)
    if not passed:
        all_passed = False

print("\nTesting plan update flagging\n")

plan_update_cases = [
    {
        "name": "Both updated",
        "title_flag": "new_value",
        "notes_flag": "new_value",
        "expected": "both",
    },
    {
        "name": "Title updated",
        "title_flag": "new_value",
        "notes_flag": "unchanged",
        "expected": "title",
    },
    {
        "name": "Notes updated",
        "title_flag": "unchanged",
        "notes_flag": "new_value",
        "expected": "notes",
    },
    {
        "name": "No updates",
        "title_flag": "unchanged",
        "notes_flag": "unchanged",
        "expected": None,
    },
]

for t in plan_update_cases:
    result = plan_update(t["title_flag"], t["notes_flag"])
    passed, message = check_result(t["name"], result, t["expected"])
    print(message)
    if not passed:
        all_passed = False

print("\nTesting sorting by submenu behaviours\n")

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

print("\nTesting sorting by title\n")

expected_ids = [7, 10, 9, 5, 3, 4, 2, 1, 8, 6]
sorted_tasks = [t["id"] for t in sort_tasks(sort_submenu_tasks, "title")]
passed, message = check_result("Sorting by title", sorted_tasks, expected_ids)
print(message)
if not passed:
    all_passed = False

print("\nTesting sorting by status\n")

expected_ids = [7, 4, 8, 5, 10, 3, 6, 1, 2, 9]
sorted_tasks = [t["id"] for t in sort_tasks(sort_submenu_tasks, "status")]
passed, message = check_result("Sorting by status", sorted_tasks, expected_ids)
print(message)
if not passed:
    all_passed = False

print("\nTesting sorting by priority level\n")

expected_ids = [7, 8, 1, 5, 2, 4, 10, 3, 6, 9]
sorted_tasks = [t["id"] for t in sort_tasks(sort_submenu_tasks, "priority")]
passed, message = check_result("Sorting by priority", sorted_tasks, expected_ids)
print(message)
if not passed:
    all_passed = False

print("\nTesting invalid sort key\n")

expected = None
sorted_tasks = sort_tasks(sort_submenu_tasks, "due_date")
passed, message = check_result("Invalid sort key", sorted_tasks, expected)
print(message)
if not passed:
    all_passed = False

if all_passed:
    print("\nAll tests passed.")
else:
    print("One or more tests failed, check results.")
