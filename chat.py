from ollama import chat
from ollama import ChatResponse

message_history = {}


def chat_with_llm(user_id, user_data, message):
    if user_id not in message_history:
        message_history[user_id] = []
        message_history[user_id].append({"role": "system", "content": f"You are talking with an user on Meshtastic network with ID: {user_id}. You are an expert on everything. Your answer is concise, short and to the point. Every response has to be less than 200 characters, or else your message won't be received literally. Here is the user information: {str(user_data)}"})

    message_history[user_id].append({"role": "user", "content": message})

    # Pass only the user's message history to the chat function.
    response: ChatResponse = chat(model='llama3.2:3b', messages=message_history[user_id])

    message_history[user_id].append(response.message)

    return response.message.content

