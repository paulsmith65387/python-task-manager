REQUIRED_SCHEMA = {
    "id": int,
    "title": str,
    "status": str,
    "priority": str,
    "notes": str,
}

ALLOWED_STATUSES = {"todo", "in progress", "done"}
ALLOWED_PRIORITY_LEVELS = {"low", "medium", "high"}


def normalize_value(value):
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

        if t["status"] not in ALLOWED_STATUSES:
            return False
        if t["priority"] not in ALLOWED_PRIORITY_LEVELS:
            return False
        if t["title"].strip() == "":
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


def add_task(tasks, title, status, priority, notes):
    task = {
        "id": next_id(tasks),
        "title": title,
        "status": normalize_value(status),
        "priority": normalize_value(priority),
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
    status = normalize_value(status)
    if status not in ALLOWED_STATUSES:
        return None
    task["status"] = status
    return task


def set_task_priority(task, priority):
    if task is None:
        return None
    priority = normalize_value(priority)
    if priority not in ALLOWED_PRIORITY_LEVELS:
        return None
    task["priority"] = priority
    return task


def sort_tasks(tasks, field_choice):
    sort_keys = {"status", "priority", "title"}
    priority_ranks = {"low": 3, "medium": 2, "high": 1}
    status_ranks = {"done": 3, "in progress": 2, "todo": 1}
    if field_choice not in sort_keys:
        return None
    if field_choice == "title":
        return sorted(
            tasks,
            key=lambda t: (
                t["title"].lower().strip(),
                status_ranks[t["status"]],
                priority_ranks[t["priority"]],
            ),
        )
    elif field_choice == "status":
        return sorted(
            tasks,
            key=lambda t: (
                status_ranks[t["status"]],
                priority_ranks[t["priority"]],
                t["title"].lower().strip(),
            ),
        )
    elif field_choice == "priority":
        return sorted(
            tasks,
            key=lambda t: (
                priority_ranks[t["priority"]],
                status_ranks[t["status"]],
                t["title"].lower().strip(),
            ),
        )


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
    status = normalize_value(status)
    filtered = [t for t in tasks if t["status"] == status]
    return filtered


def filter_by_priority_level(tasks, priority):
    priority = normalize_value(priority)
    filtered = [t for t in tasks if t["priority"] == priority]
    return filtered


def plan_update(title_flag, notes_flag):
    update_flag = None
    if title_flag == "new_value" and notes_flag == "new_value":
        update_flag = "both"
    elif title_flag == "new_value" and notes_flag == "unchanged":
        update_flag = "title"
    elif title_flag == "unchanged" and notes_flag == "new_value":
        update_flag = "notes"
    return update_flag
