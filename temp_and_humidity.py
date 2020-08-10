###################################################################################
#
# @Project: Real time temperator and humidity monitoring and uploading to cloud
# @Description: uses Raspberry Pi 4, DHT22 sensor, AWS DynamoDB
# @Author: Jianwei Cui
# @LastUpdate: Aug 10 2020
#
####################################################################################

import Adafruit_DHT
import time
import threading
import boto3
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('temp_and_humidity')

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def sample_and_upload():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        timestamp =  time.time()
        now = datetime.now().time() 
        print("now =", now)
        try:
            table.put_item(
                Item={
                    'timestamp': Decimal(str(timestamp)),
                    'temp': Decimal(str(temperature)),
                    'humidity': Decimal(str(humidity))
                }
            )
            print("Data uploaded")
        except:
            print("Failed to upload data to cloud")
        print("Time: {0:f}, Temp={1:0.1f}*C  Humidity={2:0.1f}%".format(timestamp, temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")

WAIT_TIME_SECONDS = 60

ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    sample_and_upload()
