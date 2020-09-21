# 株探のスクレイピング

## price.py
株探の時系列データのページをスクレイピングし、下記を出力します。

- price_[銘柄ーコード].csv  
日付、始値、高値、安値、終値、前日比、前日比%、売買高

## price_today.py
当日分の価格データを取得します。
- price_[銘柄コード]_YYYYMMDD.csv  
日付、始値、高値、安値、終値、前日比、前日比%、売買高

## pbr.py
各銘柄のPBRを取得します。
- pbr.csv  
銘柄コード, PBR

## industry.py
株探の各銘柄の業種を取得します。
- industry.csv  
銘柄コード、業種

## sort.py
取得データを時系列の昇順にソートします。
