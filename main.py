from storage import load_tasks, save_tasks

from logic import (
    validate_tasks,
    update_task,
    set_task_status,
    delete_task,
    add_task,
    find_task,
)

from ui import (
    string_input,
    get_choice,
    get_task_num,
    print_menu,
    view_all,
    view_task,
    get_status,
)


def main():
    tasks = load_tasks()

    def cmd_add_task():
        title = string_input("Enter task title: ")
        status = get_status()
        notes = string_input("Enter notes: ")
        print(
            "\n The following task has been added:\n",
            add_task(tasks, title, status, notes),
        )
        save_tasks(tasks)

    def cmd_view_task():
        if not tasks:
            print("No tasks yet. Use option 1 to add a task.")
            return
        task_id = get_task_num(tasks)
        task = find_task(tasks, task_id)
        if task is None:
            print("Not found.")
            return
        print(view_task(task))
        return

    def cmd_update_task():
        if not tasks:
            print("\nNo tasks to update yet, use option 1 to add a task.")
            return

        task_id = get_task_num(tasks)
        task = find_task(tasks, task_id)
        if task is None:
            print("Task not found.")
            return

        title = string_input("Enter task title: ")
        notes = string_input("Enter notes: ")

        print(
            "\n The following task has been updated:\n",
            update_task(tasks, title, notes, task_id),
        )
        save_tasks(tasks)
        return

    def cmd_delete_task():
        if not tasks:
            print("\nNo tasks to delete yet, use option 1 to add a task.")
            return

        task_id = get_task_num(tasks)
        task = find_task(tasks, task_id)
        if task is None:
            print("Task not found.")
            return
        print(delete_task(tasks, task_id))
        save_tasks(tasks)
        return

    def cmd_update_status():
        if not tasks:
            print("No tasks to update.")
            return
        task_id = get_task_num(tasks)
        task = find_task(tasks, task_id)

        if task is None:
            print("Task not found.")
            return  # back to menu

        status = get_status()
        print(
            "\n The following update has been made:",
            set_task_status(task, status),
        )
        save_tasks(tasks)
        return

    def cmd_view_all():
        if not tasks:
            print("\nNo tasks yet, use option 1 to add a task.")
            return
        print("\nAll tasks:\n")
        print(view_all(tasks))
        return

    cmd_menu = {
        "1": cmd_add_task,
        "2": cmd_view_task,
        "3": cmd_update_task,
        "4": cmd_delete_task,
        "5": cmd_update_status,
        "6": cmd_view_all,
    }

    if not validate_tasks(tasks):
        print("Fatal error, corrupted task list")
        return
    while True:
        print_menu()
        choice = get_choice()
        if choice.upper() == "Q":
            print("Goodbye.")
            save_tasks(tasks)
            break
        cmd_menu[choice]()


if __name__ == "__main__":
    main()
