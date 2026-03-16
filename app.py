import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import zipfile
import json

# --- Page Config ---
st.set_page_config(
    page_title="Dr Farooq Trading App",
    page_icon="https://em-content.zobj.net/source/twitter/408/robot_1f916.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Cyberpunk Theme CSS ---
CYBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

/* Root Variables */
:root {
    --neon-cyan: #00f0ff;
    --neon-magenta: #ff00de;
    --neon-green: #39ff14;
    --neon-yellow: #f0ff00;
    --neon-orange: #ff6600;
    --neon-red: #ff0040;
    --dark-bg: #0a0a0f;
    --dark-card: #0d0d1a;
    --dark-surface: #12122a;
    --grid-line: rgba(0, 240, 255, 0.06);
}

/* Main Background */
.stApp {
    background: linear-gradient(180deg, #0a0a0f 0%, #0d0d1a 40%, #0a0a0f 100%) !important;
    background-attachment: fixed !important;
}

/* Scanline overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 240, 255, 0.015) 2px,
        rgba(0, 240, 255, 0.015) 4px
    );
    pointer-events: none;
    z-index: 999;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1rem !important;}

/* Hero Title */
.cyber-hero {
    text-align: center;
    padding: 2rem 1rem 0.5rem 1rem;
    position: relative;
}

.cyber-hero h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 3.2rem !important;
    font-weight: 900 !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    background: linear-gradient(90deg, #00f0ff 0%, #ff00de 50%, #00f0ff 100%) !important;
    background-size: 200% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: gradient-shift 3s ease infinite !important;
    margin-bottom: 0 !important;
    text-shadow: none !important;
    line-height: 1.2 !important;
}

.cyber-subtitle {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1.1rem !important;
    color: #39ff14 !important;
    letter-spacing: 6px !important;
    text-transform: uppercase !important;
    text-align: center !important;
    margin-top: 0.3rem !important;
    text-shadow: 0 0 10px rgba(57, 255, 20, 0.5) !important;
}

.cyber-tagline {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    color: #f0ff00 !important;
    text-align: center !important;
    margin-top: 0.5rem !important;
    letter-spacing: 3px !important;
    text-shadow: 0 0 20px rgba(240, 255, 0, 0.4) !important;
}

@keyframes gradient-shift {
    0% { background-position: 0% center; }
    50% { background-position: 100% center; }
    100% { background-position: 0% center; }
}

/* Glowing separator */
.cyber-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00f0ff, #ff00de, #00f0ff, transparent);
    margin: 1.5rem 0;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.05) 0%, rgba(255, 0, 222, 0.05) 100%) !important;
    border: 1px solid rgba(0, 240, 255, 0.2) !important;
    border-radius: 4px !important;
    padding: 1rem !important;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.08), inset 0 0 15px rgba(0, 240, 255, 0.03) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(0, 240, 255, 0.5) !important;
    box-shadow: 0 0 25px rgba(0, 240, 255, 0.15), inset 0 0 20px rgba(0, 240, 255, 0.05) !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: rgba(0, 240, 255, 0.7) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'Share Tech Mono', monospace !important;
}

/* Section Headers */
.cyber-section {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #00f0ff !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 0.8rem 0 !important;
    border-bottom: 1px solid rgba(0, 240, 255, 0.2) !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.3) !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: rgba(0, 240, 255, 0.03) !important;
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 4px !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    color: #00f0ff !important;
    letter-spacing: 1px !important;
}

[data-testid="stExpander"] p, [data-testid="stExpander"] li {
    font-family: 'Rajdhani', sans-serif !important;
    color: rgba(255, 255, 255, 0.8) !important;
    font-size: 1rem !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 240, 255, 0.15) !important;
    border-radius: 4px !important;
}

/* Slider */
[data-testid="stSlider"] label {
    font-family: 'Share Tech Mono', monospace !important;
    color: rgba(0, 240, 255, 0.7) !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}

.stSlider > div > div {
    background: rgba(0, 240, 255, 0.2) !important;
}

/* Plotly charts background */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

/* Summary table labels */
.cyber-table-label {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.9rem !important;
    color: #ff00de !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 0 0 8px rgba(255, 0, 222, 0.3) !important;
}

/* Footer */
.cyber-footer {
    text-align: center;
    padding: 1.5rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: rgba(0, 240, 255, 0.4);
    letter-spacing: 2px;
    border-top: 1px solid rgba(0, 240, 255, 0.1);
    margin-top: 2rem;
}

