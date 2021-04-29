class Device(object):
    def __init__(self, site, data):
        self.site = site
        self.name = data.get('name', data.get('hostname', data.get('mac')))
        self.type = data.get('type', "")
        self.model = data.get('model', "")
        self.id = data.get('_id', "")
        self.device_id = data.get('device_id', "")
        self.adopted = str(data.get('adopted', 0))
        self.ip_address = str(data.get('ip', ""))
        self.hostname = str(data.get('hostname', data.get('ip', "")))
        self.mac = str(data.get('mac', ""))
        self.serial = str(data.get('serial', ""))
        self.version = str(data.get('version', ""))
        self.upgradable = str(data.get('upgradable', ""))
        self.architecture = str(data.get('architecture', ""))
        self.cfgversion = str(data.get('cfgversion', ""))
        self.kernel_version = str(data.get('kernel_version', ""))
        self.board_rev = str(data.get('board_rev', ""))
        self.provisioned_at = str(data.get('provisioned_at', 0))
        self.last_seen = str(data.get('last_seen', 0))
        self.connected_at = str(data.get('connected_at', 0))
        self.state = str(data.get('state', 0))
        self.uptime = str(data.get('uptime', 0))
        self.overheating = str(data.get('overheating', ""))
        self.power_source = str(data.get('power_source', ""))
        self.power_source_voltage = str(data.get('power_source_voltage', ""))
        self.uplink = None
        self.sysstat = None
        self.stat = None

    def parse_uplink(self, data):
        self.uplink = data

    def parse_sysstat(self, data):
        self.sysstat = data

    def parse_stat(self, data):
        self.stat = data

class USMINI(Device):

    def __init__(self, site, data):
        super(USMINI, self).__init__(site, data)

        self.port = {}
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_port_table(data['port_table'])
        self.general_temperature = data.get('general_temperature')
        self.parse_sysstat(data.get('sys_stats'))

    def parse_port_table(self, data):
        for port in data:
            self.port[port['port_idx']] = port

class USL8LP(Device):

    def __init__(self, site, data):
        super(USL8LP, self).__init__(site, data)

        self.port = {}
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_port_table(data['port_table'])
        self.general_temperature = data.get('general_temperature')
        self.parse_sysstat(data.get('sys_stats'))

    def parse_port_table(self, data):
        for port in data:
            self.port[port['port_idx']] = port

class USL16LP(Device):

    def __init__(self, site, data):
        super(USL16LP, self).__init__(site, data)

        self.port = {}
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_port_table(data['port_table'])
        self.general_temperature = data.get('general_temperature')
        self.parse_sysstat(data.get('sys_stats'))

    def parse_port_table(self, data):
        for port in data:
            self.port[port['port_idx']] = port

class USF5P(Device):

    def __init__(self, site, data):
        super(USF5P, self).__init__(site, data)

        self.port = {}
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_port_table(data['port_table'])
        self.general_temperature = data.get('general_temperature')
        self.parse_sysstat(data.get('sys_stats'))

    def parse_port_table(self, data):
        for port in data:
            self.port[port['port_idx']] = port

class US8P150(Device):

    def __init__(self, site, data):
        super(US8P150, self).__init__(site, data)

        self.port = {}
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_port_table(data['port_table'])
        self.general_temperature = data.get('general_temperature')
        self.parse_sysstat(data.get('sys_stats'))

    def parse_port_table(self, data):
        for port in data:
            self.port[port['port_idx']] = port

class UHDIW(Device):

    def __init__(self, site, data):
        super(UHDIW, self).__init__(site, data)

        self.radio = {}
        self.vap = []
        self.parse_radio(data['radio_table'])
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_vap_table(data['vap_table'])
        self.parse_sysstat(data['sys_stats'])

    def parse_radio(self, data):
        for radio in data:
            rstr = radio['radio']
            self.radio[rstr] = radio

    def parse_vap_table(self, data):
        for vap in data:
            self.vap.append(vap)

class UGW3(Device):

    def __init__(self, site, data):
        super(UGW3, self).__init__(site, data)

        self.networks = {}
        self.ports = {}
        self.parse_network_table(data['network_table'])
        self.parse_ports_table(data['port_table'])
        self.parse_stat(data['stat'])
        self.parse_sysstat(data['sys_stats'])
        self.parse_uplink(data['uplink'])

    def parse_network_table(self, data):
        for network in data:
            self.networks[network['name']] = network
    
    def parse_ports_table(self, data):
        for port in data:
            self.ports[port['name']] = port

class U7PG2(Device):

    def __init__(self, site, data):
        super(U7PG2, self).__init__(site, data)

        self.radio = {}
        self.vap = []
        self.parse_radio(data['radio_table'])
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_vap_table(data.get('vap_table'))
        self.parse_sysstat(data.get('sys_stats'))

    def parse_radio(self, data):
        for radio in data:
            rstr = radio['radio']
            self.radio[rstr] = radio

    def parse_vap_table(self, data):
        if data:
            for vap in data:
                self.vap.append(vap)

class U7NHD(Device):

    def __init__(self, site, data):
        super(U7NHD, self).__init__(site, data)

        self.radio = {}
        self.vap = []
        self.parse_radio(data['radio_table'])
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_vap_table(data['vap_table'])
        self.parse_sysstat(data['sys_stats'])

    def parse_radio(self, data):
        for radio in data:
            rstr = radio['radio']
            self.radio[rstr] = radio

    def parse_vap_table(self, data):
        for vap in data:
            self.vap.append(vap)

class U7LT(Device):

    def __init__(self, site, data):
        super(U7LT, self).__init__(site, data)

        self.radio = {}
        self.vap = []
        self.parse_radio(data['radio_table'])
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_vap_table(data['vap_table'])
        self.parse_sysstat(data['sys_stats'])

    def parse_radio(self, data):
        for radio in data:
            rstr = radio['radio']
            self.radio[rstr] = radio

    def parse_vap_table(self, data):
        for vap in data:
            self.vap.append(vap)

class U7HD(Device):

    def __init__(self, site, data):
        super(U7HD, self).__init__(site, data)

        self.radio = {}
        self.vap = []
        self.parse_radio(data['radio_table'])
        self.parse_stat(data['stat'])
        self.parse_uplink(data.get('uplink'))
        self.parse_vap_table(data['vap_table'])
        self.parse_sysstat(data['sys_stats'])

    def parse_radio(self, data):
        for radio in data:
            rstr = radio['radio']
            self.radio[rstr] = radio

    def parse_vap_table(self, data):
        for vap in data:
            self.vap.append(vap)


