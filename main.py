import time
from pathlib import Path

import discoverhue
import phue


def find_ip():
    bridges = discoverhue.find_bridges()
    url = list(bridges.values())[0]
    return url.split(":")[1].strip("/")


def get_ip():
    ip_file_path = Path.home() / ".ip.txt"
    if ip_file_path.exists():
        return ip_file_path.read_text()
    else:
        ip = find_ip()
        ip_file_path.write_text(ip)
        return ip


def get_bridge():
    while True:
        try:
            return phue.Bridge(get_ip())
        except phue.PhueRegistrationException:
            print("Press the button on the bridge")
            time.sleep(2)

print(get_bridge())