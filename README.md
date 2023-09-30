### Alex Ledgerwood 9/28/2023
# streaming-06-smart-smoker

#I changed my project to have a single producer and conumer, using three queues. Getting the alerts to work and dealing with nonetype errors was a huge challenge.

#I found I could get the producer and consumer working, sending and receiving to the smoker, but not food A and food B. There are three queues in RabbitMQ, so no idea why it wasn't working. !!! If this happens to you, note that there are no food temps in the csv file until 13:46:40, so these will simply show as none. After that point there will be activity in the queues for food A and B.

#Here are the three queues running on RabbitMQ
![image](https://github.com/ALedgerwood/streaming-06-smart-smoker/assets/111438988/31cf3921-9a25-4671-978b-8e50a53e58fe)

#Here are the producer and consumer running in their own terminal window, and alerts are coming through.
![image](https://github.com/ALedgerwood/streaming-06-smart-smoker/assets/111438988/d44b444c-0a00-4221-9466-97ebeebf308e)

And another where you can see info from all three queues
![image](https://github.com/ALedgerwood/streaming-06-smart-smoker/assets/111438988/94b8057a-799a-460b-956c-69a07c510077)


#Info on the project from the course site

# We want to stream information from a smart smoker. Read one value every half minute. (sleep_secs = 30)

#smoker-temps.csv has 4 columns:

#[0] Time = Date-time stamp for the sensor reading
#[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
#[2] Channel2 = Food A Temp --> send to message queue "02-food-A"
#[3] Channel3 = Food B Temp --> send to message queue "03-food-B"


#Sensors
#We have temperature sensors track temperatures and record them to generate a history 

#Streaming Data
#Our thermometer records three temperatures every thirty seconds (two readings every minute). The three #temperatures are:

#the temperature of the smoker itself.
#the temperature of the first of two foods, Food A.
#the temperature for the second of two foods, Food B.
 

#Significant Events
#We want know if:
#The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
#Any food temperature changes less than 1 degree F in 10 minutes (food stall!)
#Well this is super complicated, and it's not something the class has covered at all. So I guess ChatGPT is the place to go? 

#Smart System
#We will use Python to:

#Simulate a streaming series of temperature readings from our smart smoker and two foods. DONE
#Create a producer to send these temperature readings to RabbitMQ. DONE
#Create three consumer processes, each one monitoring one of the temperature streams. DONE
#Perform calculations to determine if a significant event has occurred.
