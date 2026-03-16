# 200-SMA Crossover Strategy

## Project Overview
Algorithmic trading system using a 200-period Simple Moving Average crossover strategy, built with Freqtrade.

- **BUY** when price crosses above the 200 SMA
- **SELL** when price crosses below the 200 SMA

## Tech Stack
- **Freqtrade** — strategy engine, backtesting, hyperopt
- **Python** — core language
- **TA-Lib** — technical indicators (SMA, RSI, etc.)
- **Pandas** — data manipulation
- **qtpylib** — crossover detection helpers
- **Binance public API** — free historical OHLCV data

## Project Structure
```
E:/200DMA/
├── CLAUDE.md
└── user_data/
    └── strategies/
        └── DMA200H.py       # Main strategy file
```

## Key Commands
```bash
# Download historical data
freqtrade download-data --exchange binance --timeframe 1Day --pairs BTC/USDT --timerange 20180101-

# Run backtest
freqtrade backtesting --strategy DMA200H

# Run backtest with date range
freqtrade backtesting --strategy DMA200H --timerange 20200101-20240101
```

## Notes
- Strategy file: `user_data/strategies/DMA200H.py`
- `startup_candle_count = 210` ensures SMA is fully formed before trading
- Max drawdown target: < 20% (excellent), 20-40% (acceptable)
- No paid data or tools required — everything runs locally
