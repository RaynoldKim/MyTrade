
__all__ = ['KiWoom']

from PyQt4.QtCore import *
import time
from Logger import Logger

class KiWoom:
    def __init__(self, ocx):
        self.ocx = ocx
        self.ocx.connect(self.ocx, SIGNAL('OnEventConnect(int)'), self.OnEventConnect)
        self.ocx.connect(self.ocx, SIGNAL('OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)'),
                         self.OnReceiveTrData)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveRealData(QString, QString, QString)"), self.OnReceiveRealData)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveRealCondition(QString, QString, QString, QString)"),
                         self.OnReceiveRealCondition)
        self.ocx.connect(self.ocx, SIGNAL('OnReceiveMsg(QString , QString , QString , QString )'),
                         self.OnReceiveMsg)
        self.ocx.connect(self.ocx, SIGNAL('OnReceiveChejanData(QString , int , QString )'),
                         self.OnReceiveChejanData)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveCondition(QString, QString, QString, QString)"),
                         self.OnReceiveCondition)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrCondition(QString, QString, QString, int, int)"),
                         self.OnReceiveTrCondition)
        self.ocx.connect(self.ocx, SIGNAL("OnReceiveConditionVer(int, QString)"), self.OnReceiveConditionVer)


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
        # elif RQName == 'opw00013':
        #     currentValue = self.CommGetData(TrCode, "", RQName, 0, '현금금액')
        #     currentValue = format(int(currentValue), ',d')
        #     if self.callback_requestCashBalance != None:
        #         self.callback_requestCashBalance(currentValue)
        elif RQName == 'opt10001':
            code = self.CommGetData(TrCode, "", RQName, 0, '종목코드')
            name = self.CommGetData(TrCode, "", RQName, 0, '종목명')
            currentValue = self.CommGetData(TrCode, "", RQName, 0, '현재가')
            fluctuations = self.CommGetData(TrCode, "", RQName, 0, '등락률')
            diffbefore = self.CommGetData(TrCode, "", RQName, 0, '전일대비')
            self.callback_request_stock_info((code, name, currentValue, fluctuations, diffbefore))

        elif RQName == 'opw00004':
            accountValue = {}
            accountValue['계좌명'] = self.CommGetData(TrCode, "", RQName, 0, '계좌명')
            accountValue['지점명'] = self.CommGetData(TrCode, "", RQName, 0, '지점명')
            accountValue['예수금'] = int(self.CommGetData(TrCode, "", RQName, 0, '예수금'))
            accountValue['유가잔고평가액'] = int(self.CommGetData(TrCode, "", RQName, 0, '유가잔고평가액'))
            accountValue['예탁자산평가액'] = int(self.CommGetData(TrCode, "", RQName, 0, '예탁자산평가액'))
            accountValue['총매입금액'] = int(self.CommGetData(TrCode, "", RQName, 0, '총매입금액'))
            accountValue['추정예탁자산'] = int(self.CommGetData(TrCode, "", RQName, 0, '추정예탁자산'))
            accountValue['매도담보대출금'] = int(self.CommGetData(TrCode, "", RQName, 0, '매도담보대출금'))
            accountValue['당일투자원금'] = int(self.CommGetData(TrCode, "", RQName, 0, '당일투자원금'))
            accountValue['당월투자원금'] = int(self.CommGetData(TrCode, "", RQName, 0, '당월투자원금'))
            accountValue['누적투자원금'] = int(self.CommGetData(TrCode, "", RQName, 0, '누적투자원금'))
            accountValue['당일투자손익'] = int(self.CommGetData(TrCode, "", RQName, 0, '당일투자손익'))
            accountValue['당월투자손익'] = int(self.CommGetData(TrCode, "", RQName, 0, '당월투자손익'))
            accountValue['누적투자손익'] = int(self.CommGetData(TrCode, "", RQName, 0, '누적투자손익'))
            x = 0
            try:
                x = float(self.CommGetData(TrCode, "", RQName, 0, '당일손익률'))
            except ValueError:
                x = 0
            accountValue['당일손익률'] = x
            try:
                x = float(self.CommGetData(TrCode, "", RQName, 0, '당월손익률'))
            except ValueError:
                x = 0
            accountValue['당월손익률'] = x
            try:
                x = float(self.CommGetData(TrCode, "", RQName, 0, '누적손익률'))
            except ValueError:
                x = 0
            accountValue['누적손익률'] = x
            Logger.instance().log(accountValue)

            cnt = self.GetRepeatCnt(TrCode, RQName)
            accountStocks = {}
            for i in range(cnt):
                name = self.CommGetData(TrCode, "", RQName, i, '종목명')
                value_rate = format(float(self.CommGetData(TrCode, "", RQName, i, '손익율')), '.2f')
                amount = format(int(self.CommGetData(TrCode, "", RQName, i, '보유수량')), ',d')
                value_cur = format(int(self.CommGetData(TrCode, "", RQName, i, '현재가')), ',d')
                value_avg = format(int(self.CommGetData(TrCode, "", RQName, i, '평균단가')), ',d')
                value_val = format(int(self.CommGetData(TrCode, "", RQName, i, '평가금액')), ',d')
                value_buy = format(int(self.CommGetData(TrCode, "", RQName, i, '매입금액')), ',d')

                accountStocks[name] = [value_rate, amount, value_cur, value_avg, value_val, value_buy]
                Logger.instance().log(name,
                                    ' 손익율', value_rate,
                                    ' 보유수량', amount,
                                    ' 현재가', value_cur,
                                    ' 평균단가', value_avg,
                                    ' 평가금액', value_val,
                                    ' 매입금액', value_buy)
            self.callback_requestCurrentAccountValue(accountValue, accountStocks)

    def OnReceiveRealData(self, sJongmokCode, sRealType, sRealData):
        Logger.instance().log('OnReceiveRealData ', sJongmokCode, sRealType, sRealData)

    def OnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        Logger.instance().log('OnReceiveRealCondition ', strCode, strType, strConditionName, strConditionIndex)

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        Logger.instance().log('OnReceiveMsg ', sRQName, sTrCode, sMsg)
        pass

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        Logger.instance().log('OnReceiveChejanData ', sGubun, nItemCnt, sFidList)

    def OnReceiveCondition(self, strCode, strType, strConditionName, strConditionIndex):
        Logger.instance().log('OnReceiveCondition ', strCode, strType, strConditionName, strConditionIndex)

    def OnReceiveConditionVer(self, lRet, sMsg):
        Logger.instance().log('OnReceiveConditionVer ', lRet, sMsg)

    def OnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        Logger.instance().log('OnReceiveTrCondition ', sScrNo, strCodeList, strConditionName, nIndex, nNext)

    def CommGetData(self, sJongmokCode, sRealType, sFieldName, nIndex, sInnerFiledName):
        data = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sJongmokCode, sRealType,
                                sFieldName, nIndex, sInnerFiledName)
        return data.strip()

    def CommConnect(self, callbackConnect):
        self.callbackConnect = callbackConnect
        rt = self.ocx.dynamicCall('CommConnect()')
        Logger.instance().log('CommConnect', rt)

    def CommRqData(self, trCode, nPrevNext, sScreenNo):
        self.ocx.dynamicCall('CommRqData(QString, QString, int, QString)', trCode, trCode, nPrevNext, sScreenNo)

    def GetMasrsterCodeName(self, code):
        return self.ocx.dynamicCall('GetMasterCodeName(QString)',[code])

    #nOrderType - 주문유형(1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
    #sHogaGb –  00:지정가, 03:시장가,
    #           05:조건부지정가, 06:최유리지정가, 07:최우선지정가,
    #           10:지정가IOC, 13:시장가IOC, 16:최유리IOC,
    #           20:지정가FOK, 23:시장가FOK, 26:최유리FOK,
    #           61:장전시간외종가, 62:시간외단일가, 81:장후시간외종가
    #※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 장전시간외, 장후시간외
    #※ 주문시 주문가격을 입력하지 않습니다.
    def SendOrder(self, sRQName,  sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo):
        ret = self.ocx.dynamicCall('SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)',
                             [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo])
        Logger.instance().log(self.convertErrorCode(ret))


    def requestOrder(self, code, quantity):
        self.SendOrder('RQ_1', 'ScreenNo', self.accountNo, 1, code, quantity, 0, '03', '');
        pass


    def requestAllStockName(self, callback):
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
        self.CommRqData('opt20001', '0', '0101')

    def requestCurrentAccountValue(self, callback):
        self.callback_requestCurrentAccountValue = callback
        self.SetInputValue('계좌번호', self.accountNo)
        self.SetInputValue("비밀번호", "8133")
        self.CommRqData('opw00004', "0", "화면번호")

    def requestStockInfo(self, stockName, callback):
        self.callback_request_stock_info = callback

        ix = self.codelist_korean.index(stockName)
        if ix >= 0:
            code = self.codelist[ix]
            self.SetInputValue('종목코드', code)
            self.CommRqData('opt10001', '0', '01011')
        else:
            callback(None)



    def GetConnectState(self):
        return self.ocx != None and (self.ocx.dynamicCall('GetConnectState()') == 1)















    def convertErrorCode(self, err):
        if err ==  0:
            desc = "정상처리";
        elif err == -100:
            desc = "사용자정보교환에 실패하였습니다. 잠시후 다시 시작하여 주십시오."
        elif err == - 101:
            desc = "서버 접속 실패"
        elif err == -102:
            desc = "버전처리가 실패하였습니다."
        elif err == -200:
            desc = '시세조회 과부하'
        elif err == -201:
            desc = 'REQUEST_INPUT_st Failed'
        elif err == -202:
            desc = '요청 전문 작성 실패'
        elif err == -300:
            desc = '주문 입력값 오류'
        elif err == -301:
            desc = '계좌비밀번호를 입력하십시오.'
        elif err == -302:
            desc = '타인계좌는 사용할 수 없습니다.'
        elif err == -303:
            desc = '주문가격이 20 억원을 초과합니다.'
        elif err == -304:
            desc = '주문가격은 50 억원을 초과할 수 없습니다.'
        elif err == -305:
            desc = '주문수량이 총발행주수의 1 % 를 초과합니다.'
        elif err == -306:
            desc = '주문수량은총발행주수의 3 % 를 초과할 수 없습니다.'
        else:
            desc = 'Unknown Error'
        return desc










