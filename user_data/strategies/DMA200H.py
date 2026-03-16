from freqtrade.strategy import IStrategy
import talib.abstract as ta
import pandas as pd
from technical.qtpylib import crossed_above, crossed_below


class DMA200H(IStrategy):
    timeframe = '1d'
    startup_candle_count = 210

    minimal_roi = {"0": 10}
    stoploss = -0.99

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe['sma200'] = ta.SMA(dataframe['close'], timeperiod=200)
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            crossed_above(dataframe['close'], dataframe['sma200']),
            'buy'
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            crossed_below(dataframe['close'], dataframe['sma200']),
            'sell'
        ] = 1
        return dataframe
