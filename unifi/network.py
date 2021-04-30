#!/usr/bin/env python3

import json
import logging
import pprint
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, SNIMissingWarning, InsecurePlatformWarning

from . import device

class Network(object):
    def __init__(self, addr, username, password):
        self.addr = addr
        self.username = username
        self.password = password
        self.cookies = {}
        self.session = requests.Session()
        self.login()

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(SNIMissingWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

    '''
    Unifi API endpoints are described in wiki:
        (https://ubntwiki.com/products/software/unifi-controller/api)
    '''
    def api_addr(self, endpoint):
        if endpoint == "login":
            return self.addr + '/api/auth/' + endpoint
        if endpoint == "status":
            return self.addr + '/proxy/network/' + endpoint
        else:
            #print(self.addr + '/proxy/network/api/' + endpoint)
            return self.addr + '/proxy/network/api/' + endpoint

    def clear_session(self):
        self.session.cookies.clear()

    def api_process_response(self, r):
        # Will raise exceptions if failing
        self.set_error(r)
        # parse json output
        data = r.json()
        return data

    def api_post(self, endpoint, payload):
        logging.debug('API POST ' + endpoint)
        try:
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            r = self.session.post(self.api_addr(endpoint), headers = headers, json = payload, verify=False, timeout = 1)
            self.set_error(r)
            return self.api_process_response(r)
        except UniFiException as e:
            if endpoint != 'login' and e.apimsg is not None and e.apimsg == 'api.err.LoginRequired':
                self.login()
                r = self.session.post(self.api_addr(endpoint), headers = headers, json = payload, verify = False, timeout = 1)
                return self.api_process_response(r)
            else:
                raise e


    def api_get(self, endpoint):
        logging.debug('API GET ' + endpoint)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            r = self.session.get(self.api_addr(endpoint), headers = headers, verify = False, timeout = 1)
            return self.api_process_response(r)
        except UniFiException as e:
            if e.apimsg is not None and e.apimsg == 'api.err.LoginRequired':
                self.login()
                r = self.session.get(self.api_addr(endpoint), headers = headers, verify = False, timeout = 1)
                return self.api_process_response(r)
            else:
                raise e


    def set_error(self, r):
        if r.status_code != 200:
            print("ERROR - Status Code: ", r.status_code)
            return
        data = r.json()
        if 'meta' in data:
            if data['meta']['rc'] == 'ok':
                return
            elif data['meta']['rc'] == 'error':
                raise UniFiException(data['meta']['msg'])
            else:
                raise UniFiException(None, 'FAIL: \n' + pprint.pformat(data))


    def login(self):
        # https://controller:8443/api/login
        # > POST {"username":"ubnt","password":"ubnt","strict":true}:
        # < Set-Cookie: unifises=k8U3umwhciVfp8e43evU95mwQI3eAxK3; Path=/; Secure; HttpOnly
        # < Set-Cookie: csrf_token=k8U3umwhciVfp8e43evU95mwQI3eAxK3; Path=/; Secure
        # { "data" : [ ] , "meta" : { "rc" : "ok"}}
        logging.info('Login ' + self.addr)
        payload = { 'username': self.username, 'password': self.password }
        self.api_post('login', payload)


    def sites(self):
        # https://controller:8443/api/self/sites
        # { "data" : [ { "_id" : "56c87bc1b41038d25762ce86" , "attr_hidden_id" : "default" , "attr_no_delete" : true , "desc" : "Default" , "name" : "default" , "num_ap" : 2 , "num_sta" : 22 , "role" : "admin"}] , "meta" : { "rc" : "ok"}}
        data = self.api_get('self/sites')
        ret = []
        for s in data.get('data'):
            ret.append(Site(self, s))
        return ret


class Site(object):
    def __init__(self, unifi, data):
        self.unifi = unifi
        self.id = data['_id']
        self.desc = data['desc']
        self.name = data['name']
        self.role = data['role']

    def api_endpoint(self, endpoint):
        return 's/' + self.name + '/' + endpoint

    def health(self):
        # https://controller:8443/api/s/default/stat/device
        data = self.unifi.api_get(self.api_endpoint('stat/health'))
        return data['data']


    def device(self):
        # https://controller:8443/api/s/default/stat/device

        data = self.unifi.api_get(self.api_endpoint('stat/device'))
        ret = []
        for d in data['data']:
            if d['model'] == 'UGW3':
                ret.append(device.UGW3(self, d))
            elif d['model'] == 'US8P150':
                ret.append(device.US8P150(self, d))
            elif d['model'] == 'USL16LP':
                ret.append(device.USL16LP(self, d))
            elif d['model'] == 'USL8LP':
                ret.append(device.USL8LP(self, d))
            elif d['model'] == 'USMINI':
                ret.append(device.USMINI(self, d))
            elif d['model'] == 'USF5P':
                ret.append(device.USF5P(self, d))
            elif d['model'] == 'U7PG2':
                ret.append(device.U7PG2(self, d))
            elif d['model'] == 'U7HD':
                ret.append(device.U7HD(self, d))
            elif d['model'] == 'U7LT':
                ret.append(device.U7LT(self, d))
            elif d['model'] == 'U7NHD':
                ret.append(device.U7NHD(self, d))
            elif d['model'] == 'UHDIW':
                ret.append(device.UHDIW(self, d))
            else:
                print(f"Unknown device type/model: {d['type']}/{d['model']}")
        return ret

    def sta(self):
        # https://controller:8443/api/s/default/stat/sta
        data = self.unifi.api_get(self.api_endpoint('stat/sta'))
        return data['data']



class UniFiException(Exception):
    apimsg = None

    def __init__(self, apimsg, s=None):
        m = s
        if m is None:
            m = apimsg
        super(UniFiException, self).__init__(m)

        self.apimsg = apimsg


