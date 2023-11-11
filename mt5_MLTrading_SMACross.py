import pytz

import pandas as pd
import pandas_ta as ta
import MetaTrader5 as mt5

from datetime import datetime

mt5.initialize()
timezone = pytz.timezone("Etc/UTC")
from_date = datetime.now()
look_back = 100
historical_data = mt5.copy_rates_from("AAPL", mt5.TIMEFRAME_H1, from_date, look_back)
df = pd.DataFrame(historical_data)
df['time'] = pd.to_datetime(df['time'], unit='s')

del df['tick_volume']
del df['real_volume']
del df['spread']

print(df)
