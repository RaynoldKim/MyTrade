import sys
from KiWoom import KiWoom
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtGui import *
from PyQt4 import uic
import Nasdaq
import re
from Logger import Logger

form_class = uic.loadUiType('main.ui')[0]


# class MyTable(QTableWidget):
#     def __init__(self, data, *args):
#         QTableWidget.__init__(self, *args)
#         self.data = data
#         self.setmydata()
#         self.resizeColumnsToContents()
#         self.resizeRowsToContents()
#
#     def setmydata(self):
#         horHeaders = []
#         for n, key in enumerate(sorted(self.data.keys())):
#             horHeaders.append(key)
#             for m, item in enumerate(self.data[key]):
#                 newitem = QTableWidgetItem(item)
#                 self.setItem(m, n, newitem)
#         self.setHorizontalHeaderLabels(horHeaders)
# 		self.resizeColumnsToContents()
# 		self.resizeRowsToContents()


class Main(QMainWindow, form_class):
	def __init__(self):
		super().__init__()
		self.setup_ui()
		self.setup_components()
		self.show()

	def setup_ui(self):
		self.setupUi(self)
		self.actionLogin.triggered.connect(self.btn_login_clicked)
		self.label_kospi.setText('KOSPI : -')
		self.label_nasdaq.setText('NASDAQ : -')
		self.label_cash_balance.setText('Cash : -')
		self.edit_all_stock_filter.textChanged.connect(self.on_edit_all_stock_filter_chagned)
		self.list_all_stock.currentItemChanged.connect(self.on_list_all_stock_item_selection_changed)
		self.btn_search_stock_buy.clicked.connect(self.on_btn_search_stock_buy_clicked)

		self.label_search_stock_name.setText('종목명 : -')
		self.label_search_stock_current.setText('현재가 : -')
		self.label_search_stock_fluctuations.setText('등락률 : -')
		self.label_search_stock_diffbefore.setText('전일대비 : -')

		# self.table_have_stock.setRowCount(10);
		# self.table_have_stock.setColumnCount(5);
		# horHeaders = []
		# self.data = {'col1': ['1', '2', '3'], 'col2': ['4', '5', '6'], 'col3': ['7', '8', '9']}
		# for n, key in enumerate(sorted(self.data.keys())):
		# 	horHeaders.append(key)
		# 	for m, item in enumerate(self.data[key]):
		# 		newitem = QTableWidgetItem(item)
		# 		newitem.setBackgroundColor(QColor('red'))
		# 		self.table_have_stock.setItem(m, n, newitem)
		# self.table_have_stock.setHorizontalHeaderLabels(horHeaders)
		# self.table_have_stock.resizeColumnsToContents()
		# self.table_have_stock.resizeRowsToContents()


		# self.setWindowTitle("myTrade")
		# self.setGeometry(300, 300, 400, 150)
		# self.statusbar = QStatusBar(self)
		# self.setStatusBar(self.statusbar)
		# self.btn_login = QPushButton('Login', self)
		# self.btn_login.move(20, 20)
		# self.btn_login.clicked.connect(self.btn_login_clicked)
		# self.label_login_info = QLabel(self)
		# self.label_login_info.setMinimumWidth(200)
		# self.label_login_info.move(20, 0)
		# self.label_kospi = QLabel(self)
		# self.label_kospi.setMinimumWidth(200)
		# self.label_kospi.move(20, 80)
		# self.label_kospi.setText('KOSPI : -')
		# self.label_nasdaq = QLabel(self)
		# self.label_nasdaq.setMinimumWidth(200)
		# self.label_nasdaq.move(220, 80)
		# self.label_nasdaq.setText('NASDAQ : -')
		# self.label_cash_balance = QLabel(self)
		# self.label_cash_balance.move(20, 120)
		# self.label_cash_balance.setMinimumWidth(200)
		# self.label_cash_balance.setText('Cash : -')

	def setup_components(self):
		self.kiwoom = KiWoom(QAxWidget("KHOPENAPI.KHOpenAPICtrl.1"))
		Logger.instance().setCallback(self.onLogCollect)

	def onLogCollect(self, *varl):
		msg =''
		index = 0
		for i in varl:
			if index != 0:
				msg += ' '
			msg += repr(i)
			index += 1

		self.list_log.addItem(msg)


	def btn_login_clicked(self):
		self.kiwoom.CommConnect(self.OnEventConnect)


	def OnEventConnect(self, ErrCode):
		if ErrCode == 0:
			self.statusbar.showMessage("connected")
			self.action_after_connection()
		else:
			self.statusbar.showMessage("Error %d " % ErrCode)


	def action_after_connection(self):
		self.kiwoom.requestAllStockName(self.OnReceiveAllStockName)
		self.kiwoom.requestLoginInfo(self.OnReceiveLoginInfo)
		self.kiwoom.requestKospi(self.OnReceiveKospi)
		Nasdaq.getNasdaqValue(self.OnReceiveNasdaq)
		self.kiwoom.requestCashBalance(self.OnReceiveCashBalance)
		self.kiwoom.requestStockBalance(self.OnReceiveStockBalance)

	def OnReceiveAllStockName(self, info):
		self.stock_names = info
		self.list_all_stock.clear()
		self.list_all_stock.addItems(info)
		pass

	def OnReceiveLoginInfo(self, info):
		self.label_login_info.setText('Info : %s' % info)

	def OnReceiveKospi(self, value, fluctuations):
		self.label_kospi.setText('KOSPI : %s (%s)'% (value, fluctuations))

	def OnReceiveNasdaq(self, value, fluctuations):
		self.label_nasdaq.setText('NASDAQ : %s (%s)' % (value, fluctuations))

	def OnReceiveCashBalance(self, cash):
		self.label_cash_balance.setText('Cash : %s' % cash)

	def OnReceiveStockBalance(self, stocks):
		self.table_have_stock.clear()

		verHeaders = []
		horHeaders = ['손익율', '수량', '현재가', '평균단가', '평가금액', '매입금액']

		self.table_have_stock.setColumnCount(len(horHeaders))
		self.table_have_stock.setRowCount(len(stocks))
		for j, name in enumerate(stocks.keys()):
			verHeaders.append(name)
			values = stocks[name]
			for i, item in enumerate(values):
				newitem = QTableWidgetItem(item)
				if i == 0 :
					if float(item) > 0:
						newitem.setBackgroundColor(QColor('green'))
					elif float(item) < 0:
						newitem.setBackgroundColor(QColor('red'))				
				self.table_have_stock.setItem(j, i, newitem)
		self.table_have_stock.setVerticalHeaderLabels(verHeaders)
		self.table_have_stock.setHorizontalHeaderLabels(horHeaders)
		self.table_have_stock.resizeColumnsToContents()
		self.table_have_stock.resizeRowsToContents()

		pass

	def on_edit_all_stock_filter_chagned(self, filterString):
		p = re.compile(filterString, re.I)
		filteredList = list(filter(p.search, self.stock_names))
		self.list_all_stock.clear()
		self.list_all_stock.addItems(filteredList)

	def on_list_all_stock_item_selection_changed(self, current, before):
		if self.isConnected and current != None:
			self.kiwoom.requestStockInfo(current.text(), self.OnReceiveStockInfo)

	def OnReceiveStockInfo(self, infos):
		self.currentSelectStock = infos
		self.label_search_stock_name.setText('종목명 : %s' % infos[1])
		self.label_search_stock_current.setText('현재가 : %s' % abs(int(infos[2])))
		self.label_search_stock_fluctuations.setText('등락률 : %s' % infos[3])
		self.label_search_stock_diffbefore.setText('전일대비 : %s' % infos[4])

	def on_btn_search_stock_buy_clicked(self, check = True):
		if check != True:
			return
		if self.isConnected != True:
			QMessageBox.warning(self, '경고', '접속 상태를 확인해주세요.')
			return

		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle('매수 확인!')
		msg.setText( '%s %s'%(self.currentSelectStock[1], self.currentSelectStock[0]))
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		retval = msg.exec_()
		if retval == QMessageBox.Yes:
			self.kiwoom.requestOrder(self.currentSelectStock[0], 1)

	@property
	def isConnected(self):
		return self.kiwoom != None and self.kiwoom.GetConnectState()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	m = Main()
	app.exec_()
