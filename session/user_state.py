from enum import Enum

class UserState(Enum):
    NEW_CHAT = 0
    NORMAL_CHAT = 1
    CHAT_WITH_LLM = 2
    ECHO = 3