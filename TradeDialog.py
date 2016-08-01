from PyQt4 import QtGui, QtCore
from PyQt4 import uic

form_class = uic.loadUiType('tradeDialog.ui')[0]

dicPriceType = [
    ('지정가', '00'),
    ('시장가', '03')
]

class TradeDialog(QtGui.QDialog, form_class):
    def __init__(self, parent=None):
        super(TradeDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setupUi(self)
        for pricetype in dicPriceType:
            self.combo_price_type.addItem(pricetype[0])
        self.combo_price_type.currentIndexChanged.connect(self.on_price_type_changed)
        self.combo_price_type.setCurrentIndex(1)


    def on_price_type_changed(self, index):
        if dicPriceType[index][0] == '지정가':
            self.spin_price.setReadOnly(False)
            self.spin_price.setDisabled(False)

            pass
        elif dicPriceType[index][0] == '시장가':
            self.spin_price.setReadOnly(True)
            self.spin_price.setDisabled (True)
            pass


    def getQuantity(self):
        return self.spin_quantity.value()

    def getCurrentPriceType(self):
        return dicPriceType[self.combo_price_type.currentIndex()][1]

    def getCurrentInputPrice(self):
        return self.spin_price.value()


    @staticmethod
    def showTrade(parent):
        dialog = TradeDialog()
        dialog.spin_price.setValue(parent.currentSelectStockPrice)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            parent.kiwoom.requestOrder(parent.currentSelectStock[0], dialog.getCurrentPriceType(),
                                       dialog.getQuantity(), dialog.getCurrentInputPrice())