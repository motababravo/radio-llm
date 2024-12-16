# LLM Platform with Meshtastic

This repository provides a platform for integrating Long Language Models (LLMs) with the Meshtastic mesh communication network. It allows users on the mesh network to interact with an LLM for concise, automated responses.

## Features

- Bi-directional communication between Meshtastic and an LLM.
- Support for general broadcast or targeted responses.
- Automatic message chunking for long responses exceeding 200 characters.
- Maintains message history for context-aware interactions.
- Node-specific information (e.g., battery level, location) can be included in responses.
- Tool Use: Your LLM can execute tasks for you based on your prompt

## Requirements

- Python 3.8+
- Meshtastic Python library
- Ollama LLM Python SDK
- PubSub library

## Setup

1. Connect your Meshtastic device via USB or configure it for TCP access.
2. Clone this repository:
   ```bash
   git clone <repo_url>
   cd <repo_name>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
4. Run the script:
   ```bash
   python main.py
   ```
5. To talk with the LLM, you can use normal message or "/tool your_message" to activate tool use.

**Ollama performace with Tool Use on small model (llama 3.2:3b) is not exactly correct. Please test your model extensively before putting it into real use.**

## Configuration

- Modify the LLM model by updating the `chat` function in `chat_with_llm`.
- Adjust chunk size or message length limits as needed.

### Custom Tools

To add your own tool:

1. Define your tool in **model/tool_handler.py**
2. Register your tool in **model/tool_registry.py**
3. Describe your tool in **model/config.yaml**

Please use the same name for your tool across all steps. In the future, this process will be streamlined.

### Different Interface

If you use BLE on your computer, please check Meshtastic documentation [here](https://meshtastic.org/docs/software/python/cli/usage/#utilizing-ble-via-the-python-cli) first. It will help you navigate the meshtastic cli to search for devices and how to authenticate the connection.

```python
# Use this if your node is connected to your local network
interface = meshtastic.tcp_interface.TCPInterface(hostname="meshtastic.local")

# Use this if your node is on BLE
# Before using BLE client, you should connect to your device using your system bluetooth settings.
# Read more on https://meshtastic.org/docs/software/python/cli/usage/#utilizing-ble-via-the-python-cli
interface = meshtastic.ble_interface.BLEClient(address="Your Node BLE Identifier")

# Use this if your node is connected to your computer
interface = meshtastic.serial_interface.SerialInterface() # add param devPath if you have multiple devices connected
```

### Ollama Model

If you use Ollama, please change the model name in model/config.yaml to your installed model.

## How It Works

1. **Receiving Messages**:

   - The script listens for incoming messages on the Meshtastic network.
   - Received messages trigger the LLM to generate a response.

2. **Generating Responses**:

   - The `chat_with_llm` function interacts with the LLM using the `ollama` library.
   - Responses are concise and limited to 200 characters.

3. **Sending Responses**:

   - Responses are sent back to the sender or broadcasted to the network.
   - Messages exceeding 200 characters are sent in chunks.

4. **Node-Specific Information**:

- The script can retrieve and include specific details about the sending node, such as:
  - Node ID
  - Battery level
  - Location (latitude, longitude, altitude)
  - Last heard time
- This information can be appended to responses for context-aware conversations.

## Key Components

- `onReceive(packet, interface)`: Handles incoming messages.
- `chat_with_llm(user_id, message)`: Queries the LLM and returns a response.
- `onConnection(interface)`: Manages connection to the Meshtastic device.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributions

Feel free to submit issues or pull requests for improvements or bug fixes.

## Disclaimer

Ensure compliance with local laws and regulations when using Meshtastic devices and LLMs.
