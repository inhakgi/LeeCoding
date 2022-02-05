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
buy_tickers = pyupbit.get_tickers("KRW")
start_ticker = "KRW-BTC"
k = 0.5


def get_target_price(KRW_tickers, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(KRW_tickers, interval="day", count=3)
    target_price = df.iloc[-2]['close'] + (df.iloc[-1]['high'] - df.iloc[-1]['low']) * k
    return target_price
    
def get_start_time(start_ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(start_ticker, interval="days", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(KRW_tickers):
    """현금 잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == KRW_tickers:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_balance(buy_tickers):
    """보유 코인 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == buy_tickers:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(KRW_tickers):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=KRW_tickers)[0]["orderbook_units"][0]["ask_price"]



# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(KRW_tickers, k)
            current_price = get_current_price(KRW_tickers)
            if target_price < current_price:
                KRW = get_balance(KRW_tickers)
                if KRW > 5000:
                    upbit.buy_market_order(KRW_tickers, 5000) #"조건을 만족할때 구매하시오"를 개별코인으로 구분해야될듯. 실행이 안됨.
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)