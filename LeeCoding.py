import time
import pyupbit
import datetime

# access key, secret key
access = "RKwDQiNOzHkimFdtXaqxL28Nf94DIRwAy7ixzbGX"
secret = "BhdEHxbux2Oc12ro2VaX5kI7FlfCxidJphcoCiQS"

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 원화시장 전체
KRW_tickers = pyupbit.get_tickers("KRW")


# def get_target_price():
#     """변동성 돌파 전략으로 매수 목표가 조회"""
#     symbols = ["KRW-MBL", "KRW-EOS", "KRW-MFT", "KRW-CRE", "KRW-TT", "KRW-MVL"]
#     target_price = {}
#     for symbol in symbols:
#         df = pyupbit.get_ohlcv(symbol, interval="minute5", count=2)
#         k = 1 - (abs(df.iloc[-2]['open'] - df.iloc[-2]['close']) / (df.iloc[-2]['high'] - df.iloc[-2]['low']))
#         target_price[symbol] = df.iloc[-1]['close'] + (df.iloc[-1]['high'] - df.iloc[-1]['low']) * k
    
# def get_start_time(ticker):
#     """시작 시간 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="days", count=1)
#     start_time = df.index[0]
#     return start_time

# def get_balance(ticker):
#     """잔고 조회"""
#     balances = upbit.get_balances()
#     for b in balances:
#         if b['currency'] == ticker:
#             if b['balance'] is not None:
#                 return float(b['balance'])
#             else:
#                 return 0
#     return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)[0]["orderbook_units"][0]["ask_price"]



# 자동매매 시작
while True:
    try:
        symbols = ["KRW-MBL", "KRW-EOS", "KRW-MFT", "KRW-CRE", "KRW-TT", "KRW-MVL"]        
        target_price = {}     
        for symbol in symbols:
            df = pyupbit.get_ohlcv(symbol, interval="minute5", count=2)
            k = 1 - (abs(df.iloc[-2]['open'] - df.iloc[-2]['close']) / (df.iloc[-2]['high'] - df.iloc[-2]['low']))
            target_price[symbol] = df.iloc[-1]['close'] + (df.iloc[-1]['high'] - df.iloc[-1]['low']) * k        
        current_price = pyupbit.get_current_price(symbols)
        
        if target_price < current_price:
            balance = upbit.get_balance()
            krw = balance("KRW")
            
            if krw > 5000:
                upbit.buy_market_order(symbols, krw*0.9995)
        
        else:
            coins = balance("symbols")
            
            if coins > 0.00008:
                upbit.sell_market_order(symbols, btc*0.9995)
        time.sleep(1)      
    except Exception as e:
        print(e)
        time.sleep(1)