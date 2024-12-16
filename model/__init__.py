import model.chat_handler as chat_handler
import yaml

# Load configuration
with open('./config.yaml', 'r') as file:
        config = yaml.safe_load(file)

chat_handler.model_name = config["model"]["name"]

if config["model"]["tool_use"]:
    chat_handler.model_tools = [{"type": "function", "function": tool } for tool in config['tools']]