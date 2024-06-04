import os
import sys
sys.path.append('../')
from send_bot import send_messages
import netifaces
from time import sleep
from pathlib import Path
from datetime import datetime

INTERFACE = 'eno1'
IP_LOG = Path(os.path.abspath(__file__)).parent / 'ip_log'

def check_ip(interface):
    addresses = netifaces.ifaddresses(interface)
    ip_address = addresses[netifaces.AF_INET][0]['addr']
    return ip_address


def get_before_ip():
    ip_logs = sorted(list(IP_LOG.glob("*.txt")))
    if len(ip_logs) > 0:
        with open(ip_logs[-1], 'r') as f:
            ip_address = f.read()
    else:
        ip_address = ""
    return ip_address


def main():
    while True:
        ip_address = check_ip(INTERFACE)
        ip_address_bf = get_before_ip()
        now = datetime.now()
        dt = now.strftime('%Y%m%d-%H%M%S')
        if ip_address != ip_address_bf:

            messages  = f"{dt}:\n {INTERFACE}のIPアドレスが変更されました。"
            messages += f"\n変更前: {ip_address_bf}\n変更後: {ip_address}"
            messages += f"\ndjangoアプリの新アドレス http://{ip_address}:8887/samplesite/main/"
            send_messages(messages)
            print(messages)
            with open(IP_LOG / f'ip_address_{dt}.txt', 'w') as f:
                f.write(ip_address)
        else:
            print(f"{dt}: IPアドレスは変更されていません。{ip_address}")
        sleep(10)



    # message = "こんにちは"
    # send_messages(message)

if __name__ == '__main__':
    main()
