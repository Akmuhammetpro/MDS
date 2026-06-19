import json
import requests
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression, e.g. '2 + 3 * 4'"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for Bucharest.",
            "parameters": {
                "type": "object",
                "properties": {}, 
            },
        },
    }
]

def execute_calculate(args):
    try:
        result = eval(args["expression"])
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def execute_get_weather(args):
    url = "https://api.open-meteo.com/v1/forecast?latitude=44.4268&longitude=26.1025&current_weather=true"
    try:
        response = requests.get(url).json()
        temp = response["current_weather"]["temperature"]
        return f"Current temperature in Bucharest is {temp}°C."
    except Exception as e:
        return f"Weather API Error: {e}"

messages = [{"role": "system", "content": "You are a helpful assistant. You MUST use the provided tools to answer questions about math or weather."}]

print("AI Agent ready! Ask me about math or weather. (Type 'exit' to quit)")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['exit', 'quit']:
        break
        
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="mistral",
        messages=messages,
        tools=tools
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        messages.append(msg) 
        
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"⚙️ [Executing tool: {func_name}({args})]")
            
            if func_name == "calculate":
                result = execute_calculate(args)
            elif func_name == "get_weather":
                result = execute_get_weather(args)
                
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
            
        final_response = client.chat.completions.create(
            model="mistral",
            messages=messages,
            tools=tools
        )
        final_msg = final_response.choices[0].message.content
        messages.append({"role": "assistant", "content": final_msg})
        print(f"🤖 AI: {final_msg}")
        
    else:
        messages.append({"role": "assistant", "content": msg.content})
        print(f" AI: {msg.content}")