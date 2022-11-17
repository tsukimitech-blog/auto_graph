import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd  
from pandas_datareader import data as pdr 
import datetime
import yfinance as yf
import numpy as np
 


# 無地のキャンバスを作成する
fig = plt.figure()

# yの配列を作成する
x = []
y = []

def get_btc_chart(tickers = ['BTC-USD'],start = "2015-01-01",end = datetime.date.today()):
    #Yahoofinanceから取得するように設定
    yf.pdr_override()

    #データの取得を実行
    crypto_data = pdr.get_data_yahoo(tickers, start, end)
    # カラムごとの計算手法を指定
    agg_dict = {
        "Open": "first", 
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Adj Close":"last",
        "Volume": "sum"
        }
 
# 週足に変換する
    crypto_data = crypto_data .resample("M").agg(agg_dict)
    print(crypto_data)

    return crypto_data

def AnimationUpdater(frame):
  # 表示されているグラフをリセット
  plt.cla()
  

  # 100個以上のデータは削除する (FIFO)
  #if len(y) >= 100:
    # 配列の先頭を削除
    #del y[0]
  
  y.append(btc_chart['Adj Close'][frame])
  x.append(btc_chart.index[frame])

  # yのグラフを表示
  plt.plot(x,y)
  plt.xticks(rotation=45)
btc_chart = get_btc_chart()
ani = animation.FuncAnimation(fig,AnimationUpdater, interval=5)

plt.show()