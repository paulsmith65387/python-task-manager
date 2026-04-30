from storage import load_tasks, save_tasks

from logic import (
    validate_tasks,
    update_task,
    set_task_status,
    delete_task,
    add_task,
    find_task,
    filter_by_status,
    search_by_keywords,
    sort_tasks_by_title,
    get_final_value,
)

from ui import (
    string_input,
    get_choice,
    get_task_num,
    print_menu,
    view_all,
    view_task,
    get_status,
    string_input_blank_allowed,
    verify_choice,
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
        print("\nCurrent task details: ")
        print(view_task(task))
        title = string_input_blank_allowed(
            "\nEnter task title, or press enter to leave unchanged: "
        )
        notes = string_input_blank_allowed(
            "Enter notes, or press enter to leave unchanged: "
        )
        title_flag, final_title = get_final_value(task["title"], title)
        notes_flag, final_notes = get_final_value(task["notes"], notes)
        if title_flag == "new_value" and notes_flag == "new_value":
            print(
                "\nThe following changes have been made: title and notes fields updated:\n",
                view_task(
                    update_task(tasks, final_title, final_notes, task_id),
                ),
            )
        elif title_flag == "new_value" and notes_flag == "unchanged":
            print(
                "\nThe following change has been made: title field updated\n",
                view_task(
                    update_task(tasks, final_title, None, task_id),
                ),
            )
        elif title_flag == "unchanged" and notes_flag == "new_value":
            print(
                "\nThe following change has been made: notes field updated:\n",
                view_task(
                    update_task(tasks, None, final_notes, task_id),
                ),
            )
        else:
            print("\nNo changes made, task details:")
            print(view_task(task))
            return
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
        print("\nTask details: ")
        print(view_task(task))
        choice = verify_choice("\nAre you sure you want to delete the task? Y/N: ")
        if choice == "y":
            print("\nTask deleted:")
            print(view_task(task))
            delete_task(tasks, task_id)
            save_tasks(tasks)
            return
        else:
            print("\nNo changes made.")
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
        if status != task["status"]:
            print(
                "\nThe following update has been made:\n",
                view_task(set_task_status(task, status)),
            )
            save_tasks(tasks)
        else:
            print("\nNo changes made:\n", view_task(task))
        return

    def cmd_view_all():
        if not tasks:
            print("\nNo tasks yet, use option 1 to add a task.")
            return
        print("\nAll tasks:\n")
        print(view_all(tasks))
        return

    def cmd_view_by_status(status):
        if not tasks:
            print("\nNo tasks yet, use option 1 to add a task.")
            return
        filtered = filter_by_status(tasks, status)
        if not filtered:
            print(f"\nNo {status} tasks.")
            return
        print(f"\nAll tasks with status {status}:\n")
        print(view_all(filtered))
        return

    def cmd_view_done():
        cmd_view_by_status("done")

    def cmd_view_in_progress():
        cmd_view_by_status("in progress")

    def cmd_view_todo():
        cmd_view_by_status("todo")

    def cmd_search_tasks():
        if not tasks:
            print("\nNo tasks yet.")
            return
        search_string = string_input("Enter keyword to search task titles and notes: ")
        results = search_by_keywords(tasks, search_string)
        if not results:
            print("\nNo matching tasks")
            return
        print(f"\nShowing results for search string: '{search_string}':\n")
        print(view_all(results))

    def cmd_sort_tasks():
        if not tasks:
            print("\nNo tasks yet.")
            return
        print("\nAll tasks sorted by title:\n")
        print(view_all(sort_tasks_by_title(tasks)))

    cmd_menu = {
        "1": cmd_add_task,
        "2": cmd_view_task,
        "3": cmd_update_task,
        "4": cmd_delete_task,
        "5": cmd_update_status,
        "6": cmd_view_all,
        "7": cmd_view_todo,
        "8": cmd_view_done,
        "9": cmd_view_in_progress,
        "10": cmd_search_tasks,
        "11": cmd_sort_tasks,
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