/* Pulse animation for profit */
@keyframes neon-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.pulse-green {
    animation: neon-pulse 2s ease-in-out infinite;
}
</style>
"""

st.markdown(CYBER_CSS, unsafe_allow_html=True)

# --- Paths ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "user_data" / "data" / "bybit"
RESULTS_DIR = BASE_DIR / "user_data" / "backtest_results"

# --- Cyberpunk Plotly Template ---
CYBER_LAYOUT = dict(
    paper_bgcolor="rgba(10, 10, 15, 0)",
    plot_bgcolor="rgba(13, 13, 26, 0.8)",
    font=dict(family="Share Tech Mono, monospace", color="rgba(0, 240, 255, 0.7)", size=11),
)


@st.cache_data
def load_ohlcv():
    feather_file = DATA_DIR / "BTC_USDT-1d.feather"
    df = pd.read_feather(feather_file)
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df.sort_values("date").reset_index(drop=True)
    df["sma200"] = df["close"].rolling(window=200).mean()
    return df


@st.cache_data
def load_backtest():
    zips = sorted(RESULTS_DIR.glob("*.zip"))
    if not zips:
        return None
    with zipfile.ZipFile(zips[-1]) as z:
        json_files = [f for f in z.namelist() if f.endswith(".json") and "config" not in f and "meta" not in f]
        if not json_files:
            return None
        data = json.loads(z.read(json_files[0]))
    return data["strategy"]["DMA200H"]


def build_price_chart(df, trades):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.78, 0.22],
    )

    # Candlestick - cyberpunk colors
    fig.add_trace(
        go.Candlestick(
            x=df["date"], open=df["open"], high=df["high"],
            low=df["low"], close=df["close"], name="BTC/USDT",
            increasing_line_color="#39ff14", increasing_fillcolor="rgba(57, 255, 20, 0.3)",
            decreasing_line_color="#ff0040", decreasing_fillcolor="rgba(255, 0, 64, 0.3)",
        ),
        row=1, col=1,
    )

    # SMA 200 - neon magenta glow
    fig.add_trace(
        go.Scatter(
            x=df["date"], y=df["sma200"], name="200 SMA",
            line=dict(color="#ff00de", width=2.5),
        ),
        row=1, col=1,
    )

    # Buy signals - neon cyan
    if len(trades) > 0:
        fig.add_trace(
            go.Scatter(
                x=trades["open_date"], y=trades["open_rate"],
                mode="markers", name="LONG ENTRY",
                marker=dict(symbol="triangle-up", size=16, color="#00f0ff",
                            line=dict(width=2, color="#00f0ff")),
                text=[f"ENTRY @ ${r:,.0f}" for r in trades["open_rate"]],
                hovertemplate="%{text}<extra></extra>",
            ),
            row=1, col=1,
        )

        # Sell signals - neon yellow
        fig.add_trace(
            go.Scatter(
                x=trades["close_date"], y=trades["close_rate"],
                mode="markers", name="EXIT SIGNAL",
                marker=dict(symbol="triangle-down", size=16, color="#f0ff00",
                            line=dict(width=2, color="#f0ff00")),
                text=[f"EXIT @ ${r:,.0f} [{p:+.1f}%]" for r, p in
                      zip(trades["close_rate"], trades["profit_ratio"] * 100)],
                hovertemplate="%{text}<extra></extra>",
            ),
            row=1, col=1,
        )

    # Volume bars - cyberpunk
    colors = ["rgba(57, 255, 20, 0.4)" if c >= o else "rgba(255, 0, 64, 0.4)"
              for c, o in zip(df["close"], df["open"])]
    fig.add_trace(
        go.Bar(x=df["date"], y=df["volume"], name="Volume",
               marker_color=colors, showlegend=False),
        row=2, col=1,
    )

    fig.update_layout(
        height=700,
        xaxis_rangeslider_visible=False,
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
            bgcolor="rgba(13, 13, 26, 0.8)", bordercolor="rgba(0, 240, 255, 0.2)", borderwidth=1,
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        **CYBER_LAYOUT,
    )
    fig.update_yaxes(title_text="PRICE (USDT)", row=1, col=1,
                     title_font=dict(color="#00f0ff", size=11),
                     gridcolor="rgba(0, 240, 255, 0.06)")
    fig.update_yaxes(title_text="VOL", row=2, col=1,
                     title_font=dict(color="#00f0ff", size=11),
                     gridcolor="rgba(0, 240, 255, 0.06)")
    fig.update_xaxes(gridcolor="rgba(0, 240, 255, 0.06)", row=1, col=1)
    fig.update_xaxes(gridcolor="rgba(0, 240, 255, 0.06)", row=2, col=1)
    return fig


def build_equity_chart(trades, starting_balance):
    equity = [starting_balance]
    dates = [trades["open_date"].iloc[0]]
    balance = starting_balance
    for _, t in trades.iterrows():
        balance += t["profit_abs"]
        equity.append(balance)
        dates.append(t["close_date"])

    eq_df = pd.DataFrame({"date": dates, "balance": equity})
    eq_df["peak"] = eq_df["balance"].cummax()
    eq_df["drawdown_pct"] = (eq_df["balance"] - eq_df["peak"]) / eq_df["peak"] * 100

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.7, 0.3],
    )

    # Equity - neon cyan fill
    fig.add_trace(
        go.Scatter(
            x=eq_df["date"], y=eq_df["balance"], name="BALANCE",
            fill="tozeroy",
            line=dict(color="#00f0ff", width=2.5),
            fillcolor="rgba(0, 240, 255, 0.08)",
            hovertemplate="$%{y:,.2f}<extra></extra>",
        ),
        row=1, col=1,
    )

    # Peak line
    fig.add_trace(
        go.Scatter(
            x=eq_df["date"], y=eq_df["peak"], name="PEAK",
            line=dict(color="rgba(255, 0, 222, 0.3)", width=1, dash="dot"),
        ),
        row=1, col=1,
    )

    # Drawdown - neon red
    fig.add_trace(
        go.Scatter(
            x=eq_df["date"], y=eq_df["drawdown_pct"], name="DRAWDOWN",
            fill="tozeroy",
            line=dict(color="#ff0040", width=1.5),
            fillcolor="rgba(255, 0, 64, 0.15)",
            hovertemplate="%{y:.2f}%<extra></extra>",
        ),
        row=2, col=1,
    )

    fig.update_layout(
        height=480,
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
            bgcolor="rgba(13, 13, 26, 0.8)", bordercolor="rgba(0, 240, 255, 0.2)", borderwidth=1,
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        **CYBER_LAYOUT,
    )
    fig.update_yaxes(title_text="BALANCE (USDT)", row=1, col=1,
                     title_font=dict(color="#00f0ff", size=11),
                     gridcolor="rgba(0, 240, 255, 0.06)")
    fig.update_yaxes(title_text="DRAWDOWN %", row=2, col=1,
                     title_font=dict(color="#ff0040", size=11),
                     gridcolor="rgba(0, 240, 255, 0.06)")
    fig.update_xaxes(gridcolor="rgba(0, 240, 255, 0.06)", row=1, col=1)
    fig.update_xaxes(gridcolor="rgba(0, 240, 255, 0.06)", row=2, col=1)
    return fig


# ============================================================
# MAIN APP
# ============================================================

# --- Hero Header ---
st.markdown("""
<div class="cyber-hero">
    <h1>DR FAROOQ TRADING APP</h1>
    <div class="cyber-subtitle">200-SMA Crossover Strategy</div>
    <div class="cyber-tagline">TRIPLE YOUR PROFITS</div>
