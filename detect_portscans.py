'''
You have several dozen computers that centrally log outbound netflow sockets to "netflow.txt".
You want to alert yourself if any of your devices  start port scanning, as that could indicate compromise. 
The central log file is of this format: "saddr:port -> daddr:port"
Write a script that prints out Source IPs that have connected to >=3 unique ports of a Dest IP

For example:
192.168.42.1:1337 -> 216.58.195.236:22
192.168.42.1:1234 -> 216.58.195.237:22
192.168.42.1:5555 -> 216.58.195.238:22
Should have no output
192.168.42.1:1234 -> 216.58.195.236:22
192.168.42.1:1337 -> 216.58.195.237:23
192.168.42.1:5555 -> 216.58.195.238:24
Should have no output
192.168.42.2:5555 -> 216.58.195.238:22
192.168.42.2:1337 -> 216.58.195.238:80
192.168.42.2:1234 -> 216.58.195.238:443 '''

log = ['192.168.42.2:1337 -> 216.58.195.238:22', '192.168.42.3:1337 -> 216.58.195.238:80', '192.168.42.2:1234 -> 216.58.195.238:443', '192.168.42.1:1337 -> 216.58.195.236:22',
        '192.168.42.1:1234 -> 216.58.195.230:22', '192.168.42.2:1337 -> 216.58.195.238:80', '192.168.42.2:1337 -> 216.58.195.238:22', '1.1.1.1:1 -> 2.2.2.2:1', '1.1.1.1:2 -> 2.2.2.2:2', '1.1.1.1:3 -> 2.2.2.2:3' ]

def build_list(l):
    result = []
    for _ in l:
        src_ip = _.split(":")[0]
        dst_port = _.split(":")[2]
        dst_ip = _.split(" ")[2].split(":")[0]

        result.append(src_ip + '>' + dst_ip + ':' + dst_port)
    return result

ip_list = build_list(log)
#print(ip_list)

ip_list_sorted_no_dups = list(dict.fromkeys(sorted(ip_list)))
#print(ip_list_sorted_no_dups)

for _ in range(len(ip_list_sorted_no_dups)):
    try:
        if (ip_list_sorted_no_dups[_].split(':')[0] == ip_list_sorted_no_dups[_+1].split(':')[0]) and \
            (ip_list_sorted_no_dups[_].split(':')[0] == ip_list_sorted_no_dups[_+2].split(':')[0]):
                print('Found:' + ip_list_sorted_no_dups[_].split('>')[0])
    except:
        pass