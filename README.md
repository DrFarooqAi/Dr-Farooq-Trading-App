# DR FAROOQ TRADING APP

### 200-SMA Crossover Strategy | Triple Your Profits

A cyberpunk-themed algorithmic trading dashboard built with **Freqtrade** and **Streamlit**, backtesting a classic 200-day Simple Moving Average crossover strategy on **BTC/USDT**.

---

## Backtest Results (Jan 2022 - Mar 2026)

| Metric | Value |
|--------|-------|
| Starting Balance | $1,000 |
| Final Balance | $2,903 |
| Total Profit | +190.4% |
| CAGR | 29.5% |
| Max Drawdown | 9.99% |
| Profit Factor | 3.78 |
| Total Trades | 16 |
| Win Rate | 31.2% |

---

## Strategy

- **BUY** when price crosses above the 200-day SMA
- **SELL** when price crosses below the 200-day SMA

Simple, robust, and time-tested. Low win rate by design — winners are massive, losers are tiny.

---

## Tech Stack

- **Freqtrade** — Strategy engine & backtesting
- **Python** — Core language
- **TA-Lib** — Technical indicators
- **Streamlit** — Interactive dashboard
- **Plotly** — Charts & visualizations
- **Bybit** — Free historical data

---

## Run Locally

```bash
# Clone
git clone https://github.com/DrFarooqAi/Dr-Farooq-Trading-App.git
cd Dr-Farooq-Trading-App

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

---

## Project Structure

```
Dr-Farooq-Trading-App/
├── app.py                          # Streamlit cyberpunk dashboard
├── config.json                     # Freqtrade configuration
├── requirements.txt                # Python dependencies
└── user_data/
    ├── strategies/
    │   └── DMA200H.py              # 200-SMA strategy
    ├── data/bybit/                 # Historical BTC/USDT data
    ├── backtest_results/           # Backtest output
    └── plot/                       # Interactive HTML charts
```

---

## License

Open source. Free to use, modify, and share.

---

**Built by Dr Farooq | Powered by Freqtrade & Streamlit**
