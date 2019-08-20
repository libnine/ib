import pandas as pd, sys

from ib.ext.ContractDetails import ContractDetails
from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from ib.ext.TickType import TickType as tt
from ib.ext.Order import Order

contracts = pd.DataFrame([
    ['BA', 'SMART', 'USD', '20191018', 0, 0, 0]
])

contracts.columns = ['symbol', 'exchange', 'currency', 'expiry', 'bidPrice', 'askPrice', 'lastPrice']


def options_handler(msg):
    if msg.field in [tt.BID, tt.ASK, tt.LAST]:
        contracts.loc[msg.tickerId, tt.getField(msg.field)] = msg.price

        if msg.field == tt.LAST:
            pass

def error_handler(msg):
    print(msg)

if __name__ == '__main__':
    # order id; increment every order
    oid = 1

    # connect to ib
    con = ibConnection(clientId=1375)
    con.register(options_handler, message.tickPrice, message.tickSize)
    con.register(error_handler, message.Error)
    con.connect()

    # create contract
    c = Contract()
    c.m_symbol, c.m_exchange, c.currency = contracts['symbol'][0], contracts['exchange'][0], contracts['currency'][0]
    c.m_expiry, c.m_secType, c.m_strike, c.m_multiplier = contracts['expiry'][0], 'OPT', 325, 100

    # con.reqMktData(str(contracts[contracts['symbol'] == 'BA'].index.item()), c, "", False)
    # con.reqContractDetails(c)

