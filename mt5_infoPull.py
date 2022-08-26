#Script that imports Terminal, Account and Instrument data from a MT5 Terminal
#By Eduardo Bogosian - 2022

import pandas as pd
import MetaTrader5 as mt5

#Starts connection with the terminal based on synthax
mt5.initialize()

#Terminal Information
terminal_info = mt5.terminal_info()._asdict()
terminal_info_df = pd.DataFrame(list(terminal_info.items()),columns=['Property','Value'])
print("Terminal Info:\n",terminal_info_df)

#Retrive if trade is allowed from dataframe matrix.
trade_allowed_bool = terminal_info_df.iat[4,1]

#Check if trades permited
if trade_allowed_bool == False:
    print("\nTrades are not allowed.")
elif trade_allowed_bool == True:
    print("\nTrades permited.")
else:
    print("\nUnkown trade status.")

#Account information
account_info = mt5.account_info()._asdict()
account_info_df = pd.DataFrame(list(account_info.items()),columns=['Property','Value'])
print("\nAccount Info:\n",account_info_df)

#Instrument Information
instrument = 'AAPL'
instrument_info = mt5.symbol_info(instrument)._asdict()
instrument_info_df = pd.DataFrame(list(instrument_info.items()),columns=['Property','Value'])
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print("\nData for:",instrument)
    print(instrument_info_df)
    
#End of interactions with the terimanl
mt5.shutdown()
