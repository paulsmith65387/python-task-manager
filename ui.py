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
    print("Q : Quit")
    
def get_choice():
    allowed_choices = {"1", "2", "3", "4", "5", "6", "q", "Q"}
    while True:
        choice = input("Enter a menu option, or Q to quit: ")
        if choice in allowed_choices:
            return choice
        print("Please enter a valid menu option")


def string_input(prompt):
    while True:
        strng = input(prompt)
        if strng == "":
            print("Field cannot be empty, please try again.")
            continue
        return strng


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


def view_all(tasks):
    return "\n\n".join(view_task(t) for t in tasks)
