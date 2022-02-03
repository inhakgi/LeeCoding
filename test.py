import time
import pyupbit
import datetime

symbols = ["KRW-MBL", "KRW-EOS", "KRW-MFT", "KRW-CRE", "KRW-TT", "KRW-MVL"]
target_price = {}

for symbol in symbols:
    df = pyupbit.get_ohlcv(symbol, interval="minute5", count=20)
    k = 1 - (abs(df.iloc[0]['open'] - df.iloc[0]['close']) / (df.iloc[0]['high'] - df.iloc[0]['low']))
    target_price[symbol] = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k

print(target_price)

