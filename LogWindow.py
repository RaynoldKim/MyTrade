from PyQt4 import QtGui, QtCore
from PyQt4 import uic


form_class = uic.loadUiType('logWindow.ui')[0]


class LogWindow(QtGui.QDialog, form_class):
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setupUi(self)
        self.show()

    def addLog(self, msg):
        self.list_log.addItem(msg)

