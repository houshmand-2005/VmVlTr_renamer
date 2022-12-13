import time
import re
import base64
import json
import binascii
from icmplib import ping

st = time.time()
print("|----------------------------------------------|")
print("| 1)change servers name                        |")
print("| 2)change servers name with ping test*        |")
print("|*If the server was dead, it will not be added |")
print("|----------------------------------------------|")
menuinput = int(input())

SERVERS = ""
with open('file location', 'r') as file:  # Specify the location of the input file
    SERVERS = file.read()
SERVERS = SERVERS.split('\n')
EDITED_SERVERS = ""


def pinger(server_ip, NUMBER):
    """Ping servers"""
    host = ping(server_ip, count=7, interval=0.2)
    if host.is_alive:
        print(f"[{NUMBER}] {host.address}, {host.avg_rtt}, And server is alive")
        return "Alive"
    else:
        print(f"[{NUMBER}] {host.address}, And server is dead")
        NUMBER -= 1
        return None


def base64_extractor(server_url, NUMBER, pingserver=True):
    """if the server url is base64 this function called"""
    extracted_date = re.sub('^[^//]*', "", server_url)
    extracted_date = extracted_date[2:]
    extracted_date = base64.b64decode(extracted_date).decode('utf-8')
    extracted_date = json.loads(extracted_date)
    if pingserver:
        if pinger(extracted_date["add"], NUMBER) is None:
            return "\n"
    # Here you type your custom name ->
    extracted_date["ps"] = f"[{NUMBER+1}] custom name"
    extracted_date = json.dumps(extracted_date).encode('ascii')
    extracted_date = base64.b64encode(extracted_date)
    extracted_date = extracted_date.decode('utf-8')
    endpr = f'{protocol}://{extracted_date}'
    return endpr+"\n"


def noramll_server_extractor(server_url, NUMBER, pingserver=True):
    """if the server url is not base64 this function called"""
    extracted_date = re.sub('^[^//]*', "", server_url)
    extracted_date = extracted_date[2:]
    server_ip = ((extracted_date.split(':'))[0]).split('@')[1]
    if pingserver:
        if pinger(server_ip, NUMBER) is None:
            return "\n"
    # Here you type your custom name ->
    names = f'#[{NUMBER+1}] custom name'
    endwithout_pr = extracted_date.split('#')[0]+names
    endpr = protocol+"://"+endwithout_pr
    return endpr+"\n"


NUMBER = 0
for server in SERVERS[:]:
    protocol = server.split(':')[0]
    try:
        if menuinput == 2:
            EDITED_SERVERS += base64_extractor(server, NUMBER)
            NUMBER += 1
        else:
            EDITED_SERVERS += base64_extractor(server,
                                               NUMBER, pingserver=False)
            NUMBER += 1
    except (UnicodeDecodeError, UnicodeEncodeError,
            json.JSONDecodeError, binascii.Error):
        if menuinput == 2:
            EDITED_SERVERS += noramll_server_extractor(server, NUMBER)
            NUMBER += 1
        else:
            EDITED_SERVERS += noramll_server_extractor(
                server, NUMBER, pingserver=False)
            NUMBER += 1

with open('file location', 'w') as file:  # Specify the location of the output file
    file.write(EDITED_SERVERS)
et = time.time()
elapsed_time = et - st
print("|----------------------------------------------|")
print("|    Auto Vmess Vless Trojan server renamer    |")
print('       Done in ', elapsed_time, 'seconds        ')
print("|                Houshmand2005                 |")
print("|----------------------------------------------|")
done = input("")
