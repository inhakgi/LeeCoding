#해당 자료는 '파이스탁' 유튜브 채널의 교육자료를 참고하여 연습과 복습을 위해 만들어놓았습니다.
#자료가 문제가 될 경우에는 삭제조치 할 예정이오니 문제가 될 경우 아래 메일로 연락 바랍니다.
#hagibal@naver.com


# 연습문제(1)
# 1. 업비트는 마켓코드(예:KRW-BTC, BTC-ETH)를 통해 주문을 수행합니다. 앞서 제공한 REST API 코드를 사용해서 원화 시장에서 거래가 가능한 가상화폐의 마켓코드를 파이썬 리스트로 저장해보세요.
import requests

url = "https://api.upbit.com/v1/market/all"
resp = requests.get(url)
data = resp.json()

krw_tickers = []

for coin in data:
    ticker = coin['market'] # coin is dictionary, ("KRW-BTC...등등등")
    

    if ticker.startswith("KRW"): #만약 ticker에서 "KRW"로 시작하면
        krw_tickers.append(ticker) #krw_tickets에 넣어주시면 됩니다.

print(krw_tickers)
print(len(krw_tickers))


# 연습문제(2)
# 2. 업비트에서 비트코인 시장의 마켓코드를 pyupbit로 얻어온 후 목록과 개수를 출력해보세요.
import pyupbit

tickers = pyupbit.get_tickers(fiat="BTC") #() 하면 모든 시장, (fiat="KRW") 하면 원화시장
print(tickers)
print(len(tickers))


# 연습문제(3)
# 업비트에서 비트코인 시장의 마켓코드를 pyupbit로 얻어온 후 ohlcv를 이용해서 1분봉의 데이터를 가져오세요.
import pyupbit

df = pyupbit.get_ohlcv("ticker=KRW-BTC", interval="minute1", count=10) # "minute1" 뒤에 , count=1~200 을 넣을수 있는데 생략하면 최대(200)까지 불러옴.
print(df)
df.to_excel("minute1.xlsx") # excel로 받오 싶은 경우 

# 연습문제(4)
# 업비트에서 비트코인 시장의 마켓코드를 pyupbit로 얻어온 후 현재가격을 조회하세요.
import pyupbit

#한 종목만 조회하는 경우
price = pyupbit.get_current_price("KRW-BTC") 
print(price)

#여러 종목을 조회하는 경우
tickers = ["KRW-BTC", "KRW-XRP"]
price = pyupbit.get_current_price(tickers)
print(price)

# 연습문제(5)
# 업비트 거래소의 원화 시장에서 거래되고 있는 모든 가상회폐에 대한 현재가를 조회하고 이를 화면에 출력해보세요.
import pyupbit

krw_tickers = pyupbit.get_tickers(fiat="KRW") #(fiat="KRW") 는 원화시장만
#print(krw_tickers)

prices = pyupbit.get_current_price(krw_tickers) #current_price 을 이용하여 krw_tickets의 정보를 받아오겠다.
#print(prices)

# k value, v value로 정렬하고 싶으면
for k, v in prices.items():
    print(k, v)

import pyupbit
import pprint

f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip() # lines[0]: text 첫번째줄 .strip: 공백제거
secret = lines[1].strip() # lines[1]: text 두번째줄
f.close()

# upbit = pyupbit.Upbit(access, secret)
# balance = upbit.get_balance("KRW") #"ticker"에 balance를 통해 잔고를 확인 가능
# print(balance, type(balance))

upbit = pyupbit.Upbit(access, secret)
balances = upbit.get_balances() # ()경우 전체 조회 (Currency, balance, ..등등)
print(balances) 
#pprint.pprint(balances[0][0]) #좀더 깔끔하게 보려면 import pprint 후 pprint.pprint해서 설정

# currency: 화폐를 의미하는 영문 대문자코드
# balance: 주문가능 금액/수량
# locked: 주문 중 묶여있는 금액/수량
# avg_buy_price: 매수평균가
# avg_buy_price_modified: 매수평균가 수정 여부
# unit_currency: 평단가 기준 화폐


