## Importing required libraries
import mysql.connector
import pandas as pd
from redis import Redis
from rq import Connection, Queue, Retry
import requests
import time
from datetime import datetime, timedelta
from client import retry_handler, send_sms_via_api

## Setup a connection to redis server
redis_conn = Redis(host='localhost', port=6379, db=0)
## Creating a queue for managing tasks
task_queue = Queue("sms_queue", connection = redis_conn, exc_handler = retry_handler)

## Connecting to MySQL Server
# connection = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='****',
#     database='satsangdb'
# )

## fetch the data from database and store it in a DataFrame
# query = "SELECT Member_Name, Contact_No FROM Member_data"
# df = pd.read_sql_query(query, connection)
# print(df)

## Read data from a excel file
# df  = pd.read_excel('/mnt/c/Python_WSL/Test.xlsx')
# df.columns = ['Contact_No', 'Member_Name', 'c3']
# df.drop(columns=['c3'], inplace = True)
# df = df.loc[:, ['Member_Name', 'Contact_No']]
# print(df.head())

## Read data from a csv file
# df = pd.read_csv('/mnt/c/Python_WSL/FW_WB_JUNE_DATA.csv')
# df.drop(columns = ['mem_guardian_name', 'mem_ritwiki_name', 'fw_updated_by', 'mem_address_permanent', 'mem_perm_pin'], inplace = True)
# df = df.loc[:, ['mem_full_name', 'mem_key']]
# print(df.head())


        

## Function to push contact_details to Redis Queue in batches
def push_to_redis_queue(contact_details, batch_size = 200):
    
    # print("Inside the function but outside the loop")
    for i in range(0, len(contact_details), batch_size):
        batch = contact_details.iloc[i:i+batch_size]
        delta = 0
        # print("Inside the first loop")
        for index, row in batch.iterrows():
            name = row['mem_full_name']
            mobile_number = row['mem_key']
            # print("Inside the 2nd loop")
            
            ## Enqueue a task to send an SMS using the extracted name , mobile number and do the task by calling the API using 
            ## send_sms_via_api function in the client.py program
            task_queue.enqueue(send_sms_via_api, 
                                  name, 
                                  mobile_number, 
                                  "Your message here",
                                  retry = Retry(max=3, interval = [10, 20, 40])
                                  )
            
            
        while not task_queue.is_empty():
            time.sleep(2)

push_to_redis_queue(df)





