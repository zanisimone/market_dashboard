# Market Dashboard — Earnings & Positioning Monitor

Market Dashboard is a lightweight, Streamlit-based web app designed to visualize upcoming earnings dates and large market positioning events across major stocks. It provides a clean, minimal interface for traders, analysts, and portfolio managers who want to stay aware of catalysts and institutional activity at a glance.

## Current Features (MVP)

**Earnings Tracker:**
- Automatically fetches the next earnings date for each ticker using Yahoo Finance (yfinance), with estimated or confirmed status.

**Positioning Monitor:**
- Allows users to upload a CSV of large trades or block positions (e.g., dark pool prints, options sweeps, 13F changes).
- Entries are filtered by notional value and visualized in both a table and a timeline.

**Interactive Timeline:**
- A Plotly-based scatter timeline displaying both earnings events and positioning data — all color-coded by event type.

**Minimal & Fast UI:**
- Built in Streamlit, with caching for performance, and a clean layout optimized for clarity.

## Vision

This project aims to evolve into a comprehensive Market Intelligence Dashboard that integrates cross-asset data, macroeconomic indicators, and liquidity metrics in one unified visualization layer. The long-term goal is to provide a real-time situational awareness tool that combines micro catalysts (like earnings and positioning) with macro regime insights.

## Roadmap

### Phase 1 — Core MVP: DONE
**Focus:** Stock earnings + major positioning events
- Ticker list input & CSV upload
- Earnings table with days-to-event
- Timeline combining earnings and positioning
- Simple filtering by notional threshold

### Phase 2 — Cross-Asset Expansion
**Focus:** Market breadth & inter-market signals
- Add Equity indices (S&P500, Nasdaq, sector indices)
- Add Bond yields & spreads (e.g., 10Y/2Y, credit spreads)
- Add Commodities & FX watchlists
- Integrate macro tickers (VIX, MOVE, DXY, etc.)

### Phase 3 — Liquidity & Flow Metrics
**Focus:** Institutional sentiment and funding conditions
- Integrate Fed balance sheet, Reverse Repo (RRP), and TGA data
- Visualize Money Supply (M2) and market liquidity flows
- Overlay positioning data with liquidity trends

### Phase 4 — Macroeconomic Layer
**Focus:** Fundamental & macro data
- Display key macro hard data (CPI, NFP, ISM, Retail Sales)
- Show event calendars (economic releases, Fed meetings, policy announcements)
- Support country-level aggregation for global macro monitoring

### Phase 5 — Intelligence & Automation
**Focus:** Analytics & systematization
- Add alerts for high-impact events or large positioning
- Implement a data refresh scheduler
- Integrate APIs (Finnhub, EODHD, Polygon, SEC-API)
- Modular adapter layer for multi-source ingestion
- Machine learning layer for macro-regime classification and event clustering

## Tech Stack

- **Frontend / App:** Streamlit
- **Data Handling:** Pandas
- **Visualization:** Plotly
- **Data Sources:** Yahoo Finance (earnings), user-provided CSV (positioning)
- **Future integrations:** Finnhub / Polygon / EODHD / SEC-API / FRED

## Folder Structure
```
market-dashboard/
├─ app.py
├─ requirements.txt
├─ samples/
│  └─ positions_template.csv
└─ README.md
```

## Example Use Case

A trader or analyst can:
1. Enter a list of stock tickers (e.g., AAPL, MSFT, NVDA)
2. Upload a CSV with large trades or institutional positioning
3. Instantly visualize upcoming earnings and major flows on a single timeline
4. Use it as a daily prep tool to monitor catalysts and positioning risk

## Future Vision

*"From earnings to liquidity regimes."*

The project will gradually evolve into a multi-layered market dashboard capable of integrating:
- **Micro events** → earnings, options, flows
- **Macro structure** → liquidity, rates, policy
- **Systematic insights** → clustering, regime shifts, correlations

Ultimately, it will serve as a Quantitative Macro Terminal — open-source, modular, and data-driven.
