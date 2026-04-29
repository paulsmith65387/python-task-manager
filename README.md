# Python Task Manager

This is a basic task manager that runs in the terminal. I am using it to learn Python concepts and gain experience with program structure, testing, and Git.

It uses separate modules, JSON persistence, and command dispatch.

## Current Features

- Add tasks
- View one task
- View all tasks
- Update title and notes
- Update task status
- Delete tasks with confirmation
- Filter tasks by status
- Search tasks by title and notes
- Sort tasks by title
- Save and load tasks from JSON
- Includes scratch tests for core logic

## Project Structure

- `main.py` - command flow and menu dispatch
- `logic.py` - task operations, validation, search, filtering, sorting, and update behaviour
- `ui.py` - input and display helper functions
- `storage.py` - JSON persistence
- `scratch_tests.py` - informal logic test harness
- `.gitignore` - excludes local runtime data such as `tasks.json`

## What I Have Learned and Practised

This is my first project to use separate modules for different responsibilities. It makes extensive use of lists and dictionaries, which has helped improve my fluency with these data structures.

The project has helped me practise validation for loaded task data and user-created tasks. It is also my first project with data that persists between sessions, which is a step up from previous work that ran purely in memory.

The app has grown from an initial create, view, and delete program into something with search, filtering, sorting, partial update functionality, and delete confirmation.

I have also added a scratch test module to check expected behaviour in core logic functions and have begun using Git and GitHub to track changes.

## How to Run

Clone or download the repository, then run `python3 main.py` from the project folder.

On some systems, the command may be `python main.py`.

A local `tasks.json` file is created automatically when the app runs. This file is ignored by Git.

## Future Improvements

- Convert scratch tests to pytest
- Add due dates
- Add priority levels
- Improve error messages
- Add terminal examples or screenshots