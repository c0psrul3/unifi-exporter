#!/usr/bin/env python3

import time
import os
import argparse
import pprint
import json
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
if status.get('meta').get('rc') != 'ok':
    print("CONTROLLER STATUS: ", status.get('meta').get('rc'))

sites = u.api_get('self/sites')
if 'data' in sites:
    #print("SITES:")
    #for s in sites.get('data'):
    #    print('\t', s.get('desc'), s.get('name'), s.get('_id'))
    #    print()

    for site in u.sites():
        #pprint.pprint(site)
        #print('SITE: ' + site.name)
        #print("\n")
        #print("DEVICES:")
        devices = u.api_get(site.api_endpoint('stat/device'))
        #devices = site.u.api_get(site.api_endpoint('stat/device'))
        print(json.dumps(devices['data']))
        #for d in devices.get('data'):
        #    if d.get('model') == "USMINI":
        #        print("** Device: *********************************************")
        #        print("  Id: ",d.get('_id'))
        #        print("  Uptime: ",d.get('_uptime'))
        #        print("  Name: ",d.get('name'))
        #        print("  Hostname: ",d.get('hostname'))
        #        print("  Model: ",d.get('model'))
        #        print("  MAC: ",d.get('mac'))
        #        print("  CfgVersion: ",d.get('cfgversion'))
        #        print("  Adopted: ",d.get('adopted'))
        #        pprint.pprint(d)
        #        print("")

#        print("STA:")
#        sta = site.sta()
#        for s in sta:
#            pprint.pprint(s)


exit(0)
