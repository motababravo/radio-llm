# LLM Platform with Meshtastic

This repository provides a platform for integrating Long Language Models (LLMs) with the Meshtastic mesh communication network. It allows users on the mesh network to interact with an LLM for concise, automated responses.

## Features

- Bi-directional communication between Meshtastic and an LLM.
- Support for general broadcast or targeted responses.
- Automatic message chunking for long responses exceeding 200 characters.
- Maintains message history for context-aware interactions.
- Node-specific information (e.g., battery level, location) can be included in responses.
- Online chat support using Gemini (via google.generativeai).

## Requirements

- Python 3.8+
- Meshtastic Python library
- Ollama LLM Python SDK
- PubSub library
- [Optional] Gemini Generative AI Python SDK

Install dependencies using:

```bash
pip install -r requirement.txt
```

## Setup

1. Connect your Meshtastic device via USB or configure it for TCP access.
2. Clone this repository:
   ```bash
   git clone <repo_url>
   cd <repo_name>
   ```
3. Run the script:
   ```bash
   python main.py
   ```

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

## Configuration

- Modify the LLM model by updating the `chat` function in `chat_with_llm`.
- Adjust chunk size or message length limits as needed.

### Different Interface

```python
# Use this if your node is connected to your local network
interface = meshtastic.tcp_interface.TCPInterface(hostname="meshtastic.local")

# Use this if your node is on BLE
# You can search for ble devices using BLE Scanner on your phone or using meshtastic cli
# Find address using meshtastic cli: meshtastic --ble-scan
interface = meshtastic.ble_interface.BLEClient(address="Your Node BLE Identifier")

# Use this if your node is connected to your computer
interface = meshtastic.serial_interface.SerialInterface() # add param devPath if you have multiple devices connected
```

### Ollama

If you use Ollama, please change the model name in chat.py to your installed model.

In my case, I'm using "llama3.2:3b".

### Gemini

If you use Gemini, please create a .env file and put your Gemini key inside.

```
GEMINI_API_KEY = "Your Key"
```

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
