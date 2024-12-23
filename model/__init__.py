from model.llm_chat_session import LLMChatSession
import yaml

# Load configuration
with open('./config.yaml', 'r') as file:
        config = yaml.safe_load(file)

LLMChatSession.model_name = config["model"]["name"]

if config["model"]["tool_use"]:
    LLMChatSession.model_tools = [{"type": "function", "function": tool } for tool in config['tools']]