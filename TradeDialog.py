from PyQt4 import QtGui, QtCore
from PyQt4 import uic

form_class = uic.loadUiType('tradeDialog.ui')[0]


class TradeDialog(QtGui.QDialog, form_class):
    def __init__(self, parent=None):
        super(TradeDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setupUi(self)

    @staticmethod
    def showTrade(parent):
        dialog = TradeDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            parent.kiwoom.requestOrder(parent.currentSelectStock[0], dialog.spin_quantity.value())