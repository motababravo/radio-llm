from ollama import chat
from ollama import ChatResponse
from .tool_registry import tool_handlers

# Load model name
model_name = "llama3.2:3b"

# Defualt tools
model_tools = []

# Store message history
# TODO: Store this in sqlite for persistent storage
message_history = {}

system_prompt = """
You are an Ollama node on Meshtastic. Keep in mind the following limitations of the Meshtastic network:

- Limited message length and transmission capacity. (<200 char or else your message will be dropped)
- Messages must be concise and clear due to the low-bandwidth nature of the network.
- Avoid sending unnecessary data or long messages.

When composing a message, please:
- Keep sentences short.
- Use abbreviations and acronyms when possible, as long as they remain understandable.
- Prioritize essential information only.

Use direct language to convey the message quickly.
"""

def init_chat(user_id, user_data):
    message_history[user_id] = []

    user_information = f"You are talking with an user on Meshtastic network with ID: {user_id}."
    node_information = f"This is their node information: <node_data> {str(user_data)} </node_data>."

    message_history[user_id].append({"role": "system", "content": system_prompt})
    message_history[user_id].append({"role": "system", "content": user_information})
    message_history[user_id].append({"role": "system", "content": node_information})

def chat_with_tools(user_id, user_data, message):
    # If this is the first time an user contact
    if user_id not in message_history:
        init_chat(user_id, user_data)

    # Log the user message to chat history
    message_history[user_id].append({"role": "user", "content": message})

    # Pass only the user's message history to the chat function.
    response: ChatResponse = chat(model=model_name, messages=message_history[user_id], tools=model_tools)

    message_history[user_id].append(response.message)

    # If no tool call is used, return early
    if not response.message.tool_calls:
        return response.message.content
    
    # If tool call is used
    for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := tool_handlers.get(tool.function.name):
            print('Calling function:', tool.function.name)
            print('Arguments:', tool.function.arguments)

            output = function_to_call(**tool.function.arguments)
        else:
            output = f"Tool {tool.function.name} was not found"
            
        print('Function output:', output)
        message_history[user_id].append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

    # Pass only the user's message history to the chat function.
    response: ChatResponse = chat(model=model_name, messages=message_history[user_id], tools=model_tools)
    print('Final response:', response.message.content)

    return response.message.content


def chat_without_tools(user_id, user_data, message):
    # If this is the first time an user contact
    if user_id not in message_history:
        init_chat(user_id, user_data)

    # Log the user message to chat history
    message_history[user_id].append({"role": "user", "content": message})

    # Pass only the user's message history to the chat function.
    response: ChatResponse = chat(model=model_name, messages=message_history[user_id])

    message_history[user_id].append(response.message)

    return response.message.content
    