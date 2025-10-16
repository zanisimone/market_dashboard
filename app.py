import os
from datetime import datetime, timedelta
from dateutil import parser as dtparser
from typing import Optional, Tuple, List

import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

@st.cache_data(show_spinner=False)
def fetch_next_earnings_date(ticker: str) -> Tuple[Optional[datetime], str]:
    """
    Fetch the next earnings date for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Returns:
        Tuple[Optional[datetime], str]: Next earnings date and status ('confirmed', 'estimated', 'unknown', or 'error')
    """
    try:
        tk = yf.Ticker(ticker)
        cal = tk.calendar
        
        if isinstance(cal, pd.DataFrame) and not cal.empty:
            if 'Earnings Date' in cal.index:
                dt = cal.loc['Earnings Date'].values[0]
                if pd.isna(dt):
                    return None, "unknown"
                dt_py = pd.to_datetime(dt).to_pydatetime()
                return dt_py, "estimated"
        
        ed = tk.earnings_dates
        if isinstance(ed, pd.DataFrame) and not ed.empty:
            # Fix timezone comparison issue
            today = pd.Timestamp.today().normalize()
            # Convert today to the same timezone as earnings dates if needed
            if ed.index.tz is not None:
                today = today.tz_localize('UTC').tz_convert(ed.index.tz)
            
            future = ed[ed.index >= today]
            if not future.empty:
                dt_py = future.index[0].to_pydatetime()
                flag = future.iloc[0].get("EP", "estimated")
                return dt_py, str(flag)
        
        return None, "unknown"
    except Exception as e:
        return None, "error"

def parse_positions_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse and normalize the positions CSV data.
    
    Args:
        df (pd.DataFrame): Raw CSV data with required columns: date, ticker, notional, type, source
        
    Returns:
        pd.DataFrame: Cleaned and normalized positions data
        
    Raises:
        ValueError: If required columns are missing
    """
    required = ["date", "ticker", "notional", "type", "source"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df.copy()
    out["date"] = out["date"].apply(lambda x: dtparser.parse(str(x)).date())
    out["ticker"] = out["ticker"].str.upper().str.strip()
    out["notional"] = pd.to_numeric(out["notional"], errors="coerce")
    out["type"] = out["type"].astype(str)
    out["source"] = out["source"].astype(str)
    if "notes" not in out.columns:
        out["notes"] = ""
    out = out.dropna(subset=["notional", "ticker", "date"])
    return out

def make_earnings_table(tickers: List[str]) -> pd.DataFrame:
    """
    Create a table of upcoming earnings dates for given tickers.
    
    Args:
        tickers (List[str]): List of stock ticker symbols
        
    Returns:
        pd.DataFrame: Earnings data with ticker, date, status, and days until earnings
    """
    records = []
    for t in tickers:
        dt, flag = fetch_next_earnings_date(t)
        records.append({
            "ticker": t,
            "next_earnings": dt,
            "status": flag,
            "days_to": (dt.date() - datetime.today().date()).days if isinstance(dt, datetime) else None,
        })
    df = pd.DataFrame(records).sort_values(by=["next_earnings"], ascending=True, na_position="last")
    return df

def style_earnings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply styling to earnings table.
    
    Args:
        df (pd.DataFrame): Earnings data
        
    Returns:
        pd.DataFrame: Styled earnings data
    """
    return df.copy()

st.set_page_config(page_title="Earnings & Big Positioning", layout="wide")
st.title("📅 Market Dashboard")

with st.sidebar:
    st.header("⚙️ Settings")
    tickers_text = st.text_area(
        "Tickers (comma-separated)", 
        value="AAPL, MSFT, NVDA, AMZN, META"
    )
    tickers = [t.strip().upper() for t in tickers_text.split(",") if t.strip()]

    st.markdown("---")
    st.markdown("**Upload positions CSV**")
    uploaded = st.file_uploader("CSV with columns: date,ticker,notional,type,source,notes (optional)", type=["csv"])
    if st.button("Download CSV template"):
        sample = pd.DataFrame({
            "date": [datetime.today().date().isoformat()],
            "ticker": ["AAPL"],
            "notional": [15000000],
            "type": ["block_trade"],
            "source": ["manual"],
            "notes": ["dark pool print"]
        })
        sample.to_csv("positions_template.csv", index=False)
        with open("positions_template.csv", "rb") as f:
            st.download_button("Download positions_template.csv", data=f, file_name="positions_template.csv")




st.subheader("🧾 Upcoming Earnings")
if tickers:
    e_df = make_earnings_table(tickers)
    
    def highlight(row):
        if pd.isna(row["next_earnings"]):
            return ["background-color: #eee"] * len(row)
        days = row["days_to"]
        if days is None:
            return [""] * len(row)
        if days <= 7:
            return ["background-color: #ffe5e5"] * len(row)
        if days <= 14:
            return ["background-color: #fff3cd"] * len(row)
        return [""] * len(row)
    
    styled_df = e_df.style.apply(highlight, axis=1)
    st.dataframe(styled_df, width='stretch', hide_index=True)
else:
    st.info("Enter one or more tickers in the sidebar.")



notional_min = 5_000_000.0

st.subheader("📈 Large Positions")
pos_df = None
if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        pos_df = parse_positions_csv(raw)
        pos_df = pos_df[pos_df["notional"] >= notional_min]
        st.dataframe(pos_df.sort_values("date"), width='stretch')
    except Exception as e:
        st.error(f"Error parsing CSV: {e}")
else:
    st.caption("Upload a CSV to view positions.")

st.subheader("🗓️ Timeline")
timeline_items = []

if tickers:
    for _, r in e_df.iterrows():
        if pd.isna(r["next_earnings"]):
            continue
        timeline_items.append({
            "ticker": r["ticker"],
            "event": "Earnings",
            "date": r["next_earnings"].date(),
            "size": None,
            "details": r["status"]
        })

if pos_df is not None and not pos_df.empty:
    for _, r in pos_df.iterrows():
        timeline_items.append({
            "ticker": r["ticker"],
            "event": r["type"],
            "date": r["date"],
            "size": r["notional"],
            "details": r["source"]
        })

if timeline_items:
    tdf = pd.DataFrame(timeline_items)
    tdf["date"] = pd.to_datetime(tdf["date"])
    tdf["label"] = tdf["event"] + " · " + tdf["ticker"] + tdf["details"].apply(lambda x: f" ({x})" if x else "")
    
    # Handle size column - replace None with a default size for earnings events
    tdf["size"] = tdf["size"].fillna(10)  # Default size for earnings events
    
    fig = px.scatter(
        tdf,
        x="date",
        y="ticker",
        size="size",
        color="event",
        hover_data=["details", "size"],
        title="Events Over Time"
    )
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.update_layout(height=450, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, config={"displayModeBar": True})
else:
    st.caption("No events to display (add tickers or upload positions).")
    

with st.expander("Future Extensions (API Adapters)"):
    st.markdown("""
- **Alternative earnings provider:** Finnhub/Polygon/EODHD.
- **Unusual options / dark pool:** with dedicated APIs. Integrate an adapter that returns a DataFrame with the **same schema** as the CSV.
- **Cache & Scheduler:** update data every X hours and persist to disk.
- **Alerts:** highlight tickers with earnings <= 7 days or positions > high threshold.
""")
