import google.generativeai as genai
import os
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv() 

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

message_history = {}

def chat_with_llm(user_id, user_data, message):
    if user_id not in message_history:
        message_history[user_id] = []
        message_history[user_id].append({"role": "system", "parts": f"You are talking with an user on Meshtastic network with ID: {user_id}. You are an expert on everything. Your answer is concise, short and to the point. Every response has to be less than 200 characters, or else your message won't be received literally. Here is the user information: {str(user_data)}"})

    chat = model.start_chat(
        history=message_history[user_id]
    )

    # Pass only the user's message history to the chat function.
    response = chat.send_message(message)

    message_history[user_id].append({"role": "user", "parts": message})
    message_history[user_id].append({"role": "model", "parts": response.text})

    return response.text
