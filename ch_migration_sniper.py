#!/usr/bin/env python
# """Module docstring."""

# This script is used to monitor for an open slot on CH Migration  website. 
# How to use:
# 1. Pick a first available date manually 
# 2. Create a file ch_migration_sniper.txt and add that date to a file in format YYYY-MM-DD. Example - 2022-10-18
# 3. set the proper location (399 == Luzern)
# 4. schedule this script to run every 5 min
# 5. add your telegram chat ID and token
# 6. if script will find a slot - it will send you a message with a link. Use the link to register yourself

# Imports
import os
import sys
import requests
import json
import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Module Constants
START_MESSAGE = "CH edoc slot monitoring script"
URL = "https://www.ch-edoc-reservation.admin.ch"
ID = "123qwe" #login from paper email
location_code = "399" #depends on the canton

TELEGRAM_CHAT_ID = <your chat ID>
TELEGRAM_TOKEN = "your token"
CONFIG_FILE = "/path/to/ch_migration_sniper.txt"

# Module "Global" Variables
location = os.path.abspath(__file__)
today = datetime.datetime.today().strftime("%Y-%m-%d")


# Module Functions and Classes
def main(*args):
    """My main script function.
    Displays the full patch to this script, and a list of the arguments passed
    to the script.
    """
    print(START_MESSAGE)
    print("Script Location:", location)
    print("Arguments Passed:", args)
    
    # step 0 - read current app date
    with open(CONFIG_FILE, 'r') as f:
        current_appointment_date = f.read().rstrip('\n')
    #print(current_appointment_date)
#    current_appointment_date = "2023-05-31"

    # step 1 - get the data
    headers = {
        'Host': 'www.ch-edoc-reservation.admin.ch',
        'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36',
        'Token': ID,
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'close',
    }

    params = {
        'dateFrom': today,
        'dateTo': current_appointment_date,
        'excludedApptIds': '4664285',
    }

    response = requests.get(
        f'https://www.ch-edoc-reservation.admin.ch/rest/public/appointment/calendar/location/{location_code}/ZEMIS',
        params=params,
        headers=headers,
        verify=False,
    )

    json_obj = response.json()

    #print(json.dumps(json_obj, indent=4))

    # step X - iterate through the response
    for i in json_obj:
        if i["freeCapacity"] != 0:
            if i["date"] != "2023-05-19":  #you can add some exceptions date here
                new_date = i["date"]
                time_available = ""
                for j in i["slots"]:
                    if j["freeCapacity"] != 0:
                        time_available = j["timeFrom"]
                print("[+] New slot available: ", new_date, " Time:", time_available)
                send_telegram_message(f"New slot available: {new_date}. Time: {time_available}. Book here: {URL}")
                with open(CONFIG_FILE, 'w') as f:
                   f.write(new_date)

def send_telegram_message(bot_message, token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID):
    
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={bot_message}"
    response = requests.get(url)

    return response.json()


# Check to see if this file is the "__main__" script being executed
if __name__ == '__main__':
    _, *script_args = sys.argv
    main(*script_args)
