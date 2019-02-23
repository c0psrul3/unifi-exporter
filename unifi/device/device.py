class Device(object):
    def __init__(self, site, data):
        self.site = site
        self.name = data['name']
        self.model = data['model']
        self.id = data['_id']
        self.device_id = data['device_id']
        self.adopted = data['adopted']
        self.mac = data['mac']
        self.serial = data['serial']
        self.uplink = None
        self.sysstat = None
        self.stat = None

    def parse_uplink(self, data):
        self.uplink = data

    def parse_sysstat(self, data):
        self.sysstat = data

    def parse_stat(self, data):
        self.stat = data
