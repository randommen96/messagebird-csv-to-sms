#!/usr/bin/env python

# script to mass text numbers from CSV data
# d.dernederlanden

# import modules needed
import messagebird
import csv
from os import getenv
from dotenv import load_dotenv

# define variables
load_dotenv()
ACCESS_KEY=getenv('ACCESS_KEY')
message_content=getenv('message_content')
message_sender=getenv('message_sender')
message_reference=getenv('message_reference')
csv_filename=getenv('csv_filename')
result_filename=getenv('result_filename')
message_receiver = "31XXXXXXXXX"

# open result file and truncate it
try:
    open(result_filename, 'w').close()
except IOError:
    print('failure opening resultfile')

# open csv file and fill list with numbers
csvfile = open(csv_filename)
csvreader = csv.reader(csvfile)

# skip header and define empty lists
header = next(csvreader)
receivers = []
numbers = []

#fill lists
for person in csvreader:
    receivers.append(person)
for item in receivers:
    numbers.append(item[1])

# function to send text
def sendtext(message_sender, message_receiver, message_content):
    try:
        client = messagebird.Client(ACCESS_KEY)
        message = client.message_create(
                message_sender,
                message_receiver,
                message_content,
                { 'reference' : message_reference }
          )

        # verify if message is actually sent, otherwise print reason why not  
        status = message._recipients['items'][0].__dict__['status'] 
        if status == 'sent':
            return 'ok;' + status + ';' + message_receiver
        else:
            return status + ';' + message_receiver

# catch errors while sendig texts and print them
    except messagebird.client.ErrorException as e:
        for error in e.errors: 
            return 'failed;' + error.__dict__['description'] + ';' + message_receiver

# loop to send text to all numbers in list
for message_receiver in numbers:
    sendresult = sendtext(message_sender, message_receiver, message_content)
    with open(result_filename, 'a') as f:
        f.write(sendresult + '\n')
