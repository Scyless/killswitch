#''            The killswitch            '''#
#'''Created on Aug 17, 2019'''#
#'''@author: scy'''#

import time
import os
import urllib.request
import psutil    
from datetime import datetime
import easyufw as ufw
from playsound import playsound

#'''Start the client'''#
ovpn = "openvpn" in (p.name() for p in psutil.process_iter())
def client():
    if ovpn and 'Status: active' in ufw.status():
        os.system('sudo -H -u scy bash -c "/usr/bin/qbittorrent" >&/dev/null &')
    else:
        print('Something isn\'t right. Nuke it three times.')
        nuke()
        return

#'''Absolutely nuke the shit out of the client'''#
def nuke():
    
    os.system('killall qbittorrent & sudo killall qbittorrent >&/dev/null &')
    os.system('pkill -9 qbittorrent & sudo pkill -9 qbittorrent >&/dev/null &')
    os.system('pgrep qbittorrent | xargs kill -9 & pgrep qbittorrent | sudo xargs kill -9 >&/dev/null &')

#'''Check our IP address'''#
def check():
    
    ipaddr = (urllib.request.urlopen('https://ident.me').read().decode('utf8'))
    ip = ('213.152.162.89')
    
    if ip in ipaddr:
        print(datetime.now().strftime('%H:%M:%S') + ' No leak.')
        return


client()


#''' Shield 1'''#
while True:
    time.sleep(0.5)
    try:
        check()
    except:
        nuke()
        os.system('notify-send "IP address leaked, nuking."')
        print(datetime.now().strftime('%H:%M:%S') + ' IP address leaked, nuking.')
        playsound('./gib.mp3')
        break
    
#'''Shield 2'''#
    ovpn = "openvpn" in (p.name() for p in psutil.process_iter())
    try:
        if ovpn and 'Status: active' in ufw.status():
            print(datetime.now().strftime('%H:%M:%S') +  ' OVPN & UFW running.')
        elif ovpn is 0 or'Status: inactive' in ufw.status():
            nuke()
            os.system('notify-send "Firewall or VPN failed, nuking."')
            print(datetime.now().strftime('%H:%M:%S') + ' Firewall or VPN failed, nuking.')
            playsound('./gib.mp3')
            break
    except (ValueError) as err:
        print(datetime.now().strftime('%H:%M:%S ') + err)
        playsound('./gib.mp3')

        nuke()