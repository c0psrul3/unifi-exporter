#!/usr/bin/env python3

import time
import configparser
import argparse
import pprint
from unifi import unifi

parser = argparse.ArgumentParser(description='UniFi Prometheus dump')
parser.add_argument('--config', dest='config', default=None, required=True, help='Configuration file for API')

args = parser.parse_args()
configfile = args.config

config = configparser.ConfigParser()
config.read(configfile)
apiendpoint = config.get('API','URL')
apiusername = config.get('API','Username')
apipassword = config.get('API','Password')

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
