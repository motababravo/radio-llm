import meshtastic
import meshtastic.ble_interface
import meshtastic.tcp_interface
import meshtastic.serial_interface
from pubsub import pub
import time
from session import UserSession

user_sessions: dict[str, UserSession] = {}

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

def send_message(to_id, full_message, interface):
    print("Send: " + str(full_message).strip())

     # Ensure the full message is sent if it's less than 200 characters
    if len(full_message) <= 200:
        if to_id == 'all':
            interface.sendText(full_message, wantAck=True)
        else:
            interface.sendText(full_message, destinationId=to_id, wantAck=True)
    else:
        # Chunk the response if it exceeds 200 characters
        chunk_size = 150
        for i in range(0, len(full_message), chunk_size):
            chunk = full_message[i:i + chunk_size]
            print("------")
            print(chunk)
            if to_id == 'all':
                interface.sendText(chunk, wantAck=True)
            else:
                interface.sendText(chunk, destinationId=to_id, wantAck=True)

def onReceive(packet, interface):  # called when a packet arrives
    try:
        sender = "all" if packet['toId'] == '^all' else str(packet["fromId"])

        node_data = get_node_summary(interface.nodes[str(packet["fromId"])])

        text_message_present =  "decoded" in packet and "text" in packet["decoded"]

        if text_message_present:
            received_text = packet["decoded"]["text"]

            print(f"Received from {sender}: {received_text}")

            if sender not in user_sessions:
                user_sessions[sender] = UserSession(sender, node_data)

            response = user_sessions[sender].chat(received_text)

            if response != "":
                send_message("all" if packet['toId'] == '^all' else sender, response, interface)

    except Exception as e:
        print(f"Error: {e}") # Prints error message

def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    print("Device successfully connected!")
    

pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")

# Use this if your node is connected to your computer
interface = meshtastic.serial_interface.SerialInterface()

while True:
    time.sleep(10000)