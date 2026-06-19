import json
import datetime


TASKS_FILE = "tasks.json"


def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def cmd_add(tasks, args):
    if not args:
        print("Error: usage: add <task text>")
        return
    title = " ".join(args)
    task = {
        "id": next_id(tasks),
        "title": title,
        "status": "pending",
        "created_at": datetime.date.today().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {title}")


def cmd_done(tasks, args):
    if len(args) != 1:
        print("Error: usage: done <task_id>")
        return
    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: task_id must be an integer")
        return
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "done"
            save_tasks(tasks)
            print(f"Task #{task_id} marked as done.")
            return
    print(f"Error: task #{task_id} not found.")


def cmd_delete(tasks, args):
    if len(args) != 1:
        print("Error: usage: delete <task_id>")
        return
    try:
        task_id = int(args[0])
    except ValueError:
        print("Error: task_id must be an integer")
        return
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"Task #{task_id} deleted.")
            return
    print(f"Error: task #{task_id} not found.")


def cmd_list(tasks, args):
    if len(args) == 0:
        filtered = tasks
    elif len(args) == 2:
        try:
            start = datetime.date.fromisoformat(args[0])
            end = datetime.date.fromisoformat(args[1])
        except ValueError:
            print("Error: dates must be in YYYY-MM-DD format")
            return
        filtered = []
        for t in tasks:
            try:
                d = datetime.date.fromisoformat(t["created_at"])
            except ValueError:
                continue
            if start <= d <= end:
                filtered.append(t)
    else:
        print("Error: usage: list [<start_date> <end_date>]")
        return

    if not filtered:
        print("No tasks found.")
        return

    print(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Date':<12}")
    print("-" * 56)
    for t in filtered:
        print(f"{t['id']:<4} {t['status']:<8} {t['title']:<30} {t['created_at']:<12}")


def cmd_help():
    print("Available commands:")
    print("  add <task text>            - Add a new task")
    print("  done <task_id>             - Mark a task as done")
    print("  delete <task_id>           - Delete a task")
    print("  list                       - List all tasks")
    print("  list <start> <end>         - List tasks in a date range")
    print("  help                       - Show this help")
    print("  exit                       - Exit the application")


def main():
    tasks = load_tasks()
    while True:
        try:
            line = input("todo> ").strip()
        except EOFError:
            print()
            break
        if not line:
            continue

        parts = line.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "exit":
            break
        elif command == "help":
            cmd_help()
        elif command == "add":
            cmd_add(tasks, args)
        elif command == "done":
            cmd_done(tasks, args)
        elif command == "delete":
            cmd_delete(tasks, args)
        elif command == "list":
            cmd_list(tasks, args)
        else:
            print(f"Error: unknown command '{command}'. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
