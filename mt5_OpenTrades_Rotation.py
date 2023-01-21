# Script that imports open trade data from a MT5 Terminal and rotates through graphs.
# Made for article on Medium: https://medium.com/@eduardo-bogosian/a-python-script-that-rotates-through-your-open-trades-in-mt5-2ccd9e7136f5
# By Eduardo Bogosian - 2023

# Imports
import pytz
import time
import datetime

import pandas as pd
import seaborn as sns
import MetaTrader5 as mt5
import matplotlib.pyplot as plt

from datetime import date
from datetime import datetime


# ------------------------------------------------
# Defs

def get_today():
    timezone = pytz.timezone("Etc/UTC")
    current_date = str(date.today())
    current_year = int(current_date[0] + current_date[1] + current_date[2] + current_date[3])
    current_month = int(current_date[5] + current_date[6])
    current_day = int(current_date[8] + current_date[9])
    today = datetime(current_year, current_month, current_day, tzinfo=timezone)

    return today


def get_instrument_historical(instrument):
    today = get_today()
    hist = mt5.copy_rates_from(instrument, mt5.TIMEFRAME_D1, today, 90)
    hist_df = pd.DataFrame(hist)
    hist_df['time'] = pd.to_datetime(hist_df['time'], unit='s')
    del hist_df['tick_volume']
    del hist_df['spread']
    del hist_df['real_volume']

    return hist_df


def get_open_price(trades_df, instrument):
    open_price_loc = trades_df[trades_df['symbol'] == instrument].index.values
    open_price = trades_df.iloc[open_price_loc]['price_open']
    open_price = float(open_price)
    
    return open_price


def get_stop_loss(trades_df, instrument):
    stop_loss_loc = trades_df[trades_df['symbol'] == instrument].index.values
    stop_loss = trades_df.iloc[stop_loss_loc]['sl']
    stop_loss = float(stop_loss)
    return stop_loss


def get_take_profit(trades_df, instrument):
    take_profit_loc = trades_df[trades_df['symbol'] == instrument].index.values
    take_profit = trades_df.iloc[take_profit_loc]['tp']
    take_profit = float(take_profit)
    
    return take_profit


def get_trade_direction(trades_df, instrument):
    trade_direction_loc = trades_df[trades_df['symbol'] == instrument].index.values
    trade_direction_indicator = trades_df.iloc[trade_direction_loc]['type']
    trade_direction_indicator = str(trade_direction_indicator)
    trade_direction = int(trade_direction_indicator[5])
    if trade_direction == 0:
        return 'Long'
    elif trade_direction == 1:
        return 'Short'
    else:
        return 'Unknown'


def show_graph(trades_df, instrument_history, ticker, duration):
    open_price = get_open_price(trades_df, ticker)
    stop_loss = get_stop_loss(trades_df, ticker)
    take_profit = get_take_profit(trades_df, ticker)
    trade_direction = str(get_trade_direction(trades_df, ticker))
    symbol = str(ticker)
    plt.figure(figsize=(16, 6))
    sns.lineplot(data=instrument_history,
                 x=instrument_history['time'],
                 y=instrument_history['close'],
                 color='black')
    plt.axhline(y=open_price, color='blue')
    plt.axhline(y=stop_loss, color='red')
    plt.axhline(y=take_profit, color='green')
    plt.title(f'{symbol} - {trade_direction}')
    plt.show(block=False)
    plt.pause(1.00)
    time.sleep(duration)
    plt.close()

# ------------------------------------------------


def main():
    print("Starting up...")
    while 1 == 1:
        # Get active trades (if none wait 'x' amount of time)
        trades = mt5.positions_get()
        if not trades:
            print("No open trades. Waiting...")
            time.sleep(60)
            continue
        else:
            open_trades = pd.DataFrame(list(trades),
                                       columns=trades[0]._asdict().keys())
            open_trades['time'] = pd.to_datetime(open_trades['time'],
                                                 unit='s')
            with pd.option_context('display.max_rows',
                                   None,
                                   'display.max_columns',
                                   None):
                # print(open_trades)
                pass

            # Get graph data for instrument[0]
            for instrument in open_trades['symbol']:
                hist = get_instrument_historical(instrument)
                # Show graph for x amount of time
                show_graph(open_trades, hist, instrument, 10)

    mt5.shutdown()

# ------------------------------------------------


if __name__ == '__main__':
    mt5.initialize()
    main()
