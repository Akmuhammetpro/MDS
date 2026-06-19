import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

try:
    with open("tasks.json", "r") as f:
        tasks_db = json.load(f)
except FileNotFoundError:
    tasks_db = []

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks_db, f, indent=4)

tools = [{
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Add a new task to the todo list.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The task description"},
                "deadline": {"type": "string", "description": "Date in DD-MM-YYYY format"}
            },
            "required": ["title", "deadline"],
        },
    },
}]

def execute_add_task(args):
    tasks_db.append({"title": args["title"], "deadline": args["deadline"]})
    save_tasks()
    return f"Task '{args['title']}' added successfully."

messages = [{"role": "system", "content": "You are a task assistant. Extract title and date for add_task tool."}]
print("Task Agent: Ready to schedule! (e.g., 'Add a task for paying taxes by May 25 this year')")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit':
        break
    
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="mistral", messages=messages, tools=tools)
    msg = response.choices[0].message
    
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = execute_add_task(args)
            print(f" {result}")
    else:
        print(f"AI: {msg.content}")