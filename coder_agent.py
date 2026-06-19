import json, subprocess
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Read file (cat), list files (ls), or run python scripts.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    }
]

def execute_safe_command(command):
    # Автоматическая замена для Windows
    if command.startswith("cat "):
        command = command.replace("cat ", "type ")
    elif command.strip() == "ls":
        command = "dir"
        
    print(f"\nSECURITY: AI wants to run: '{command}'")
    confirm = input("Allow execution? (y/n): ")
    
    if confirm.lower() != 'y':
        return "Denied by user."
        
    try:
        res = subprocess.run(command, shell=True, capture_output=True, text=True)
        return res.stdout or res.stderr
    except Exception as e:
        return str(e)
    
messages = [{"role": "system", "content": "You are a coding agent. Always verify the command with the user."}]

print("Coding Agent: I can help you read and run files. What should I do?")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit': break
        
    messages.append({"role": "user", "content": user_input})
    
    # Используем правильное имя модели (убедитесь через 'ollama list')
    response = client.chat.completions.create(model="mistral:latest", messages=messages, tools=tools)
    msg = response.choices[0].message
    
    if msg.tool_calls:
        messages.append(msg) 
        
        for tool_call in msg.tool_calls:
            cmd = json.loads(tool_call.function.arguments)["command"]
            res = execute_safe_command(cmd)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": res,
            })
            
        final_response = client.chat.completions.create(
            model="mistral:latest", 
            messages=messages, 
            tools=tools
        )
        print(f"\nAI: {final_response.choices[0].message.content}")
        messages.append({"role": "assistant", "content": final_response.choices[0].message.content})
    else:
        print(f"\nAI: {msg.content}")
        messages.append({"role": "assistant", "content": msg.content})