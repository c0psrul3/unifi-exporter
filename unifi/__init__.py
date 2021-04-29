from .network import Network
from .protect import Protect

class UniFiException(Exception):
    apimsg = None

    def __init__(self, apimsg, s=None):
        m = s
        if m is None:
            m = apimsg
        super(UniFiException, self).__init__(m)

        self.apimsg = apimsg




