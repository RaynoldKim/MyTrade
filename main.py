import sys
from KiWoom import KiWoom
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtGui import *
from PyQt4 import uic
import Nasdaq

form_class = uic.loadUiType('main.ui')[0]

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


	def btn_login_clicked(self):
		self.kiwoom.CommConnect(self.OnEventConnect);


	def OnEventConnect(self, ErrCode):
		if ErrCode == 0:
			self.statusbar.showMessage("connected")
			self.action_after_connection()
		else:
			self.statusbar.showMessage("Error %d " % ErrCode)


	def action_after_connection(self):
		self.kiwoom.requestAllStockInfo(self.OnReceiveAllStockInfo)
		self.kiwoom.requestLoginInfo(self.OnReceiveLoginInfo)
		self.kiwoom.requestKospi(self.OnReceiveKospi)
		Nasdaq.getNasdaqValue(self.OnReceiveNasdaq)
		self.kiwoom.requestCashBalance(self.OnReceiveCashBalance)

	def OnReceiveAllStockInfo(self, info):
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



if __name__ == "__main__":
	app = QApplication(sys.argv)
	m = Main()
	app.exec_()
