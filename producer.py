"""
    This program sends a message to a queue on the RabbitMQ server every 30 seconds.
    The timestamps of temps are sent to queues based on temp of the smoker, Food A, or Food B.
    Messages come from the csv file of smoker temps.
    I've corrected this file from the version I wrote from Mod 5, because it did not include 3 queues as needed.
    
    Author: Alex Ledgerwood
    Date: September 27, 2023

"""

import pika
import sys
import webbrowser
import csv
import time
import logging


# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Declare program constants
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
SMOKER_FILE_NAME = "smoker-temps.csv"
SHOW_OFFER = True  # Control whether to show the RabbitMQ Admin webpage offer

def admin():
    """Offer to open the RabbitMQ Admin website"""
    global SHOW_OFFER
    if SHOW_OFFER:
        webbrowser.open_new("http://localhost:15672/#/queues")

def send_message(channel, queue_name, timestamp, temperature):
    """Send a message to the specified queue.
    Display a message regarding what queue was accessed, what time the temp was recorded, and what the temp was.
    
    Parameters (all fed in from the main() function):
        channel
        queue_name
        timestamp
        temperature
    """
def send_message(channel, queue_name, timestamp, temperature):
    if temperature is not None:  # Check if temperature is not None
        channel.basic_publish(exchange="", routing_key=queue_name, body=f"{timestamp},{temperature}")
        logging.info(f"Sent to {queue_name} Queue: Timestamp={timestamp}, Temperature={temperature}")

def main():
    """
    Delete existing queues.
    Declare new queues.
    Read from csv file.
    Send messages to queue based on which column is being read from the csv.
    This process runs and finishes.
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(HOST))
        # use the connection to create a communication channel
        ch = conn.channel()
        # Delete the queues if they exist
        ch.queue_delete(queue="01-smoker")
        ch.queue_delete(queue="02-food-A")
        ch.queue_delete(queue="03-food-B")
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue="01-smoker", durable=True)
        ch.queue_declare(queue="02-food-A", durable=True)
        ch.queue_declare(queue="03-food-B", durable=True)
        
        # open and read the csv file
        with open(SMOKER_FILE_NAME, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row if it exists

                # iterate over each row in the csv and assign the values in each column of that row to a variable
                for row in reader:
                    timestamp = row[0]
                    smoker_temp = float(row[1]) if row [1] else None # Handle empty string
                    food_a_temp = float(row[2]) if row [2] else None # Handle empty string
                    food_b_temp = float(row[3]) if row [3] else None # Handle empty string

                    # Send messages to 3 different RabbitMQ queues using the send_message function referenced above
                    # messages sent to different queues based on which variable is being referenced
                    send_message(ch, "01-smoker", timestamp, smoker_temp)
                    send_message(ch, "02-food-A", timestamp, food_a_temp)
                    send_message(ch, "03-food-B", timestamp, food_b_temp)

                    # Wait for 30 seconds before processing the next batch of records
                    time.sleep(30)
                    # print a message to the console for the user
                    logging.info(f"Sent: Timestamp={timestamp}, Smoker Temp={smoker_temp}, Food A Temp={food_a_temp}, Food B Temp={food_b_temp}")
                    # print a reminder about how to cancel the program's run
                    logging.info("------------------------------------------------Type CTRL+C to cancel the programs run---------------------------------------------------")
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()



# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # open the RabbitMQ Admin site
    admin()

    #call the custom function to read and send data from csv
    main()