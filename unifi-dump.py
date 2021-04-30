#!/usr/bin/env python3

import time
import os
import argparse
import pprint
import unifi

parser = argparse.ArgumentParser(description='UniFi Prometheus dump')

args = parser.parse_args()

apiendpoint = os.environ.get('API_URL', 'https://localhost:8443')
apiusername = os.environ.get('API_USERNAME', 'ubnt')
apipassword = os.environ.get('API_PASSWORD', 'ubnt')

u = unifi.Network(apiendpoint, apiusername, apipassword)


# Just as a help really, code will not be reached as config.get() will blow up
if apiendpoint is None:
    raise AssertionError('API/URL is required in configuration')
if apiusername is None or apipassword is None:
    raise AssertionError('API/Username and API/Password is required in configuration')

# print controller status
status = u.api_get('status')
print("CONTROLLER STATUS: ", status.get('meta').get('rc'))
print()

pprint.pprint(u.api_get('stat/sites'))

sites = u.api_get('self/sites')
if 'data' in sites:
    print("SITES:")
    for s in sites.get('data'):
        print('\t', s.get('desc'), s.get('name'), s.get('_id'))
        print()

for site in u.sites():
    print('SITE: ' + site.name)

    print("DEVICES:")
    devices = u.api_get(site.api_endpoint('stat/device'))
    #devices = site.u.api_get(site.api_endpoint('stat/device'))
    pprint.pprint(devices)

    print("\nHEALTH:")
    for health in site.health():
        subsystem = health.pop('subsystem')
        if health.get('status') != "unknown":
            print(f"Subsystem: {subsystem}")
            pprint.pprint(health)
            print()
    
    print("STA:")
    sta = site.sta()
    pprint.pprint(sta)



exit(0)
