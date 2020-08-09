# 株探のスクレイピング

## price.py
株探の時系列データのページをスクレイピングし、下記を出力します。

- [銘柄コード]_YYYYMMDD_price.csv  
始値、終値、高値、安値

- [銘柄コード]_YYYYMMDD_pbr.csv  
各銘柄のPBR

## industry.py
株探の各銘柄の業種を取得します。

- industry.csv  
銘柄コード、業種