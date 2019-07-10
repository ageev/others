import subprocess
import json
import requests
import time

args = ["powershell.exe", "-Command", r"-"]
filename = "c:\\users.csv"
output = []
output_filename = "c:\\users_details.csv"

def main():

    names = (line.rstrip("\n") for line in open(filename))
    print("Opening file")

    for name in names:
        name = "'" + name + "'"
        output.append(name + ";" + get_samname(name) + ";" + get_enabled(name) + ";" + get_email(name) + ";" + ";".join(get_CI(name)))

    with open(output_filename, 'w') as of:
        of.write("\n".join(output))

def get_samname(name):
    process = subprocess.Popen(args, stdin = subprocess.PIPE, stdout =   subprocess.PIPE)
    cmdlet = str.encode("Get-ADUser -Filter{displayName -like " + name + "} | select -ExpandProperty SamAccountName\r\n")
    process.stdin.write(cmdlet)
    samname = process.communicate()[0].decode("utf-8").replace("\r\n", "")

    print(samname)

    return samname

def get_enabled(name):
    process = subprocess.Popen(args, stdin = subprocess.PIPE, stdout =   subprocess.PIPE)
    cmdlet = str.encode("Get-ADUser -Filter{displayName -like " + name + "} | select -ExpandProperty Enabled\r\n")
    process.stdin.write(cmdlet)
    enabled = process.communicate()[0].decode("utf-8").replace("\r\n", "")
    return enabled

def get_email(name):
    process = subprocess.Popen(args, stdin = subprocess.PIPE, stdout =   subprocess.PIPE)
    cmdlet = str.encode("Get-ADUser -Filter{displayName -like " + name + "} -Properties EmailAddress | select -ExpandProperty EmailAddress\r\n")
    process.stdin.write(cmdlet)
    email = process.communicate()[0].decode("utf-8").replace("\r\n", "")

    print(email)

    return email

def get_CI(name):
    ci_id = []
    ITRP_URL = 'https://api.itrp.com/v1/'
    API_TOKEN = 'tokenshmoken'
    HEADERS = {'X-ITRP-Account' : '<company>', 'Content-Type' : 'application/json'}
    time.sleep(0.7)
    r = requests.get(ITRP_URL + "people" + "?api_token=" + API_TOKEN + "&name=" + name.strip("'"), 
        headers = HEADERS)
    try:
        user_id = r.json()[0][u'id']
    except:
        pass
    try:
        r = requests.get(ITRP_URL + "people/" + str(user_id) + "/cis" + "?api_token=" + API_TOKEN, 
            headers = HEADERS)
    except:
        pass

    try:
        for i in r.json():
            ci_id.append(i[u'label'])
    except:
        pass
    print(ci_id)

    return ci_id

main()