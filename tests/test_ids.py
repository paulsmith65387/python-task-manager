from logic import next_id


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