# Autonomous Trading Agent (paper only)

Orbit runs a market review every 15 minutes. The service uses local Qwen 3.5 9B for a bounded classification of recent Alpaca/Benzinga headlines. The model cannot place orders or choose tickers. Deterministic Python rules choose whether to hold, buy, or sell. Market and news text are treated as untrusted input.

## Data and signal

- Watchlist: VTI, SPY, BND.
- Alpaca IEX latest trades plus 90 daily bars.
- Alpaca Benzinga headlines from the last 24 hours. If there are no relevant headlines, data is stale/incomplete, the local model fails, the account is blocked, or the market is closed, the cycle holds.
- Buy only with SMA20 above SMA50, 20-day return above 2%, 5-day return positive, and positive local news sentiment with at least 80% confidence.
- Sell an existing long position on SMA20 below SMA50 and 20-day return below -2%, or negative sentiment plus a negative 5-day return. Short selling is not enabled.

## Limits and controls

- Alpaca paper endpoint only; credentials must be paper keys (`PK…`). No live trading endpoint exists in the agent or broker.
- At most $100 total notional per local day and $300 per symbol. $100 daily account-loss stop. One submitted order per day. Buys are limited by available paper cash.
- JARVIS has a Pause/Enable control. Orbit's global Stop all agents is checked before each cycle and again before an order.
- A reserved daily amount is not restored after a timeout; verify Alpaca paper order history before retrying.
- Cycle status is in `/var/lib/orbit-market/autopilot/status.json`; append-only hash-chained cycle/order events are in `audit.jsonl`.

This is an experimental paper strategy, not investment advice or a prediction of live execution. Alpaca paper fills and IEX coverage can differ from real-market trading.
