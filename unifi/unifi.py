#!/usr/bin/env python3

import json
import logging
import pprint
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, SNIMissingWarning, InsecurePlatformWarning

from . import site

class UniFiException(Exception):
    apimsg = None

    def __init__(self, apimsg, s=None):
        m = s
        if m is None:
            m = apimsg
        super(UniFiException, self).__init__(m)

        self.apimsg = apimsg

class UniFi(object):
    def __init__(self, addr, username, password):
        self.addr = addr
        self.username = username
        self.password = password
        self.cookies = {}
        self.session = requests.Session()

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(SNIMissingWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

    def api_addr(self, endpoint):
        return self.addr + '/api/' + endpoint

    def clear_session(self):
        self.session.cookies.clear()

    def api_process_response(self, r):
        data = r.json()
        # Will raise exceptions if failing
        self.set_error(data)
        return data

    def api_post(self, endpoint, payload):
        logging.debug('API POST ' + endpoint)
        try:
            r = self.session.post(self.api_addr(endpoint), data=json.dumps(payload), verify=False)
            return self.api_process_response(r)
        except UniFiException as e:
            if endpoint != 'login' and e.apimsg is not None and e.apimsg == 'api.err.LoginRequired':
                self.login()
                r = self.session.post(self.api_addr(endpoint), data=json.dumps(payload), verify=False)
                return self.api_process_response(r)
            else:
                raise e


    def api_get(self, endpoint):
        logging.debug('API GET ' + endpoint)
        try:
            r = self.session.get(self.api_addr(endpoint), verify=False)
            return self.api_process_response(r)
        except UniFiException as e:
            if e.apimsg is not None and e.apimsg == 'api.err.LoginRequired':
                self.login()
                r = self.session.get(self.api_addr(endpoint), verify=False)
                return self.api_process_response(r)
            else:
                raise e


    def set_error(self, data):
        if data['meta']['rc'] == 'ok':
            return
        elif data['meta']['rc'] == 'error':
            raise UniFiException(data['meta']['msg'])
        else:
            raise UniFiException(None, 'FAIL: \n' + pprint.pformat(data))

    def login(self):
        # https://hemma:8443/api/login
        # > POST {"username":"ubnt","password":"ubnt","strict":true}:
        # < Set-Cookie: unifises=k8U3umwhciVfp8e43evU95mwQI3eAxK3; Path=/; Secure; HttpOnly
        # < Set-Cookie: csrf_token=k8U3umwhciVfp8e43evU95mwQI3eAxK3; Path=/; Secure
        # { "data" : [ ] , "meta" : { "rc" : "ok"}}
        logging.info('Login ' + self.addr)
        payload = { 'username': self.username, 'password': self.password }
        self.api_post('login', payload)

    def sites(self):
        # https://hemma:8443/api/self/sites
        # { "data" : [ { "_id" : "56c87bc1b41038d25762ce86" , "attr_hidden_id" : "default" , "attr_no_delete" : true , "desc" : "Default" , "name" : "default" , "num_ap" : 2 , "num_sta" : 22 , "role" : "admin"}] , "meta" : { "rc" : "ok"}}
        data = self.api_get('self/sites')
        ret = []
        for s in data['data']:
            ret.append(site.Site(self, s))
        return ret
