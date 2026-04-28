from logic import normalize_status, ALLOWED_STATUSES


def print_menu():
    print("\nTask Manager version 1.0")
    print("_________________________")
    print("Select an option:")
    print("1 : Add a task")
    print("2 : View a task")
    print("3 : Update a task")
    print("4 : Delete a task")
    print("5 : Update task status")
    print("6 : View all tasks")
    print("7 : View all todo tasks")
    print("8 : View all done tasks")
    print("9 : View all in progress tasks")
    print("10 : Search tasks by title/notes")
    print("11 : View all tasks sorted by title")
    print("Q : Quit")


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
        "10",
        "11",
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
        string_input = input(prompt)
        if string_input == "":
            print("Field cannot be empty, please try again.")
            continue
        return string_input


def string_input_blank_allowed(prompt):
    string_input = input(prompt)
    if not string_input == "" and string_input.strip() == "":
        return ""
    return string_input


def get_status():
    while True:
        status = normalize_status(
            input("Enter task status. Options: todo, in progress, done: ")
        )
        if status not in ALLOWED_STATUSES:
            print("Please enter a valid status")
            continue
        return status


def get_task_num(tasks):
    allowed_values = {t["id"] for t in tasks}
    while True:
        task_number = input("Enter task id: ")
        try:
            task_int = int(task_number)
        except ValueError:
            print("Please enter a valid integer")
            continue
        if task_int in allowed_values:
            return task_int
        else:
            print("Please enter a valid current task number from", allowed_values)


def view_task(task):
    if task is None:
        return "Not found"
    return (
        f"\nTask number: {task['id']}\n"
        f"Task Title: {task['title']}\n"
        f"Task Status: {task['status']}\n"
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


def view_short(task):
    if task is None:
        return "Not found"
    return f"#{task['id']} [{task['status'].strip()}] {task['title'].strip()}"


def view_all(tasks):
    return "\n\n".join(view_short(t) for t in tasks)
