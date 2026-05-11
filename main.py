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
    sort_tasks,
    get_final_value,
    set_task_priority,
    filter_by_priority_level,
    plan_update,
)

from ui import (
    string_input,
    get_choice,
    get_task_num,
    print_menu,
    view_all,
    view_task,
    get_status,
    get_priority_level,
    string_input_blank_allowed,
    verify_choice,
    print_filter_menu,
    get_submenu_choice,
    print_update_menu,
    print_sort_menu,
)


def main():
    tasks = load_tasks()

    def cmd_add_task():
        title = string_input("Enter task title: ")
        status = get_status()
        priority = get_priority_level()
        notes = string_input("Enter notes: ")
        print(
            "\n The following task has been added:\n",
            add_task(tasks, title, status, priority, notes),
        )
        save_tasks(tasks)

    def cmd_view_task():
        if not tasks:
            print("\nNo tasks yet. Use option 1 to add a task.")
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
            print("\nNo tasks yet. Use option 1 to add a task.")
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
        update_flag = plan_update(title_flag, notes_flag)
        if update_flag is None:
            print("\nNo changes made, task details:")
            print(view_task(task))
            return
        update_dict = {
            "both": {
                "message": "\nThe following changes have been made: title and notes fields updated:",
                "title_arg": final_title,
                "notes_arg": final_notes,
            },
            "title": {
                "message": "\nThe following change has been made: title field updated:",
                "title_arg": final_title,
                "notes_arg": None,
            },
            "notes": {
                "message": "\nThe following change has been made: notes field updated:",
                "title_arg": None,
                "notes_arg": final_notes,
            },
        }
        display_msg = update_dict[update_flag]["message"]
        title_arg = update_dict[update_flag]["title_arg"]
        notes_arg = update_dict[update_flag]["notes_arg"]
        print(display_msg)
        print(view_task(update_task(tasks, title_arg, notes_arg, task_id)))
        save_tasks(tasks)
        return

    def cmd_delete_task():
        if not tasks:
            print("\nNo tasks yet. Use option 1 to add a task.")
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

    def cmd_sort_tasks():
        if not tasks:
            print("\nNo tasks yet. Use option 1 to add a task.")
            return
        sort_choice = {
            "1": {"sort_key": "title", "display_key": "title"},
            "2": {"sort_key": "status", "display_key": "status"},
            "3": {"sort_key": "priority", "display_key": "priority level"},
        }
        print_sort_menu()
        choice = get_submenu_choice(
            "View all tasks sorted by title/status/priority level, or back to main menu: ",
            {"1", "2", "3", "b", "B"},
        )
        if choice == "b":
            return
        sort_key = sort_choice[choice]["sort_key"]
        display_label = sort_choice[choice]["display_key"]
        print(f"\nAll tasks sorted by {display_label}:\n")
        print(view_all(sort_tasks(tasks, sort_key)))

    def cmd_update_task_field():
        if not tasks:
            print("\nNo tasks yet. Use option 1 to add a task.")
            return
        update_choice = {
            "1": {
                "get_field": get_status,
                "task_key": "status",
                "set_field": set_task_status,
            },
            "2": {
                "get_field": get_priority_level,
                "task_key": "priority",
                "set_field": set_task_priority,
            },
        }
        print_update_menu()
        choice = get_submenu_choice(
            "Update a task's status or priority level, or back to main menu: ",
            {"1", "2", "b", "B"},
        )
        if choice == "b":
            return
        task_id = get_task_num(tasks)
        task = find_task(tasks, task_id)
        if task is None:
            print("Task not found.")
            return
        chosen_update = update_choice[choice]
        new_field_value = chosen_update["get_field"]()
        task_key = chosen_update["task_key"]
        setter = chosen_update["set_field"]
        if new_field_value != task[task_key]:
            print(
                "\nThe following update has been made:\n",
                view_task(setter(task, new_field_value)),
            )
            save_tasks(tasks)
        else:
            print("\nNo changes made:\n", view_task(task))
        return

    def cmd_view_all():
        if not tasks:
            print("\nNo tasks yet. Use option 1 to add a task.")
            return
        print("\nAll tasks:\n")
        print(view_all(tasks))
        return

    def cmd_view_by_status():
        status = get_status()
        filtered = filter_by_status(tasks, status)
        if not filtered:
            print(f"\nNo tasks with status '{status}'.")
            return
        print(f"\nAll tasks with status '{status}':\n")
        print(view_all(filtered))
        return

    def cmd_view_by_priority_level():
        priority = get_priority_level()
        filtered = filter_by_priority_level(tasks, priority)
        if not filtered:
            print(f"\nNo {priority} priority tasks.")
            return
        print(f"\nAll tasks with {priority} priority:\n")
        print(view_all(filtered))
        return

    def cmd_view_by_field():
        filter_choices = {
            "1": cmd_view_by_status,
            "2": cmd_view_by_priority_level,
        }
        if not tasks:
            print("\nNo tasks yet. Use option 1 to add a task.")
            return
        print_filter_menu()
        choice = get_submenu_choice(
            "Filter by status or priority level, or B to return to main menu: ",
            {"1", "2", "b", "B"},
        )
        if choice == "b":
            return
        filter_choices[choice]()

    def cmd_search_tasks():
        if not tasks:
            print("\nNo tasks yet. Use option 1 to add a task.")
            return
        search_string = string_input("Enter keyword to search task titles and notes: ")
        results = search_by_keywords(tasks, search_string)
        if not results:
            print("\nNo matching tasks")
            return
        print(f"\nShowing results for search string: '{search_string}':\n")
        print(view_all(results))

    cmd_menu = {
        "1": cmd_add_task,
        "2": cmd_view_task,
        "3": cmd_update_task,
        "4": cmd_delete_task,
        "5": cmd_update_task_field,
        "6": cmd_view_all,
        "7": cmd_view_by_field,
        "8": cmd_search_tasks,
        "9": cmd_sort_tasks,
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
