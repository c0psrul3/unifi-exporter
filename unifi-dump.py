#!/usr/bin/env python3

import time
import os
import argparse
import pprint
from unifi import unifi

parser = argparse.ArgumentParser(description='UniFi Prometheus dump')

args = parser.parse_args()

apiendpoint = os.environ.get('API_URL', 'https://localhost:8443')
apiusername = os.environ.get('API_USERNAME', 'ubnt')
apipassword = os.environ.get('API_PASSWORD', 'ubnt')

unifi = unifi.UniFi(apiendpoint, apiusername, apipassword)


# Just as a help really, code will not be reached as config.get() will blow up
if apiendpoint is None:
    raise AssertionError('API/URL is required in configuration')
if apiusername is None or apipassword is None:
    raise AssertionError('API/Username and API/Password is required in configuration')

print("SITES:")
sites = unifi.api_get('self/sites')
pprint.pprint(sites)

for site in unifi.sites():
    print('SITE: ' + site.name)

    print("DEVICES:")
    devices = site.unifi.api_get(site.api_endpoint('stat/device'))
    pprint.pprint(devices)

print("STA:")
sta = site.sta()
pprint.pprint(sta)
exit(0)
