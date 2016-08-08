from PyQt4 import QtGui, QtCore
from PyQt4 import uic

form_class = uic.loadUiType('tradeDialog.ui')[0]

dicOrderType = [
    ('매수', 1),
    ('매도', 2)
]

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
        for ordertype in dicOrderType:
            self.combo_order_type.addItem(ordertype[0])
        self.combo_order_type.currentIndexChanged.connect(self.on_order_type_changed)
        for pricetype in dicPriceType:
            self.combo_price_type.addItem(pricetype[0])
        self.combo_price_type.currentIndexChanged.connect(self.on_price_type_changed)
        self.combo_price_type.setCurrentIndex(1)
        self.spin_quantity.setValue(1)

    def on_order_type_changed(self, index):
        if dicOrderType[index][0] == '매수':
            pass
        elif dicOrderType[index][0] == '매도':
            pass

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

    def getCurrentOrderType(self):
        return dicOrderType[self.combo_order_type.currentIndex()][1]

    def getCurrentPriceType(self):
        return dicPriceType[self.combo_price_type.currentIndex()][1]

    def getCurrentInputPrice(self):
        return self.spin_price.value()


    @staticmethod
    def showTrade(parent):
        dialog = TradeDialog()

        dialog.spin_price.setValue(parent.currentSelectStockPrice)
        dialog.edit_code.setText(parent.currentSelectStockCode)
        dialog.edit_name.setText(parent.currentSelectStockName)


        if dialog.exec_() == QtGui.QDialog.Accepted:
            parent.kiwoom.requestOrder(parent.currentSelectStock[0],
                                       dialog.getCurrentOrderType(),
                                       dialog.getCurrentPriceType(),
                                       dialog.getQuantity(),
                                       dialog.getCurrentInputPrice())