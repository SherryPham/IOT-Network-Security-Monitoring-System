# Network Traffic Monitoring System

## Table of Contents

1. [Scripts Overview](#scripts-overview)
2. [Overall Code Function](#overall-code-function)
3. [Prerequisites and Dependencies](#prerequisites-and-dependencies)
4. [Setting Up Configuration](#setting-up-configuration)
5. [Setting Up the GUI](#setting-up-the-gui)
6. [Running the Script and Observing the Output](#running-the-script-and-observing-the-output)
7. [Interrupting Execution](#interrupting-execution)
8. [Disclaimer](#disclaimer)
9. [References](#references)

## Scripts Overview

This project contains the following Python scripts and files:

1. `Publish_Public.py`: Publishes network traffic data to a public MQTT topic for general analysis.
2. `Publish_Private.py`: Publishes network traffic data to a private MQTT topic, intended for sensitive information and actions.
3. `Private_Monitor_Client.py`: Monitors and processes incoming messages from subscribed MQTT topics, providing real-time analysis and recommendations.
4. `Local_Sample.txt`: A sample text file containing simulated network traffic data, derived from a Wireshark capture.
5. `Recommendations.txt`: Contains recommendations based on the analysis of the incoming network traffic data.
6. `README.md`: This documentation file.
7. `Output/`: A directory that includes screenshots demonstrating the functioning of the scripts.

## Overall Code Function

This set of scripts simulates a comprehensive network traffic monitoring system. The main functionality includes:

- **Data Acquisition:** The system reads and processes network traffic data from various sources.
- **MQTT Integration:** It connects to an MQTT broker, allowing for the publication and subscription of messages to specific topics.
- **Real-Time Monitoring:** As messages are published to the broker, the monitoring client subscribes to these messages, analyzes the content, and generates relevant recommendations based on predefined criteria.
- **Continuous Operation:** The system runs indefinitely until all recommendations are published, ensuring that real-time traffic analysis is consistently maintained.

## Prerequisites and Dependencies

To run this project, ensure you have the following installed on your machine:

- **Python:** The scripts are written in Python. Make sure you have Python 3.x installed.
- **Paho MQTT Client:** This library is essential for MQTT communication. You can install it using pip:

  ```bash
  pip install paho-mqtt
  ```

## Setting Up Configuration

Before running the scripts, you need to configure the MQTT broker. Use the following credentials:

- **Broker Address:** `rule28.i4t.swin.edu.au` (This is the address of the MQTT broker you will connect to)
- **Port:** `1883` (The default port for MQTT communication)
- **Username:** `103818400` (Your unique username for broker authentication)
- **Password:** `103818400` (Your password for broker authentication)

Make sure to replace these credentials with your own if necessary.

## Setting Up the GUI

The system includes a graphical user interface (GUI) that allows clients to subscribe to specific MQTT channels. The available channels are:

1. **Public:** General traffic data.
2. **103818400/Expected Traffic:** Data regarding expected network traffic patterns.
3. **103818400/Suspicious Traffic:** Alerts and notifications about suspicious activity.
4. **103818400/Solutions:** Recommendations and solutions based on the analysis.

It is recommended to subscribe to these channels first using the GUI, as this will help visualize the output of the Python scripts. This step is optional but provides a more intuitive way to observe system behavior.

## Running the Script and Observing the Output

To execute the scripts, follow these steps:

1. **Directory Structure:** Ensure that all files and scripts are stored in the same directory to avoid file not found errors.
2. **Start the Monitoring Client:**
   - Run `Private_Monitor_Client.py` first to start monitoring and processing incoming messages.
3. **Execute Data Publishers:**
   - After the monitoring client is running, execute `Publish_Public.py` and `Publish_Private.py` in any order to start publishing data.

The output generated by each script can be observed in the terminal and the GUI simultaneously, allowing for real-time tracking of network activities and responses.

## Interrupting Execution

To safely stop the script at any time, you can interrupt the execution by pressing `Ctrl + C` in the terminal where the script is running. This action will raise a keyboard interrupt, allowing the script to attempt a graceful disconnection from the MQTT broker.

## Disclaimer

Please note that the contents of the `Local_Sample.txt` file are derived from a Wireshark capture of my network. The data has been altered to fit the requirements of this project and should not be used for any real-world applications without proper analysis and consideration.
