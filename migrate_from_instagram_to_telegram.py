# this script will upload all Instagram photos to telegram
# 1. request your archive from Instagram https://www.instagram.com/download/request/ . Choose JSON option!
# 2. wait for the mail with the link. download your archive and unpack
# 3. create a private TG channel, create a group. Go to channel propertries and add the group
# 4. copy channel join link
# 5. find this TG bot: @username_to_id_bot. Paste the link and get channel's CHAT_ID
# 6. (optional) goto channel properties and remove & creat new join link
# 7. copy both posts and stories into the same foled
# 8. copy content of content/post_1.json file
# 9. open CyberShef, paste the text and apply filters: Unescape Unicode Char AND Decode text - UTF-8
# 10. copy result text back to file posts.json
# 11. start the script

import requests, json, pathlib, os, datetime, time

# below thing is only needed if you want to intercept the traffic using Burp suite (to see what's happening)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# if you remove this - also remove "proxies=PROXIES, verify=False" from the requests below


TOKEN =  ""
CHAT_ID = "-1001337200670" 
INSTA_POST_DIR = "c:\\Temp\\i\\posts\\"
INSTA_CAPTION_FILE = "c:\\Temp\\i\\posts.json"

PROXIES = {"https" : "localhost:8080"}

def main():
    titles = ""
    i = 0
    j = 0
    files = []

    for dirpath, dirnames, filenames in os.walk(INSTA_POST_DIR):
        for f in filenames:
            uri = "media/posts/" + dirpath[-6:] + "/" + f
            title = getTitle(uri, INSTA_CAPTION_FILE)
            if title:
                titles += title + "\n"
            if len(titles) > 1001:
                titles = titles[:1000]
            
            with open(dirpath + "\\" + f, 'rb') as f:
                mediafile = []
                mediafile.append(f.read())
                mediafile.append(pathlib.Path(f.name).suffix)

            files.append(mediafile)

            i += 1
            j += 1
            if i == 10:
                while True:
                    r = sendMediaGroup(titles, files)
                    if r:
                        print(f"{datetime.datetime.now():%H-%M-%S}" + " - [i] " + str(j) + "/" + str(len(filenames)) + " files sent")
                        break
                i = 0
                files = []
                titles = ""
    if i > 0:
        while True:
            r = sendMediaGroup(titles, files)
            if r:
                break


def getTitle(uri, postsfile):
    with open(postsfile, encoding='utf8') as f:
        posts = json.load(f)

    for i in posts:
        u = json.dumps(i['media'][0]['uri']).replace('"',"")
        if  u == uri:
            epochtime = i['media'][0]['creation_timestamp']
            title = i['media'][0]['title']
            dtime = datetime.datetime.fromtimestamp(epochtime).strftime("%Y/%m/%d")
            return "[" + dtime + "] " + title

def readposts(postsfile):
    with open(postsfile, encoding='utf8') as f:
        return json.load(f)

def sendtext(bot_message, token=TOKEN, chat_id=CHAT_ID):
    
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={bot_message}"
    return requests.get(url)

def sendPhotoURL(caption, photourl, token=TOKEN, chat_id=CHAT_ID):
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={caption}&photo={photo}"
    return requests.get(url)

def sendPhotoFile(caption, photofile, token=TOKEN, chat_id=CHAT_ID):
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={caption}" 
    return requests.post(url, files = {"photo": photofile})

def sendMediaGroup(caption, mediafiles, token=TOKEN, chat_id=CHAT_ID):
    params = {
    'chat_id': chat_id,
    'media': [],
    }
    files = {}
    mediatype = "photo"

    for i in list(range(len(mediafiles))):
        if mediafiles[i][1] == ".mp4":
            mediatype = "video"
        elif mediafiles[i][1] == ".jpg":
           mediatype = "photo"
        if i == 0:
            params['media'].append({'type': mediatype, 'caption' : caption, 'media': "attach://file0"})
        else:
            params['media'].append({'type': mediatype, 'media': f"attach://file{i}"})
        files[f"file{i}"] = mediafiles[i][0]

    params['media'] = json.dumps(params['media'])
    
    url = f"https://api.telegram.org/bot{token}/sendMediaGroup" 

    r = requests.post(url, data=params, files = files, proxies=PROXIES, verify=False)

    try: 
        reply = json.loads(r.text)
        if "error_code" in reply:
            print(f"{datetime.datetime.now():%H-%M-%S}" + " - [i] Reply[error_code]: " + str(reply["error_code"]))

        if reply["ok"] == True:
            return True

        else:
            print(f"{datetime.datetime.now():%H-%M-%S}" + " - [!] Server error! " + reply["description"])
            if "error_code" in reply:
                if reply["error_code"] == 429:
                    retry = reply["parameters"]["retry_after"]
                    print(f"{datetime.datetime.now():%H-%M-%S}" + " - [i] Too many requests. Retrying in " + str(retry) + " seconds")
                    time.sleep(reply["parameters"]["retry_after"])
                else:
                    print(f"{datetime.datetime.now():%H-%M-%S}" + " - [i] Retrying in 60 seconds.")
                    time.sleep(60)

    except Exception as exception:
        print(f"{datetime.datetime.now():%H-%M-%S}" + " - [!] Error parsing server's reply. " + "Exception message: {}".format(exception))

    return False

if __name__ == "__main__":
    main()