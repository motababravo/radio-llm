from session.user_state import UserState
from model import LLMChatSession

class UserSession:
    def __init__(self, user_id: str, user_data):
        self.current_state = UserState.NEW_CHAT
        self.user_id = user_id
        self.user_data = user_data
        self.llm_chat_session = None

    def chat_with_llm(self, message, tools_enabled = False):
        if self.llm_chat_session == None:
            self.llm_chat_session = LLMChatSession(self.user_id, self.user_data)
        
        if tools_enabled:
            return self.llm_chat_session.chat_with_tools(message)
        
        return self.llm_chat_session.chat_without_tools(message)

    def process_command(self, command: str, message: str) -> str:

        if command == "tool":
            return self.chat_with_llm(message, tools_enabled=True)
        elif command == "enable_llm":
            self.current_state = UserState.CHAT_WITH_LLM
            return "Chat with LLM enabled."
        elif command == "enable_echo":
            self.current_state = UserState.ECHO
            return "Echo enabled"
        elif command == "disable_echo" or command == "disable_llm" or command == "go_to_normal":
            self.current_state = UserState.NORMAL_CHAT
            return "Normal chat enabled."
        
        return f"Command /{command} not recognized."

    def chat(self, message: str) -> str:
        message = message.strip()

        if len(message) == 0:
            return ""
        
        if message[0] == "/":
            if " " in message:
                command, message = message.split(" ", 1)
            else:
                command, message = message, ""

            return self.process_command(command[1:], message)
        
        if self.current_state == UserState.ECHO:
            return message
        elif self.current_state == UserState.NEW_CHAT:
            self.current_state = UserState.NORMAL_CHAT
            return "Hello, this is MeshAI. You can enable LLM by /enable_llm or echo by /enable_echo."
        elif self.current_state == UserState.NORMAL_CHAT:
            return ""
        elif self.current_state == UserState.CHAT_WITH_LLM:
            return self.chat_with_llm(message)