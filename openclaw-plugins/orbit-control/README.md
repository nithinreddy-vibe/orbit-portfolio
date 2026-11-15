> Historical design/deployment note. This portfolio does not include the full deployment, referenced services, or all scripts. These notes are not a current security certification or runnable setup guide.

# Orbit Control OpenClaw plugin

This local plugin talks only to the Orbit Task API at `127.0.0.1:18082`. It exposes five fixed tools:

- `orbit_submit_task` records a task.
- `orbit_request_approval` records a pending approval bound to an exact JSON payload and a 15-minute expiry.
- `orbit_paper_portfolio` reads the local USA paper portfolio.
- `orbit_paper_trade` records a simulated buy or sell using a user-supplied fill price.
- `orbit_raleigh_buy_rent` calculates a Raleigh, NC housing scenario from supplied assumptions.

The plugin has no shell, file, Docker, broker, quote-feed, or network-search tool. Paper trades cannot reach a broker. Raleigh calculations do not retrieve listing or market data. Approval decisions are made in the Orbit console through the Tailscale Serve route; approved actions stay held because the global execution pause is on.

## Local validation

From Orbit as the `orbit` user:

```bash
openclaw plugins build --root . --entry ./index.js
openclaw plugins validate --root . --entry ./index.js
openclaw plugins inspect orbit-control --runtime --json
```

Keep the minimal tool profile and allow only these five `orbit_*` tools. These controls do not execute real-world actions.

