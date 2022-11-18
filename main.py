import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd  
from pandas_datareader import data as pdr 
import datetime
import yfinance as yf
import numpy as np
 
#アクティブアドレスのデータ
#https://data.nasdaq.com/data/BCHAIN/NADDU-bitcoin-number-of-unique-bitcoin-addresses-used

# 無地のキャンバスを作成する
fig = plt.figure()
time_scale = 'M' #def M

# yの配列を作成する
x = []
y1 = []
y2 = []

def get_active_address(dir = 'BCHAIN-NADDU.csv'):
  #アクティブアドレス（CSV）の読み込み
  active_address = pd.read_csv(dir,index_col=0)
  active_address.index = pd.to_datetime(active_address.index)
  #データを反転
  active_address = active_address.iloc[::-1]
  agg_dict = {"Value": "sum"}
  # 月足に変換する
  active_address = active_address.resample(time_scale).agg(agg_dict)
  return active_address

def get_hasurate(dir = 'BCHAIN-HRATE.csv'):
  #アクティブアドレス（CSV）の読み込み
  active_address = pd.read_csv(dir,index_col=0)
  active_address.index = pd.to_datetime(active_address.index)
  #データを反転
  active_address = active_address.iloc[::-1]
  agg_dict = {"Value": "sum"}
  # 月足に変換する
  active_address = active_address.resample(time_scale).agg(agg_dict)
  return active_address


def get_btc_chart(tickers = ['BTC-USD'],start = "2015-01-01",end = "2022-11-16"):
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
 
    #月足に変換する
    crypto_data = crypto_data .resample(time_scale).agg(agg_dict)
    return crypto_data

def AnimationUpdater(frame):
  # figureオブジェクトを作成
  # 表示されているグラフをリセット
  plt.cla()
  y1.append(btc_chart['Adj Close'][frame])
  y2.append(btc_chart['Value'][frame])
  x.append(btc_chart.index[frame])

  # yのグラフを表示
  ax1.plot(x,y1,color='forestgreen',label='BTC_PRICE')
  ax2.plot(x,y2,color='Orange',label='HASH_RATE')
  
def main():
  global btc_chart, fig, ax1, ax2
  #グラフの箱を用意
  ax1 = fig.subplots()
  ax2 = ax1.twinx()

  #btcの価格を取得
  btc_chart = get_btc_chart()

  #アクティブアドレス数/ハッシュレートを取得
  data = get_hasurate()

  #連結
  btc_chart = pd.concat([btc_chart, data], axis=1).dropna()

  #最終月のデータを削除（ハッシュレートやアクティブアドレスの計算が月末までにならないと総和が取れないため）
  btc_chart = btc_chart[:-1]

  #動的なグラフの作成
  ani = animation.FuncAnimation(fig,AnimationUpdater, interval=500)

  #Xラベルを45度傾ける
  ax1.tick_params(axis='x', labelrotation=45)
  
  #表示
  plt.show()

  #保存
  #ani.save('btc.gif', writer='pillow')

if __name__ == "__main__": 
  main()