</div>
<div class="cyber-divider"></div>
""", unsafe_allow_html=True)

# Load data
df = load_ohlcv()
bt = load_backtest()

if bt is None:
    st.error("NO BACKTEST DATA FOUND. SYSTEM OFFLINE.")
    st.stop()

trades = pd.DataFrame(bt["trades"])
trades["open_date"] = pd.to_datetime(trades["open_date"], utc=True)
trades["close_date"] = pd.to_datetime(trades["close_date"], utc=True)

# --- Metrics Row ---
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("TOTAL PROFIT", f"${bt['profit_total_abs']:,.0f}", f"+{bt['profit_total'] * 100:.1f}%")
col2.metric("CAGR", f"{bt['cagr'] * 100:.1f}%")
col3.metric("MAX DRAWDOWN", f"{bt['max_drawdown_account'] * 100:.1f}%")
col4.metric("WIN RATE", f"{bt['winrate'] * 100:.1f}%")
col5.metric("PROFIT FACTOR", f"{bt['profit_factor']:.2f}")
col6.metric("TOTAL TRADES", f"{bt['total_trades']}")

st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)

# --- Strategy Explanation ---
with st.expander("// SYSTEM PROTOCOL: HOW THE STRATEGY WORKS", expanded=False):
    st.markdown("""
**The 200-SMA Crossover** is a battle-tested trend-following algorithm:

- **LONG ENTRY** -- Price crosses **above** the 200-day Simple Moving Average
- **EXIT SIGNAL** -- Price crosses **below** the 200-day SMA

