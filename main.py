import meshtastic
import meshtastic.ble_interface
import meshtastic.tcp_interface
import meshtastic.serial_interface
from pubsub import pub
import time
from chat import chat_with_llm

def get_node_summary(node_data):
    user_info = node_data.get("user", {})
    position = node_data.get("position", {})
    metrics = node_data.get("deviceMetrics", {})

    summary = (
        f"Node ID: {user_info.get('id', 'Unknown')}\n"
        f"Name: {user_info.get('longName', 'Unknown')}\n"
        f"Short Name: {user_info.get('shortName', 'Unknown')}\n"
        f"Battery: {metrics.get('batteryLevel', 'Unknown')}%\n"
        f"Position: "
        f"Lat {position.get('latitude', 'N/A')}, "
        f"Lon {position.get('longitude', 'N/A')}, "
        f"Alt {position.get('altitude', 'N/A')}m\n"
    )

    return summary

def onReceive(packet, interface):  # called when a packet arrives
    try:
        sender = str(packet["fromId"])
        node_data = get_node_summary(interface.nodes[sender])

        text_message_present =  "decoded" in packet and "text" in packet["decoded"]

        if text_message_present:
            received_text = packet["decoded"]["text"]

            print(f"Received from {sender}: {received_text}")

            if packet['toId'] == '^all':
                response = chat_with_llm("general_chat", node_data, received_text)
            else:
                response = chat_with_llm(str(sender), node_data, received_text)

            full_message = response

            print("Send: " + str(response).strip())

            # Ensure the full message is sent if it's less than 200 characters
            if len(full_message) <= 200:
                if packet['toId'] == '^all':
                    interface.sendText(full_message, wantAck=True)
                else:
                    interface.sendText(full_message, destinationId=sender, wantAck=True)
            else:
                # Chunk the response if it exceeds 200 characters
                chunk_size = 150
                for i in range(0, len(full_message), chunk_size):
                    chunk = full_message[i:i + chunk_size]
                    print("------")
                    print(chunk)
                    if packet['toId'] == '^all':
                        interface.sendText(chunk, wantAck=True)
                    else:
                        interface.sendText(chunk, destinationId=sender, wantAck=True)

    except Exception as e:
        print(f"Error: {e}") # Prints error message

def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    print("Device successfully connected!")
    

pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")

# Use this if your node is connected to your local network
# interface = meshtastic.tcp_interface.TCPInterface(hostname="meshtastic.local")

# Use this if your node is on BLE
# Before using BLE client, you should connect to your device using your system bluetooth settings.
# Read more on https://meshtastic.org/docs/software/python/cli/usage/#utilizing-ble-via-the-python-cli
# interface = meshtastic.ble_interface.BLEClient(address="you can find address by using meshtastic cli: meshtastic --ble-scan")

# Use this if your node is connected to your computer
interface = meshtastic.serial_interface.SerialInterface()

while True:
    time.sleep(10000)