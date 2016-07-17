__all__ = ['KiWoom']

from PyQt4.QtCore import *

class KiWoom:
    def __init__(self, ocx):
        self.ocx = ocx
        self.ocx.connect(self.ocx, SIGNAL('OnEventConnect(int)'), self.OnEventConnect)

    def OnEventConnect(self, err):
        self.callbackConnect(err);

    def CommConnect(self, callbackConnect):
        self.callbackConnect = callbackConnect
        self.ocx.dynamicCall('CommConnect()')




