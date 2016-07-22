
__all__ = ['KiWoom']

from PyQt4.QtCore import *
import time

class KiWoom:
    def __init__(self, ocx):
        self.ocx = ocx
        self.ocx.connect(self.ocx, SIGNAL('OnEventConnect(int)'), self.OnEventConnect)
        self.ocx.connect(self.ocx, SIGNAL('OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)'),
                         self.OnReceiveTrData)

    def OnEventConnect(self, err):
        self.callbackConnect(err);
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def SetInputValue(self, sID, sValue):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", sID, sValue)

    def GetRepeatCnt(self, sTrCode, sRecordName):
        ret = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRecordName)
        return ret

    def OnReceiveTrData(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrCode, Message, SplmMsg):
        # cnt = self.GetRepeatCnt(TrCode, RQName)
        if RQName == 'opt20001':
            currentValue = self.CommGetData(TrCode, "", RQName, 0, '현재가')
            fluctuations = self.CommGetData(TrCode, "", RQName, 0, '전일대비')
            if self.callback_requestKospi != None:
                self.callback_requestKospi(currentValue, fluctuations)
        elif RQName == 'opw00013':
            currentValue = self.CommGetData(TrCode, "", RQName, 0, '현금금액')
            currentValue = format(int(currentValue), ',d')
            if self.callback_requestCashBalance != None:
                self.callback_requestCashBalance(currentValue)


    def CommGetData(self, sJongmokCode, sRealType, sFieldName, nIndex, sInnerFiledName):
        data = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sJongmokCode, sRealType,
                                sFieldName, nIndex, sInnerFiledName)
        return data.strip()

    def CommConnect(self, callbackConnect):
        self.callbackConnect = callbackConnect
        rt = self.ocx.dynamicCall('CommConnect()')
        print('CommConnect', rt)

    def CommRqData(self, rqName, trCode, nPrevNext, sScreenNo):
        self.ocx.dynamicCall('CommRqData(QString, QString, int, QString)', rqName, trCode, nPrevNext, sScreenNo)

    def GetMasrsterCodeName(self, code):
        return self.ocx.dynamicCall('GetMasterCodeName(QString)',[code])

    def requestAllStockInfo(self, callback):
        self.codelist = self.ocx.dynamicCall('GetCodeListByMarket(QString)',['0']).split(';')
        self.codelist_korean = list(map(self.GetMasrsterCodeName, self.codelist))
        callback(self.codelist_korean)

    def requestLoginInfo(self, callback):
        self.callback_requestLoginInfo = callback

        accno = self.ocx.dynamicCall('GetLoginInfo(QString)', ["ACCNO"])
        self.accountNo = accno.rstrip(';')
        callback(self.accountNo)


    def requestKospi(self, callback):
        self.callback_requestKospi = callback

        self.SetInputValue('시장구분', '0')
        self.SetInputValue('업종코드', '001')
        self.CommRqData('opt20001', 'opt20001', '0', '0101')

    def requestCashBalance(self, callback):
        self.callback_requestCashBalance = callback
        self.SetInputValue('계좌번호', self.accountNo)
        self.SetInputValue("비밀번호", "8133")
        self.CommRqData("opw00013", "opw00013", "0", "화면번호")