**Why it dominates:**
- Captures massive uptrends while sidestepping prolonged crashes
- Low win rate is by design -- winners are 50x larger than losers
- Simple, robust, zero-emotion execution

**Parameters:**
- Timeframe: 1 Day
- SMA Period: 200
- Stop Loss: None (the SMA IS the exit)
""")

# --- Price Chart ---
st.markdown('<div class="cyber-section">PRICE CHART & SIGNALS</div>', unsafe_allow_html=True)

min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.slider(
    "TEMPORAL RANGE",
    min_value=min_date, max_value=max_date,
    value=(pd.Timestamp("2022-01-01").date(), max_date),
    format="YYYY-MM-DD",
)
mask = (df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])
trade_mask = (trades["open_date"].dt.date >= date_range[0]) & (trades["close_date"].dt.date <= date_range[1])

fig_price = build_price_chart(df[mask], trades[trade_mask])
st.plotly_chart(fig_price, use_container_width=True)

# --- Equity Curve ---
st.markdown('<div class="cyber-section">EQUITY CURVE & DRAWDOWN</div>', unsafe_allow_html=True)
fig_equity = build_equity_chart(trades, bt["starting_balance"])
st.plotly_chart(fig_equity, use_container_width=True)

# --- Summary Metrics ---
st.markdown('<div class="cyber-section">PERFORMANCE MATRIX</div>', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    st.markdown('<div class="cyber-table-label">// RETURNS</div>', unsafe_allow_html=True)
    summary_return = {
        "Starting Balance": f"${bt['starting_balance']:,.2f}",
        "Final Balance": f"${bt['final_balance']:,.2f}",
        "Total Profit": f"${bt['profit_total_abs']:,.2f}",
        "Total Return": f"+{bt['profit_total'] * 100:.1f}%",
        "CAGR": f"{bt['cagr'] * 100:.1f}%",
        "Avg Profit/Trade": f"{bt['profit_mean'] * 100:.2f}%",
        "Best Trade": f"+{trades['profit_ratio'].max() * 100:.1f}%",
        "Worst Trade": f"{trades['profit_ratio'].min() * 100:.1f}%",
    }
    st.dataframe(
        pd.DataFrame(summary_return.items(), columns=["Metric", "Value"]),
        hide_index=True, use_container_width=True,
    )

with right:
    st.markdown('<div class="cyber-table-label">// RISK ANALYSIS</div>', unsafe_allow_html=True)
    summary_risk = {
        "Max Drawdown": f"{bt['max_drawdown_account'] * 100:.1f}%",
        "Drawdown Duration": f"{bt['drawdown_duration']}",
        "Sharpe Ratio": f"{bt['sharpe']:.2f}",
        "Sortino Ratio": f"{bt['sortino']:.2f}",
        "Calmar Ratio": f"{bt['calmar']:.2f}",
        "Profit Factor": f"{bt['profit_factor']:.2f}",
        "Win Rate": f"{bt['winrate'] * 100:.1f}%",
        "SQN": f"{bt['sqn']:.2f}",
    }
    st.dataframe(
        pd.DataFrame(summary_risk.items(), columns=["Metric", "Value"]),
        hide_index=True, use_container_width=True,
    )

# --- Trade List ---
st.markdown('<div class="cyber-section">TRADE LOG</div>', unsafe_allow_html=True)
trade_display = trades[["pair", "open_date", "close_date", "open_rate", "close_rate",
                         "profit_ratio", "profit_abs", "trade_duration"]].copy()
trade_display["open_date"] = trade_display["open_date"].dt.strftime("%Y-%m-%d")
trade_display["close_date"] = trade_display["close_date"].dt.strftime("%Y-%m-%d")
trade_display["profit_ratio"] = (trade_display["profit_ratio"] * 100).round(2)
trade_display["trade_duration"] = (trade_display["trade_duration"] / 60 / 24).round(1)
trade_display.columns = ["Pair", "Entry Date", "Exit Date", "Entry Price",
                          "Exit Price", "Profit %", "Profit USDT", "Duration (days)"]
st.dataframe(trade_display, hide_index=True, use_container_width=True)

# --- Footer ---
st.markdown("""
<div class="cyber-footer">
    <div class="cyber-divider"></div>
    DR FAROOQ TRADING APP // 200-SMA CROSSOVER PROTOCOL // BTC/USDT DAILY // POWERED BY FREQTRADE & STREAMLIT
</div>
""", unsafe_allow_html=True)
