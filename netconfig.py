from requests import get, Session
from sys import argv
from bs4 import BeautifulSoup
from re import compile, findall
from termcolor import colored
from os import system
from json import loads

system("color")

with open("C:/Users/Jaka/Documents/Programming/Python/netconfig/config.json", "r") as f:
    cfg = loads(f.read())

if len(argv) not in [2, 3]:
    print(f"{colored('Error:', 'red')} Invalid format -> netconfig /?")
    exit()
elif argv[1] not in ["block", "unblock", "list", "/?"]:
    print(f"{colored('Error:', 'red')} Invalid parameters -> netconfig /?")
    exit()
    
GATEWAY= "http://192.168.0.1"
if len(argv) == 3:
    match argv[1]:
        case "block":
            ACTION = "1"
        case "unblock":
            ACTION = "2"
    MAC = argv[2]
else:
    ACTION = argv[1]

mac_re = compile(r'(?:[0-9a-fA-F]:?){12}')
def getBlocked():	
    blocked = BeautifulSoup(get(f"{GATEWAY}/UbeeAdvancedMacFiltering.asp").text, "html.parser").find("option")
    return findall(mac_re, str(blocked))

blocked = getBlocked()
    
login_data = {
    "loginUsername": cfg["loginUsername"],
    "loginPassword": cfg["loginPassword"]
}

s = Session()
s.post(f"{GATEWAY}/goform/login", data = login_data)

def blockMAC():
    global blocked
    if MAC.lower() not in blocked:	
        macFiltering_data = {
            "MacFilterAction": ACTION,
            "NewMacFilter": MAC
        }

        s.post(f"{GATEWAY}/goform/UbeeAdvancedMacFiltering", data = macFiltering_data)
        print(f"{colored('Success:', 'green')} Blocked internet traffic to {MAC}\n")
        blocked = getBlocked()

        print("Current blocked entries:")
        [print(f"  {mac}") for mac in blocked] if len(blocked) != 0 else print("  None")
    else:
        print(f"{colored('Error:', 'red')} {MAC} is already blocked")

def unblockMAC():
    global blocked
    if MAC.lower() in blocked:	
        macFiltering_data = {
            "MacFilterList": blocked.index(MAC.lower()),
            "MacFilterAction": ACTION,
            "NewMacFilter": None
        }	
        
        s.post(f"{GATEWAY}/goform/UbeeAdvancedMacFiltering", data = macFiltering_data)
        print(f"{colored('Success:', 'green')} Unblocked internet traffic to {MAC}\n")
        blocked = getBlocked()
        
        print("Current blocked entries:")
        [print(f"  {mac}") for mac in blocked] if len(blocked) != 0 else print("  None")
    else:
        print(f"{colored('Error:', 'red')} {MAC} is already unblocked")

def listDevices():
    ipv4_re = compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    
    site = s.get(f"{GATEWAY}/UbeeAdvConnectedDevicesList.asp").text
    soup = BeautifulSoup(site, "html.parser")
    html_code = soup.find_all("table", {"style": "font-family: Helvetica;font-size:14"})
    mac_addresses = findall(mac_re, str(html_code))
    ipv4_addresses = findall(ipv4_re, str(html_code))

    print(f"Interface: 192.168.0.1\n")
    print("  Internet address      Physical address")
    [print(f"  {ip}          {mac.lower()}") for ip, mac in zip(ipv4_addresses, mac_addresses)]
        
def displayHelp():
    with open("C:/Users/Jaka/Documents/Programming/Python/netconfig/help.txt", "r") as f:
        print(f.read())
    
match ACTION:	
    case "1":	
        blockMAC()
    case "2":
        unblockMAC()
    case "list":
        listDevices()
    case "/?":
        displayHelp()
