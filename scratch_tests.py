from logic import (
    validate_tasks,
    filter_by_status,
    search_by_keywords,
    sort_tasks_by_title,
    get_final_value,
    next_id,
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
            {"id": 1, "title": "Buy milk", "status": "todo", "notes": "Check fridge"}
        ],
        "expected": True,
    },
    {
        "name": "not a list",
        "tasks": {
            "id": 1,
            "title": "Buy milk",
            "status": "todo",
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
        "tasks": [{"id": 1, "title": "Buy milk", "status": "todo"}],
        "expected": False,
    },
    {
        "name": "extra priority key",
        "tasks": [
            {
                "id": 1,
                "title": "Buy milk",
                "status": "todo",
                "notes": "Check fridge",
                "priority": "high",
            }
        ],
        "expected": False,
    },
    {
        "name": "id is bool",
        "tasks": [
            {"id": True, "title": "Buy milk", "status": "todo", "notes": "Check fridge"}
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
                "notes": "Check fridge",
            }
        ],
        "expected": True,
    },
]

print("Testing validate tasks\n")

for t in validate_cases:
    passed, message = check_result(t["name"], validate_tasks(t["tasks"]), t["expected"])
    print(message)
    if not passed:
        all_passed = False


tasks = [
    {
        "id": 1,
        "title": "Buy milk",
        "status": "todo",
        "notes": "Check fridge and bread",
    },
    {
        "id": 2,
        "title": "Email dentist",
        "status": "done",
        "notes": "Ask about June check-up",
    },
    {
        "id": 3,
        "title": "Book train tickets",
        "status": "in progress",
        "notes": "London trip with family",
    },
    {
        "id": 4,
        "title": "Fix bike brake",
        "status": "todo",
        "notes": "Rear brake rubbing slightly",
    },
    {
        "id": 5,
        "title": "Submit meter reading",
        "status": "done",
        "notes": "Electricity account",
    },
    {
        "id": 6,
        "title": "Plan coding session",
        "status": "in progress",
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
    result = filter_by_status(tasks, t["status"])
    returned_ids = [r["id"] for r in result]
    passed, message = check_result(t["name"], returned_ids, t["expected"])
    print(message)
    if not passed:
        all_passed = False

print("\nTesting sorting by title\n")

messy_sort_tasks = [
    {"id": 1, "title": "  banana", "status": "todo", "notes": ""},
    {"id": 2, "title": "Apple", "status": "todo", "notes": ""},
    {"id": 3, "title": "cherry", "status": "todo", "notes": ""},
    {"id": 4, "title": "  apricot", "status": "todo", "notes": ""},
]

expected_ids = [2, 4, 1, 3]
sorted_tasks = [t["id"] for t in sort_tasks_by_title(messy_sort_tasks)]
passed, message = check_result("Sorting by title", sorted_tasks, expected_ids)
print(message)
if not passed:
    all_passed = False

print("\nTesting search by keyword\n")

tasks = [
    {"id": 1, "title": "Buy milk", "status": "todo", "notes": "Check fridge and bread"},
    {
        "id": 2,
        "title": "Email dentist",
        "status": "done",
        "notes": "Ask about June check-up",
    },
    {
        "id": 3,
        "title": "Book train tickets",
        "status": "in progress",
        "notes": "London trip with family",
    },
    {
        "id": 4,
        "title": "Fix bike brake",
        "status": "todo",
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
    result = search_by_keywords(tasks, t["query"])
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

if all_passed:
    print("\nAll tests passed.")
else:
    print("One or more tests failed, check results.")