# 지정가 매수/매도 주문
import pyupbit
import pprint

f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip() # lines[0]: text 첫번째줄 .strip: 공백제거
secret = lines[1].strip() # lines[1]: text 두번째줄
f.close()

upbit = pyupbit.Upbit(access, secret) # upbit 객체 생성

xrp_price = pyupbit.get_current_price("KRW-XRP")
resp = upbit.buy_limit_order("KRW-XRP", 744, 10) #지정가, ticker, 금액, 수량(*최소수량 참고 할 것)
pprint.pprint(resp)
print 항목중에 'uuid' 가 '주문의 고유 아이디' 이므로 주문 취소를 할 때 참고 할 것.

xrp_balance = upbit.get_balance("KRW-XRP") # 내가 가지고 있는 xrp 수량 확인
resp = upbit.sell_limit_order("KRW-XRP", 700, xrp_balance) #지정가에 매도
print(resp)

시장가 매수 주문
buy_market_order(ticker, 주문가격)
주문가격은 원화임
KRW-XRP 마켓에서 XRP가 200원에서 거래되고 있을 때 주문가격을 1,000원을 입력하면 5XRP가 매수됨

import pyupbit
import pprint

f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip() # lines[0]: text 첫번째줄 .strip: 공백제거
secret = lines[1].strip() # lines[1]: text 두번째줄
f.close()

시장가 매수
upbit = pyupbit.Upbit(access, secret)
balances = upbit.get_balances() #잔고조회 해도되고 안해도됨
resp = upbit.buy_market_order("KRW-EOS", 10000)
pprint.pprint(resp)

시장가 매도
upbit = pyupbit.Upbit(access, secret)

eos_balance = upbit.get_balance("KRW-EOS") #보유중인 KRW-EOS 수량 확인
resp = upbit.sell_market_order("KRW-EOS", eos_balance)
pprint.pprint(resp)

# 주문 취소
import pyupbit
import pprint

f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip() # lines[0]: text 첫번째줄 .strip: 공백제거
secret = lines[1].strip() # lines[1]: text 두번째줄
f.close()
upbit = pyupbit.Upbit(access, secret)

uuid = "60aa23c9-86ac-4e04-b3e9-c952f94b80e8"
resp = upbit.cancel_order(uuid)
pprint.pprint(resp)

import pyupbit
import pprint
import time 
import datetime

krw_tickers1 = ["KRW-BTC"]
df1 = pyupbit.get_ohlcv(krw_tickers1, "minute5", count=5)

minute5ago = df1.iloc[-2] 
today = df1. iloc[-1]
minute5ago_range = minute5ago['high'] - minute5ago['low']
target = today['open'] + minute5ago_range * 0.5
print(target)

krw_tickers2 = ["KRW-EOS"]
df2 = pyupbit.get_ohlcv(krw_tickers2, "minute5", count=5)

minute5ago = df2.iloc[-2] 
today = df2. iloc[-1]
minute5ago_range = minute5ago['high'] - minute5ago['low']
target = today['open'] + minute5ago_range * 0.5
print(target)

symbols = ["KRW-BTC", "KRW-EOS"]
target_price = {}
for symbol in symbols:
  df = pyupbit.get_ohlcv(symbol, "minutes5", count=2)
  minutes5ago = df.iloc[-2]
  today = df.iloc[-1]
  minutes5ago_range = minutes5ago['high'] - minutes5ago['low']
  target_price[symbol] = today['open'] + minutes5ago_range * 0.5

print(target_price)


 while True:
    krw_tickers = pyupbit.get_tickers(fiat="KRW")
    price = pyupbit.get_current_price(krw_tickers)
    now = datetime.datetime.now() #현재시간 확인
    print(now)
    pprint.pprint(price) #현재시간과, 가격 보여줌
    time.sleep(1) #1초에 한번씩 현재가격 조회







