# bitbank-websocket-adaptor

bitbankがWebSocketを介して公開している各種情報をRxPYを使ってリアルタイムに取得します

## 課題と目的

仮想通貨のBot開発には取引所との高速なWebAPI接続が必要不可欠です。

昨今は取引所もHttp通信と比べてより早いレスポンスを返すWebSocket通信にて情報を公開することが増えました。
Http通信はリクエストのたびにコネクションを作成するのに対し、WebSocket通信は一度コネクションを確立したら
コネクションを切断することなくデータを受け取り続けることが可能です。

しかし、bitbankにおいては、セキュリティの観点から、WebSocketの通信に制限時間を設けており、それがたったの30秒となっています。
これでは1分足すら取得することができず、Bot開発に用いるには難点であると言えます。

今回はその課題を解決すべく、bitbankからWebSocketを介しつつ時間制限なしに情報を取得できるプログラムを作成しました。

## 利用するための環境構築

エディター: Visual Studio Code

pythonバージョン: 3.8.1

<br/>

`venv`で仮想環境を利用することを推奨します。<br/>
仮想環境のディレクトリ名は任意ですが、`envs`にするとVSCodeが認識してくれます。

```
> py -3.8 -m venv envs
```

<br/>

`requirements.txt`をもとにモジュールをpip installします。

```
> pip install -r requirements.txt
```

<br/>

[bitbankのリポジトリ](https://github.com/bitbankinc/python-bitbankcc)から`python-bitbankcc`をpip installします。

```
> pip install git+https://github.com/bitbankinc/python-bitbankcc.git
```

<br/>

デフォルトではパブリックなWebAPIメソッドのみ利用する状態です。<br/>
プライベートなWebAPIメソッドも利用可能ですが、<br/>
その場合はbitbankよりAPIキーを発行し、bitbank_api.pyの__init__メソッド内に書き込んでください。

`main.py`を実行

```
> python main.py
```

<br/>

デフォルトでは次のように、時刻とビットコインの最終売買価格の情報がリアルタイムに印字されます。

```
('2020-11-20 05:52:19', 'last buy: 1866990', 'last sell: 1866429', 'min ask: 1866423.0', 'max bid: 1866422.0')
```

## 表示したいデータを編集する

`mytrade.py`のmyTradeStreamにて表示させるデータを指定しています。<br/>
例えば`PriceLastBuyStream`はbitbankにおいてトレードされた最終買値です。<br/>
これらはすべて`Observable`型で、ここではストリームと呼ぶことにしています。

<br/>

`mytrade.py`に記述できるストリームはstreams.pyに記述されているものです。

<br/>

また、取得するペアはデフォルトでは`btc/jpy`ですが、<br/>
`parameters.py`にある定数`PAIR`の値を変更することでbitbankで公開されている別のペアを指定することも可能です。

## 所感

自分が実行して確認する分には、<br/>
bitbank取引所で表示されるよりも<br/>
早く値が更新されるように思いました(1秒から5秒ほど)。

<br/>

単純に`python-bitbankcc`モジュールを使ったAPI連携をするよりも、<br/>
WebSocketを取り入れた本モジュールのほうが早いレスポンスを得られるため、<br/>
よりリアルタイムに情報を得たいBOTの開発などでの有用性が見込めると考えられます。

## 工夫した点

- bitbank特有のWebSocketが30秒で切断されるという課題をRxPYを駆使することで解決しました。
  - RxPYについてはAngularの学習で得たRxJSの知見をもとに実装を進めました。
- また、再利用性の向上と関心の分離を目的として、modelsやstreamsなど役割ごとにソースを分割することを意識しました。
- さらに、なるべく型を指定することでドキュメントとしてのソースを書き上げることを意識しました。
  - これにより、ほかの人が見たり、自分が後日見たりしたときにもソースの意味を理解しやすいようにできると考えています。
- デフォルトではパブリックなWebAPIメソッドのみ利用するようにしていますが、プライベートメソッドにも
アクセスできるように実装しています。
  - これにより、Bot開発に関心があるほかの方でも好みの手法を組み立てやすいようにしています。
