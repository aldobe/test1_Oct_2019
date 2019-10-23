# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:51:15 2019

@author: EJ
"""

import websocket
import requests
import json

import csv  ## to write as csv file
from datetime import date   # pip install datetime
today = str(date.today().isoformat())
print(today)
# 중요한 값은 상수사용합니다.
SYMBOL_LIST_ENDPOINT = "https://www.bitmex.com/api/v1/instrument/active"
ENDPOINT = 'wss://www.bitmex.com/realtime'

def sendRequest(url):
    res = requests.get(url)
    contents = res.content.decode('utf-8')
    # python2에서는 contents = res.content만 적어도 됩니다.
    # python2에서는 res.content가 string으로 오지만
    # python3에서는 byte로 오기 때문에 디코딩이 필요합니다.

    # 대부분의 api는 json으로 반환되기 때문에 곧바로 json 라이브러리를 이용해 로드합니다
    json_contents = json.loads(contents)
    return json_contents

temp_list = []

def getBitmexSymbolList(contents):
    symbol_list = [
          pair['symbol']
          for pair in contents
         ]
    # contents안에 들어있는 각각의 아이템들 중에서
    # 키가 symbol인 것들만 리스트에 넣겠다는 뜻

    # formatted_list = [ 'tradeBin1m:{}'.format(symbol) for symbol in symbol_list]
    formatted_list = [ 'tradeBin1m:XBTUSD','tradeBin1m:ETHUSD']

    #  {"op":"subscribe", "args" : []}의 형식이었죠? args에 formatted_list를
    #  웹서버로 보내주면 bitmex에서 제공하는 모든 symbol에 대한 OHLCV를 얻을 수 있습니다.
    print(formatted_list)
    return {"op":"subscribe", "args" : formatted_list}

def on_message(ws, message):
    print(message)
    temp = json.loads(message)
    # print(temp["data"][0])
    temp_list.append(temp["data"][0])
    with open('test_{}.csv'.format(today),'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(temp_list[0].keys())
        for i in range(len(temp_list)):
            writer.writerow(temp_list[i].values())
    csvfile.close()
    # print(message)

def on_error(ws, error):
    print(error)
    ws.on_close(ws)

def on_close(ws):
    print("### closed ###")
    ws.close()

def on_open(ws):
    print("### open ###")
    contents = sendRequest(SYMBOL_LIST_ENDPOINT)
    symbols = getBitmexSymbolList(contents)
    # temp_list.append(symbols)
    ws.send(json.dumps(symbols))




def run(endpoint):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(endpoint,
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.run_forever()

if __name__ == "__main__":
    run(ENDPOINT)
