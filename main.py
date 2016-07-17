import sys
from KiWoom import KiWoom
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtGui import *


class Main(QMainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.setup_ui()
		self.setup_components()
		self.show()

	def setup_ui(self):
		self.setWindowTitle("myTrade")
		self.setGeometry(300, 300, 300, 150)
		self.statusBar = QStatusBar(self)
		self.setStatusBar(self.statusBar)
		self.btn_login = QPushButton('Login', self)
		self.btn_login.move(20, 20)
		self.btn_login.clicked.connect(self.btn_login_clicked)

	def setup_components(self):
		self.kiwoom = KiWoom(QAxWidget("KHOPENAPI.KHOpenAPICtrl.1"))


	def btn_login_clicked(self):
		self.kiwoom.CommConnect(self.OnEventConnect);


	def OnEventConnect(self, ErrCode):
		if ErrCode == 0:
			self.statusBar.showMessage("connected")
			self.action_after_connection()
		else:
			self.statusBar.showMessage("Error %d " % ErrCode)


	def action_after_connection(self):
		pass


if __name__ == "__main__":
	app = QApplication(sys.argv)
	m = Main()
	app.exec()
