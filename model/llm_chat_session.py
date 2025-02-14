from ollama import chat
from ollama import ChatResponse
from .tool_registry import tool_handlers

class LLMChatSession():
    # Static System Prompt For A LLM Chat Session
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

    # Static Model Name
    model_name = "deepseek-r1:latest"

    # Static Model Tools
    model_tools = []

    def __init__(self, user_id, user_data):
        self.message_history = []

        user_information = f"You are talking with an user on Meshtastic network with ID: {user_id}."
        node_information = f"This is their node information: <node_data> {str(user_data)} </node_data>."

        self.message_history.append({"role": "system", "content": LLMChatSession.system_prompt})
        self.message_history.append({"role": "system", "content": user_information})
        self.message_history.append({"role": "system", "content": node_information})

    def chat_with_tools(self, message):
        # Log the user message to chat history
        self.message_history.append({"role": "user", "content": message})

        # Pass only the user's message history to the chat function.
        response: ChatResponse = chat(model=LLMChatSession.model_name, messages=self.message_history, tools=LLMChatSession.model_tools)

        self.message_history.append(response.message)

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
            self.message_history.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

        # Pass only the user's message history to the chat function.
        response: ChatResponse = chat(model=LLMChatSession.model_name, messages=self.message_history, tools=LLMChatSession.model_tools)
        print('Final response:', response.message.content)

        return response.message.content


    def chat_without_tools(self, message):

        # Log the user message to chat history
        self.message_history.append({"role": "user", "content": message})

        # Pass only the user's message history to the chat function.
        response: ChatResponse = chat(model=LLMChatSession.model_name, messages=self.message_history)

        self.message_history.append(response.message)

        return response.message.content
