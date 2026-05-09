from logic import normalize_value, ALLOWED_STATUSES, ALLOWED_PRIORITY_LEVELS


def print_menu():
    print("\nTask Manager version 1.0")
    print("_________________________")
    print("Select an option:")
    print("1 : Add a task")
    print("2 : View a task")
    print("3 : Update a task")
    print("4 : Delete a task")
    print("5 : Update task status/priority")
    print("6 : View all tasks")
    print("7 : Filter tasks by status/priority")
    print("8 : Search tasks by title/notes")
    print("9 : View all tasks sorted by title/priority")
    print("Q : Quit")


def print_filter_menu():
    print("\n1 : Filter by status")
    print("2 : Filter by priority level")
    print("B : Back to main menu")


def print_update_menu():
    print("\n1 : Update status")
    print("2 : Update priority level")
    print("B : Back to main menu")


def print_sort_menu():
    print("\n1 : Sort tasks by title")
    print("2 : Sort tasks by priority level")
    print("B : Back to main menu")


def get_submenu_choice(prompt, allowed_choices):
    while True:
        choice = input(prompt)
        if choice in allowed_choices:
            return choice.lower()
        print("Please enter a valid menu option")


def get_choice():
    allowed_choices = {
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "q",
        "Q",
    }
    while True:
        choice = input("Enter a menu option, or Q to quit: ")
        if choice in allowed_choices:
            return choice
        print("Please enter a valid menu option")


def string_input(prompt):
    while True:
        raw_text = input(prompt)
        if raw_text == "":
            print("Field cannot be empty, please try again.")
            continue
        return raw_text


def string_input_blank_allowed(prompt):
    raw_text = input(prompt)
    return raw_text


def get_field(allowed, prompt, error_msg):
    while True:
        field = normalize_value(input(prompt))
        if field not in allowed:
            print(error_msg)
            continue
        return field


def get_status():
    status = get_field(
        ALLOWED_STATUSES,
        "Enter task status. Options: todo, in progress, done: ",
        "Please enter a valid status.",
    )
    return status


def get_priority_level():
    priority = get_field(
        ALLOWED_PRIORITY_LEVELS,
        "Enter task priority level: Options: low, medium, high: ",
        "Please enter a valid priority level.",
    )
    return priority


def get_task_num(tasks):
    allowed_values = {t["id"] for t in tasks}
    while True:
        task_number = input("Enter task id: ")
        try:
            task_integer = int(task_number)
        except ValueError:
            print("Please enter a valid integer")
            continue
        if task_integer in allowed_values:
            return task_integer
        else:
            print("Please enter a valid current task number from", allowed_values)


def view_task(task):
    if task is None:
        return "Not found"
    return (
        f"\nTask number: {task['id']}\n"
        f"Task Title: {task['title']}\n"
        f"Task Status: {task['status']}\n"
        f"Priority Level: {task['priority']}\n"
        f"Notes: {task['notes']}"
    )


def verify_choice(prompt):
    allowed_choices = {"y", "n"}
    while True:
        choice = string_input_blank_allowed(prompt).lower().strip()
        if choice in allowed_choices:
            return choice
        else:
            print("Please enter Y or N.")
        continue


def view_task_short_form(task):
    if task is None:
        return "Not found"
    return f"#{task['id']} [{task['status'].strip()}] [{task['priority'].strip()}] {task['title'].strip()}"


def view_all(tasks):
    return "\n\n".join(view_task_short_form(t) for t in tasks)
