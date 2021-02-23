# bitbank-websocket-adaptor

bitbankがWebSocketを介して公開している各種情報をrxを使ってリアルタイムに取得します

## 利用するための環境構築

エディター: Visual Studio Code

pythonバージョン: 3.8.1

`venv`で仮想環境を利用することを推奨します。<br/>
仮想環境のディレクトリ名は任意ですが、`envs`にするとVSCodeが認識してくれます。

```
> py -3.8 -m venv envs
```


`requirements.txt`をもとにモジュールをpip installします。

```
> pip install -r requirements.txt
```


[bitbankのリポジトリ](https://github.com/bitbankinc/python-bitbankcc)から`python-bitbankcc`をpip installします。

```
> pip install git+https://github.com/bitbankinc/python-bitbankcc.git
```


デフォルトではパブリックなWebAPIメソッドのみ利用する状態です。<br/>
プライベートなWebAPIメソッドも利用可能ですが、<br/>
その場合はbitbankよりAPIキーを発行し、bitbank_api.pyの__init__メソッド内に書き込んでください。

`main.py`を実行

```
> python main.py
```


デフォルトでは次のように、時刻とビットコインの最終売買価格の情報がリアルタイムに印字されます。

```
('2020-11-20 05:52:19', 'last buy: 1866990', 'last sell: 1866429', 'min ask: 1866423.0', 'max bid: 1866422.0')
```

## 表示したいデータを編集する

`mytrade.py`のmyTradeStreamにて表示させるデータを指定しています。<br/>
例えば`PriceLastBuyStream`はbitbankにおいてトレードされた最終買値です。<br/>
これらはすべて`Observable`型で、ここではストリームと呼ぶことにしています。


`mytrade.py`に記述できるストリームはstreams.pyに記述されているものです。


また、取得するペアはデフォルトでは`btc/jpy`ですが、<br/>
`parameters.py`にある定数`PAIR`の値を変更することでbitbankで公開されている別のペアを指定することも可能です。

## 所感

自分が実行して確認する分には、<br/>
bitbank取引所で表示されるよりも<br/>
早く値が更新されるように思いました(1秒から5秒ほど)。


単純に`python-bitbankcc`モジュールを使ったAPI連携をするよりも、<br/>
websocketを取り入れた本モジュールのほうが早いレスポンスを得られるため、<br/>
よりリアルタイムに情報を得たいBOTの開発などでの有用性が見込めると考えられます
