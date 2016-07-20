from googlefinance import getQuotes

def getNasdaqValue(callback):
    ixic = getQuotes('.IXIC')
    if callback != None:
        callback(ixic[0]['LastTradePrice'], ixic[0]['Change'])

