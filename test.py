import pyupbit
import time
import datetime
import numpy as np

access = "RKwDQiNOzHkimFdtXaqxL28Nf94DIRwAy7ixzbGX"
secret = "BhdEHxbux2Oc12ro2VaX5kI7FlfCxidJphcoCiQS"

########################################################################

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_best(ticker):
    best_ror = 0
    best_k = 0.5
    for k in np.arange(0.1, 1.0, 0.1):
        df = pyupbit.get_ohlcv(ticker, count=7)
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)

        df['ror'] = np.where(df['high'] > df['target'],
                             df['close'] / df['target'],
                             1)

        ror = df['ror'].cumprod()[-2]

        if best_ror < ror:
            best_ror = ror
            best_k = k

    return best_k, best_ror

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def find_best(list):
    b_coin = ""
    b_ror = 0
    b_k = 0.5
    ror = 0
    k = 0.5
    for i in list:
        try:
            k, ror = get_best(i)
            if ror > b_ror:
                b_ror = ror
                b_coin = i
                b_k = k
        except Exception as e:
            print(e)
    return b_coin, b_k
########################################################################

#암호화폐 목록
list_coin = pyupbit.get_tickers(fiat="KRW")

# 상승장 판단
best_coin, best_k = find_best(list_coin)
print("Best_Coin : ", best_coin)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(best_coin)
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(best_coin, best_k)
            ma15 = get_ma15(best_coin)
            current_price = get_current_price(best_coin)
            print("Current : ", current_price)
            print("Target : ", target_price)
            print("ma15 : ", ma15)
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order(best_coin, krw*0.9995)
            else:
                # 차선책 코인 찾기
                # list_coin에서 지금의 코인을 제거
                list_coin.remove(best_coin)
                best_coin, best_k = find_best(list_coin)
        else:
            btc = get_balance(best_coin[4:])
            if btc > (5000 / get_current_price(best_coin)):
                upbit.sell_market_order(best_coin, btc)
                # 코인 재설정
                list_coin = pyupbit.get_tickers(fiat="KRW")
                best_coin, best_k = find_best(list_coin)
            else:
                # 코인 재설정
                best_coin, best_k = find_best(list_coin)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)