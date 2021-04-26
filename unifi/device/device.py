class Device(object):
    def __init__(self, site, data):
        self.site = site
        self.name = data.get('name', "")
        self.type = data.get('type', "")
        self.model = data.get('model', "")
        self.id = data.get('_id', "")
        self.device_id = data.get('device_id', "")
        self.adopted = str(data.get('adopted', 0))
        self.ip_address = str(data.get('ip',""))
        self.hostname = str(data.get('hostname',""))
        self.mac = str(data.get('mac', ""))
        self.serial = str(data.get('serial', ""))
        self.version = str(data.get('version', ""))
        self.upgradable = str(data.get('upgradable', ""))
        self.architecture = str(data.get('architecture', ""))
        self.cfgversion = str(data.get('cfgversion', ""))
        self.kernel_version = str(data.get('kernel_version', ""))
        self.board_rev = str(data.get('board_rev', ""))
        self.provisioned_at = str(data.get('provisioned_at', ""))
        self.last_seen = str(data.get('last_seen', ""))
        self.connected_at = str(data.get('connected_at', ""))
        self.uptime = str(data.get('uptime', ""))
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

