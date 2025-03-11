# Created by Tran Anh Thu Pham
# Created on 8/10/2024
# Publish_Private.py

# Importing necessary libraries for MQTT communication, introducing delays, generating random client IDs, 
# and handling potential network errors with sockets.
import paho.mqtt.client as mqtt     # MQTT communication library
import time                         # Used to introduce time delays
import random                       # To generate random unique client IDs
import socket                       # Handles socket-related errors for network communication

# Generating a unique client ID for this session.
# 'subscribe-' is prefixed to differentiate between publisher and subscriber clients, followed by a random number.
client_id = f'subscribe-{random.randint(0, 100)}'

# Define private subscription topics using the student ID. These topics are specific to this client.
# The network traffic data is divided into expected and suspicious categories.
private_sub_topic1 = f'{103818400}/Expected Traffic'  # Topic for expected traffic
private_sub_topic2 = f'{103818400}/Suspicious Traffic'  # Topic for suspicious traffic

# Function to connect to the MQTT broker
def connect_mqtt():
    # Callback function executed when the connection to the broker is established.
    def on_connect(client, userdata, flags, rc):
        # rc (result code) 0 means connection successful.
        if rc == 0:
            print("Connected to MQTT Broker!")  # Successful connection message
        else:
            print(f"Failed to connect, return code {rc}\n")  # Failure message with the return code

    # Creating a new MQTT client instance with the generated client_id.
    # Using the latest CallbackAPIVersion.
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)

    # Setting authentication details for the MQTT broker (username and password).
    client.username_pw_set(username="103818400", password="103818400")
    
    # Assigning the on_connect callback function, which is executed when the client connects to the broker.
    client.on_connect = on_connect

    # Attempting to connect to the broker located at "rule28.i4t.swin.edu.au" on port 1883.
    try:
        print("Attempting to connect to the MQTT broker...")
        client.connect("rule28.i4t.swin.edu.au", 1883, keepalive=60)  # Establish connection with keepalive
    except socket.timeout:
        print("Connection attempt timed out. The broker might be unreachable or there might be network issues.")
        return None  # Return None if connection fails
    except socket.error as e:
        print(f"Socket error occurred: {e}")  # Handle any socket-related errors
        return None
    except Exception as e:
        print(f"An unexpected error occurred while connecting: {e}")  # Catch any other errors
        return None

    return client  # Return the connected client

# Function to subscribe to the relevant MQTT topics
def subscribe(client: mqtt):
    # Callback function executed when a message is received on the subscribed topics.
    def on_message(client, userdata, msg):
        # Decoding the message payload (from byte format to string) and printing it alongside the topic it came from.
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

# File path where the local network traffic data is stored.
file_path = "Local_Sample.txt"

# Function to read network traffic data from a file.
def read_network_traffic_from_file(file_path):
    try:
        # Open the file and read each line, ignoring lines that are empty.
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return [line.strip() for line in file if line.strip()]  # Return list of non-empty lines
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")  # Handle the case where the file doesn't exist
        return []
    except IOError as e:
        print(f"Error reading the file: {e}")  # Handle any IO errors
        return []

# Function to publish network traffic data to the appropriate MQTT topic.
def publish_network_traffic(client, protocol, message):
    # Determine the topic to publish the message to, based on the protocol.
    # Suspicious traffic uses SSH or TELNET protocols, everything else is expected traffic.
    topic = private_sub_topic2 if protocol in ["SSH", "TELNET"] else private_sub_topic1

    # Publish the message to the selected topic.
    result, _ = client.publish(topic, message)

    # If the message was successfully published, notify the user.
    if result == mqtt.MQTT_ERR_SUCCESS:
        print(f"Message sent to topic `{topic}`: {message}")
    # If the message couldn't be sent, notify the user of the failure.
    else:
        print(f"Failed to send message to topic `{topic}`")

# Function to process each line of network traffic data.
def process_network_traffic_line(client, line):
    # Split the line into individual components based on spaces.
    elements = line.split()

    # Ensure that there are at least 7 elements in the line (to avoid index errors).
    if len(elements) >= 7:
        no = elements[0]  # First element is the packet number.
        time = elements[1]  # Second element is the timestamp.
        source = elements[2]  # Third element is the source address.
        destination = elements[3]  # Fourth element is the destination address.
        protocol = elements[4]  # Fifth element is the protocol used.
        length = elements[5]  # Sixth element is the packet length.

        # Remaining elements form the "Info" field.
        info = ' '.join(elements[6:])

        # Format the data into a message string to be published.
        message = f"No.: {no}, Time: {time}, Source: {source}, Destination: {destination}, Protocol: {protocol}, Length: {length}, Info: {info}"

        # Publish the formatted message to the relevant topic.
        publish_network_traffic(client, protocol, message)

# Function to read, process, and publish the network traffic data.
def publish(client):
    # Read the network traffic data from the file.
    network_traffic = read_network_traffic_from_file(file_path)
    
    # Process and publish each line of the network traffic data.
    for line in network_traffic:
        process_network_traffic_line(client, line)

# Main function to run the MQTT client
def run():
    client = connect_mqtt()  # Establish connection with the MQTT broker
    if client is None:
        print("Failed to establish connection. Exiting...")  # Exit if connection fails
        return

    client.loop_start()  # Start the MQTT network loop
    subscribe(client)  # Subscribe to the relevant topics

    try:
        # Continuously read and publish network traffic data every 10 seconds
        while True:
            publish(client)  # Publish the data
            time.sleep(10)  # Wait 10 seconds between each publish cycle
    except KeyboardInterrupt:
        print("Program interrupted by user. Disconnecting...")  # Handle user interruption
    finally:
        print("Stopping MQTT loop and exiting...")  # Cleanup before exiting
        client.loop_stop()  # Stop the MQTT network loop
        client.disconnect()  # Disconnect from the MQTT broker

# Execute the run function if the script is run directly.
if __name__ == '__main__':
    run()
