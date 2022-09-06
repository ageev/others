#!/usr/bin/env python
# """Module docstring."""

# This script is used to monitor for an open slot on IND website. 
# How to use:
# 1. Pick a first available date manually 
# 2. Create a file IND_sniper.txt and add that date to a file in format YYYY-MM-DD. Example - 2022-10-18
# 3. set the proper location (DB == Den Bosch) and proper ammount of people
# 4. schedule this script to run every 15 min
# 5. add your telegram chat ID and token
# 6. if script will find a slot - it will send you a message with a link. Use the link to register yourself

# Imports
import os
import sys
import requests
import json
import datetime


# Module Constants
START_MESSAGE = "IND monitoring script"

URL = "https://oap.ind.nl/oap/nl/#/doc" # this URL is for docs
#URL = "https://oap.ind.nl/oap/nl/#/BIO" # this URL is for biometry

SERVICE = "doc"  # to get documents use 'doc', for biometry use "BIO"
NUMBER_OF_PEOPLE = 2
IND_LOCATION = "DB"

TELEGRAM_CHAT_ID = YOUR_CHAT_ID
TELEGRAM_TOKEN = YOUR_TOKEN
URL = f'https://oap.ind.nl/oap/api/desks/{IND_LOCATION}/slots/?productKey={SERVICE}&persons={NUMBER_OF_PEOPLE}'
CONFIG_FILE = "/PATH/TO/IND_sniper.txt"

# Module "Global" Variables
location = os.path.abspath(__file__)


# Module Functions and Classes
def main(*args):
    """My main script function.

    Displays the full patch to this script, and a list of the arguments passed
    to the script.
    """
    print(START_MESSAGE)
    print("Script Location:", location)
    print("Arguments Passed:", args)

    # step 1 - get the data

    r = requests.get(URL)
    rd = json.loads(r.text[5:])
    earliest_date_available = rd["data"][0]['date']
    print("Earliest date available: ", earliest_date_available)

    # step 2 - read current app date
    with open(CONFIG_FILE, 'r') as f:
        current_appointment_date = f.read()

    print("Current appointment date: ", current_appointment_date)

    # step 3 - compare and sent TG message
    result = compare_IND_dates(current_appointment_date, earliest_date_available)
    if result:
        send_telegram_message(f"New slot(s) avaialble for {SERVICE} for {NUMBER_OF_PEOPLE} persons: {earliest_date_available} Book here: {URL}")
        with open(CONFIG_FILE, 'w') as f:
            f.write(earliest_date_available)

def compare_IND_dates(a, b):
    current_date = datetime.datetime.strptime(a, "%Y-%m-%d").date()
    new_date = datetime.datetime.strptime(b, "%Y-%m-%d").date()
    if new_date < current_date:
        print("bingo!")
        return True
    return False

def send_telegram_message(bot_message, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID):
    
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={bot_message}"
    response = requests.get(url)

    return response.json()


# Check to see if this file is the "__main__" script being executed
if __name__ == '__main__':
    _, *script_args = sys.argv
    main(*script_args)
