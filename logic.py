REQUIRED_SCHEMA = {"id": int, "title": str, "status": str, "notes": str}
ALLOWED_STATUSES = {"todo", "in progress", "done"}


def normalize_status(value):
    return value.strip().lower()


def validate_tasks(tasks):
    if not isinstance(tasks, list):
        return False

    required_keys = set(REQUIRED_SCHEMA)

    for t in tasks:
        if not isinstance(t, dict):
            return False

        if set(t.keys()) != required_keys:
            return False

        for key, expected_type in REQUIRED_SCHEMA.items():
            # bool is a subclass of int, so guard id explicitly
            if key == "id" and isinstance(t["id"], bool):
                return False
            if not isinstance(t[key], expected_type):
                return False

        if normalize_status(t["status"]) not in ALLOWED_STATUSES:
            return False

    return True


def next_id(tasks):
    used = {t["id"] for t in tasks}
    candidate = 1
    while candidate in used:
        candidate += 1
    return candidate


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def add_task(tasks, title, status, notes):
    task = {
        "id": next_id(tasks),
        "title": title,
        "status": normalize_status(status),
        "notes": notes,
    }
    tasks.append(task)
    return task


def update_task(tasks, title, notes, task_num):
    task = find_task(tasks, task_num)
    if task is None:
        return None
    if title:
        task["title"] = title
    if notes:
        task["notes"] = notes
    return task


def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        return None
    tasks.remove(task)
    return task


def set_task_status(task, status):
    if task is None:
        return None
    status = normalize_status(status)
    if status not in ALLOWED_STATUSES:
        return None
    task["status"] = status
    return task


def sort_tasks_by_title(tasks):
    return sorted(tasks, key=lambda t: t["title"].lower().strip())


def search_by_keywords(tasks, query):
    query_lower = query.lower().strip()
    if not query_lower:
        return []
    return [
        t
        for t in tasks
        if query_lower in t["title"].lower() or query_lower in t["notes"].lower()
    ]


def get_final_value(old_val, new_val):
    stripped_val = new_val.strip()
    if stripped_val == "" or stripped_val == old_val:
        return "unchanged", old_val
    return "new_value", stripped_val


def filter_by_status(tasks, status):
    status = normalize_status(status)
    filtered = [t for t in tasks if t["status"] == status]
    return filtered


def validate_tasks(tasks):
    if not isinstance(tasks, list):
        return False

    required_keys = set(REQUIRED_SCHEMA)

    for t in tasks:
        if not isinstance(t, dict):
            return False

        if set(t.keys()) != required_keys:
            return False

        for key, expected_type in REQUIRED_SCHEMA.items():
            # bool is a subclass of int, so guard id explicitly
            if key == "id" and isinstance(t["id"], bool):
                return False
            if not isinstance(t[key], expected_type):
                return False

        if normalize_status(t["status"]) not in ALLOWED_STATUSES:
            return False

    return True
