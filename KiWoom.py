__all__ = ['KiWoom']

from PyQt4.QtCore import *

class KiWoom:
    def __init__(self, ocx):
        self.ocx = ocx
        self.ocx.connect(self.ocx, SIGNAL('OnEventConnect(int)'), self.OnEventConnect)
        self.ocx.connect(self.ocx, SIGNAL('OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)'),
                         self.OnReceiveTrData)

    def OnEventConnect(self, err):
        self.callbackConnect(err);

    def SetInputValue(self, sID, sValue):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", sID, sValue)

    def GetRepeatCnt(self, sTrCode, sRecordName):
        ret = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRecordName)
        return ret

    def OnReceiveTrData(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrCode, Message, SplmMsg):
        if self.callback_requestKospi != None:
            self.callback_requestKospi(1000)
        self.tr_event_loop.exit()

    def CommConnect(self, callbackConnect):
        self.callbackConnect = callbackConnect
        self.ocx.dynamicCall('CommConnect()')

    def CommRqData(self, rqName, trCode, nPrevNext, sScreenNo):
        self.ocx.dynamicCall('CommRqData(QString, QString, int, QString)', rqName, trCode, nPrevNext, sScreenNo)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def requestKospi(self, callback):
        self.callback_requestKospi = callback

        self.SetInputValue('업종코드', '001')
        self.CommRqData('RQName', 'opt20001', '0', '화면번호')






