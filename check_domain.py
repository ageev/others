# Domain availability check tool for Gandi API v2.1
# https://api.gandi.net/docs/domains/
# curl -X GET 'https://api.gandi.net/v5/domain/check?name=z32.nl' -H 'authorization: Apikey <key>'

import requests, json, logging, os, time
from datetime import datetime
from multiprocessing import Queue
from multiprocessing.dummy import Pool as ThreadPool
from sys import argv

INPUT_FILE = argv[1]
ZONE = ""
ZONE = argv[2]
OUTPUT_FILE = INPUT_FILE + ".output"
LOG_NAME = INPUT_FILE + ".log"
CHECKED_FILE = INPUT_FILE + ".checked"
FAILED_FILE = INPUT_FILE + ".failed"
THREADS = 20

api_url = 'https://api.gandi.net/v5/domain/check?name='
token = "key"

# LOGGER INIT
logging.basicConfig(
    format='%(asctime)s %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.ERROR, #change to INFO for more details
    handlers=[
        logging.FileHandler(LOG_NAME),
        logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)
logger.info('Script started')

with open(INPUT_FILE, 'r') as f:
    list_of_all_domains = [(line.rstrip()+ZONE) for line in f]

found = 0
checked = 0
failed = 0
total = len(list_of_all_domains)
last_time = time.time()

def main():
    pool = ThreadPool(THREADS)
    results = pool.map(task, list_of_all_domains)
    pool.close()
    pool.join()

def task(domain):
    global found, checked, failed
    checked += 1
    response = check_name(domain)
    if response[0] == "Available":
        found += 1
        print("[+] " + str(datetime.now()) + " "  + domain + " is AVAILABLE. " + str(total) + '/' + str(checked) + '/' + str(found))
        with open(OUTPUT_FILE, 'a') as f:
            f.write(domain + ";" + response[1] + '\n')
    elif response[0] == "Error":
        failed += 1
        print("[!] " + str(datetime.now()) + " " + domain + " ERROR: " + response[1] + str(total) + '/' + str(checked) + '/' + str(found))
        logger.error(" Name: " + domain + " " + response[1])
        with open(FAILED_FILE, 'a') as f:
            f.write(domain + '\n')
    else:
        print("[-] " + str(datetime.now()) + " " + domain + " is unavailable " + str(total) + '/' + str(checked) + '/' + str(found))
    
    save2file(domain, CHECKED_FILE)

def check_name(name):
    url = api_url + name
    headers = {'authorization': 'Apikey ' + token, 'Content-Type' : 'application/json'}
    try:
        response = requests.get(url, headers = headers)
    except Exception as e:
        return ["Error", "NetError: " + repr(e)]

    try:
        r = response.json()
    except Exception as e:
        return ["Error", "JSONError: " + repr(e)]

    if "products" in r:
        if r["products"][0]["status"] == "available":
            return ["Available", str(r['products'][0]['prices'][0]['price_after_taxes'])]   
        else:
            return ["Unavailable", ""]
    return ["Error", "LogicError "] 

def save2file(content, file="output.txt"):
    with open(file, 'a') as f:
        f.write(content + '\n')

if __name__ == "__main__":
    main()
