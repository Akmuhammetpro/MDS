# Specification: CLI TODO List Application

## 1. Project Overview
Create a command-line interface (CLI) application in Python to manage a TODO list. The application must run an interactive REPL (Read-Eval-Print Loop) where it continuously prompts the user for input until the user exits.

## 2. Data Storage
- Tasks must be saved locally in a file named `tasks.json`.
- The application should load existing tasks from this file on startup.
- Every time a task is added, modified, or deleted, the changes must be saved to `tasks.json` immediately.
- A task object should contain: `id` (integer), `title` (string), `status` ("pending" or "done"), and `created_at` (date string in YYYY-MM-DD format).

## 3. Supported Commands
The REPL must support the following commands exactly:

- `add <task text>`
  Creates a new task with status "pending" and sets `created_at` to today's date.
  Example: `add Buy milk`

- `done <task_id>`
  Changes the status of the specified task ID to "done".
  Example: `done 1`

- `delete <task_id>`
  Removes the task with the specified ID from the list.
  Example: `delete 1`

- `list`
  Displays all tasks in a readable format, showing ID, Status, Title, and Date.

- `list <start_date> <end_date>`
  Displays only the tasks created within the specified date range. Dates are in YYYY-MM-DD format.
  Example: `list 2026-06-01 2026-06-30`

- `help`
  Displays instructions and a list of all available commands.

- `exit`
  Saves any pending changes and closes the application.

## 4. Technical and UX Requirements
- Use standard Python libraries only (e.g., `json`, `datetime`). No external dependencies like `click` or `rich`.
- The input prompt should look like this: `todo> `
- Handle user errors gracefully. If the user types a command that doesn't exist, or provides an invalid ID/Date, print a clear error message and return to the prompt without crashing.