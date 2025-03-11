# Created by Tran Anh Thu Pham
# Created on 8/10/2024
# Publish_Public.py

# Importing necessary libraries
import paho.mqtt.client as mqtt     # MQTT communication library to handle publish-subscribe messaging
import time                         # Provides time-related functions like sleep (for delays)
import random                       # Generates random numbers, used here to create unique client IDs
import socket                       # Handles low-level networking interfaces, used here to manage socket errors

# Generating a random client ID 
client_id = f'subscribe-{random.randint(0, 100)}'    # Create a unique client ID for each session, randomizing between 0 and 100

# Define topic that the client will subscribe to and publish messages to
public_topic = 'public'         # The topic is set to "public", meaning all clients subscribing to 'public' will receive these messages

# Connect the client to the MQTT broker
def connect_mqtt():
    # This function will be called when the client tries to connect to the broker
    def on_connect(client, userdata, flags, rc):
        # 'rc' is the result code: if it's 0, the connection was successful; any other code means failure
        if rc == 0:
            print("Connected to MQTT Broker!")       # Connection successful message
        else:
            print(f"Failed to connect, return code {rc}\n")   # Display error code if connection fails

    # Create a new MQTT client instance using the generated client ID
    # Version 2 of the Callback API is used here for compatibility
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)

    # Authenticate with the broker using your student ID as the username and password
    client.username_pw_set(username="103818400", password="103818400")

    # Attempt to connect to the MQTT broker at the specified server and port
    try:
        print("Attempting to connect to the MQTT broker...")   # Log the connection attempt
        client.connect("rule28.i4t.swin.edu.au", 1883, keepalive=60)  # Connect to the broker at port 1883 with a 60-second keepalive
    except socket.timeout:        # Handle connection timeouts
        print("Connection attempt timed out. The broker might be unreachable or there might be network issues.")
        return None
    except socket.error as e:     # Handle general socket errors
        print(f"Socket error occurred: {e}")
        return None
    except Exception as e:        # Handle any other unexpected exceptions
        print(f"An unexpected error occurred while connecting: {e}")
        return None

    return client   # Return the client object if the connection was successful

# Subscribe the client to topics and handle incoming messages
def subscribe(client: mqtt):
    # This function will be triggered whenever a message is received on a subscribed topic
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")  # Decode and print the received message and the topic

    # Subscribe to all subtopics under the 'public' topic (e.g., 'public/messages', 'public/updates')
    client.subscribe(public_topic + '/#')

    # Set the on_message callback to handle incoming messages
    client.on_message = on_message

# Publish messages to the public topic
def publish(client):
    msg_count = 1    # Initialize a message counter to keep track of the number of messages sent
    while True:      # Infinite loop to keep publishing messages periodically
        time.sleep(10)      # Pause for 10 seconds between each message
        msg = f"messages: {msg_count}"    # Create a message with the current count

        # Send (publish) the message to the 'public' topic
        result = client.publish(public_topic, msg)  # The result tuple contains status, where 0 indicates success
        status = result[0]
        
        # If the message was successfully sent, log the success; otherwise, report failure
        if status == 0:
            print(f"Sent `{msg}` to topic `{public_topic}`")   # Log successful message sending
        else:
            print(f"Failed to send message to topic {public_topic}")   # Log failure in sending message
        msg_count += 1   # Increment the message count for the next message

# Main function to tie everything together and run the MQTT client
def run():          
    # Connect to the MQTT broker
    client = connect_mqtt()
    if client is None:    # If the connection fails, exit the program
        print("Failed to establish connection. Exiting...")
        return
    
    client.loop_start()    # Start the network loop to handle communication
    subscribe(client)      # Subscribe to the public topic to receive messages

    # Continuously publish messages to the public topic
    try:
        publish(client)    # Start publishing messages
    except KeyboardInterrupt:    # If the user manually interrupts the program (Ctrl+C), gracefully disconnect
        print("Program interrupted by user. Disconnecting...")
    finally:
        print("Stopping MQTT loop and exiting...")    # Ensure proper shutdown of the network loop
        client.loop_stop()   # Stop the network loop
        client.disconnect()  # Disconnect from the MQTT broker

# This block ensures the MQTT client is executed only when this script is run directly
if __name__ == '__main__':
    run()
