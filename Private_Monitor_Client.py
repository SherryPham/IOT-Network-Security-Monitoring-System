# Created by Tran Anh Thu Pham
# Created on 8/10/2024
# Private_Monitor_Client.py

# Importing necessary libraries
import paho.mqtt.client as mqtt     # For MQTT communication (publish/subscribe to topics)
import time                         # Used to introduce delays in execution (e.g., between message publishing)
import random                       # Used to generate unique client IDs for MQTT connections
import socket                       # Handles network-related errors (e.g., connection issues)

# Generating a unique client ID
client_id = f'publish-{random.randint(0, 100)}'  # Creates a random ID to distinguish this client instance

# Defining the private subscription topics for incoming messages
private_sub_topic2 = f'{103818400}/Suspicious Traffic'  # Topic to subscribe to suspicious traffic notifications
private_sub_topic3 = f'{103818400}/Solutions'  # Topic for publishing/receiving solution or recommendation messages

# Define the file path for recommendations to be published
recommendations_file_path = "Recommendations.txt"  # Path where the recommendation messages are stored in a file

# Variable to keep track of whether all recommendations have been published
all_recommendations_published = False  # Set to False initially, changes when all recommendations are sent

# Establish an MQTT connection
def connect_mqtt():
    # Inner function to handle the event when a connection is established
    def on_connect(client, userdata, flags, rc):
        if rc == 0:  # rc == 0 indicates a successful connection
            print("Connected to MQTT Broker!")  # Print confirmation of successful connection

            # Subscribe to topics to receive incoming messages
            client.subscribe(private_sub_topic2)  # Subscribes to receive suspicious traffic notifications
            client.subscribe(private_sub_topic3)  # Subscribes to receive solutions/recommendations
        else:
            print(f"Failed to connect, return code {rc}\n")  # Prints error if connection fails with error code

    # Create an MQTT client instance with a unique client ID
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)

    # Set the username and password for MQTT broker authentication
    client.username_pw_set(username="103818400", password="103818400")  # Authenticate with the broker

    # Set the on_connect function as the handler for the connection event
    client.on_connect = on_connect

    try:
        print("Attempting to connect to the MQTT broker...")
        # Attempt to connect to the broker using its address, port, and keepalive time (60 seconds)
        client.connect("rule28.i4t.swin.edu.au", 1883, keepalive=60)
    except socket.timeout:
        # Catch timeout exception if the broker is unreachable or there's a network issue
        print("Connection attempt timed out. The broker might be unreachable or there might be network issues.")
        return None
    except socket.error as e:
        # Catch any socket-related errors (e.g., network failure) and print the error message
        print(f"Socket error occurred: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected exceptions and print the error message
        print(f"An unexpected error occurred while connecting: {e}")
        return None

    return client  # Return the client object if the connection is successful

# Function to handle incoming messages from subscribed topics
def on_message(client, userdata, msg):
    message = msg.payload.decode()  # Decode the incoming message payload from bytes to string
    print(f"Received `{message}` from `{msg.topic}` topic")  # Display the received message and the topic

    # Check if the message contains more than one comma to identify specific messages for recommendations
    if message.count(',') > 1:
        publish_recommendations(client)  # Call the function to publish recommendations

# Function to publish recommendations read from a file
def publish_recommendations(client):
    try:
        # Open the file containing recommendations in read mode
        with open(recommendations_file_path, 'r') as file:
            recommendations = file.readlines()  # Read all lines (recommendations) from the file
            
            # Iterate through each recommendation in the file
            for recommendation in recommendations:
                # Publish each recommendation to the Solutions topic, stripping any leading/trailing whitespace
                result, _ = client.publish(private_sub_topic3, recommendation.strip())
                
                # Check if the message was successfully published (result should be MQTT_ERR_SUCCESS)
                if result == mqtt.MQTT_ERR_SUCCESS:
                    print(f"Recommendation sent to topic `{private_sub_topic3}`: {recommendation.strip()}")  # Notify success
                else:
                    print(f"Failed to send recommendation to topic `{private_sub_topic3}`")  # Notify failure
                
                time.sleep(1)  # Introduce a delay between sending recommendations

            # After sending all recommendations, mark all as published
            global all_recommendations_published  # Reference the global variable
            all_recommendations_published = True  # Set the flag to True
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print(f"Error: The file '{recommendations_file_path}' was not found.")
    except IOError as e:
        # Handle any file reading issues
        print(f"Error reading the file: {e}")

# Main function to run the MQTT client
def run():
    client = connect_mqtt()  # Establish the MQTT connection using the connect_mqtt function
    if client is None:
        print("Failed to establish connection. Exiting...")  # Exit if connection was unsuccessful
        return

    client.loop_start()  # Start the MQTT client loop to process incoming/outgoing network traffic
    client.on_message = on_message  # Set the message handler for incoming messages
    
    # Publish recommendations immediately after connecting
    publish_recommendations(client)  # Call function to publish recommendations
    
    try:
        # Continue the program until all recommendations are published
        while not all_recommendations_published:
            time.sleep(1)  # Sleep to reduce CPU usage while waiting
    except KeyboardInterrupt:
        # Gracefully handle the program exit if interrupted (e.g., Ctrl+C)
        print("Program interrupted by user. Disconnecting...")
    finally:
        # Stop the MQTT client loop and disconnect from the broker
        print("Stopping MQTT loop and exiting...")
        client.loop_stop()
        client.disconnect()  # Disconnect from the MQTT broker

# Execute the MQTT client when this script is run directly
if __name__ == '__main__':
    run()  # Call the main function to start the program
