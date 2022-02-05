import time
import pyupbit
import datetime

access = "RKwDQiNOzHkimFdtXaqxL28Nf94DIRwAy7ixzbGX"
secret = "BhdEHxbux2Oc12ro2VaX5kI7FlfCxidJphcoCiQS"

upbit = pyupbit.Upbit(access, secret)

# 원화시장 전체
KRW_tickers = pyupbit.get_tickers("KRW")
buy_tickers = pyupbit.get_tickers("KRW")
start_ticker = "KRW-BTC"
k = 0.5
ticker = "KRW-EOS"

krw = upbit.get_balances()
resp = upbit.buy_market_order(KRW_tickers, 5000)
print(resp)
