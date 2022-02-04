import time
import pyupbit
import datetime

access = "RKwDQiNOzHkimFdtXaqxL28Nf94DIRwAy7ixzbGX"
secret = "BhdEHxbux2Oc12ro2VaX5kI7FlfCxidJphcoCiQS"

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# symbols = ["KRW-EOS", "KRW-MBL", "KRW-MFT", "KRW-CRE", "KRW-TT", "KRW-MVL"]
# target_price = {}

# for symbol in symbols:
#     df = pyupbit.get_ohlcv(symbol, interval="minute5", count=2)
#     k = 1 - (abs(df.iloc[-2]['open'] - df.iloc[-2]['close']) / (df.iloc[-2]['high'] - df.iloc[-2]['low']))
#     target_price[symbol] = df.iloc[-1]['close'] + (df.iloc[-1]['high'] - df.iloc[-1]['low']) * k
    

# print(target_price)




symbols = ["KRW-EOS", "KRW-MBL", "KRW-MFT", "KRW-CRE", "KRW-TT", "KRW-MVL"]
coins = pyupbit.get_current_price(symbols)
print(coins)