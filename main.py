import time

import discoverhue
import phue


def get_bridge():
    bridges = discoverhue.find_bridges()
    url = list(bridges.values())[0]
    ip = url.split(":")[1].strip("/")

    while True:
        try:
            return phue.Bridge(ip)
        except phue.PhueRegistrationException:
            print("Press the button on the bridge")
            time.sleep(2)

print(get_bridge())