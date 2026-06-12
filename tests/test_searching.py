from logic import search_by_keywords


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


def task_ids(task_list):
    return [t["id"] for t in task_list]

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