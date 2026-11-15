# Orbit / J.A.R.V.I.S. Demo

This is a **standalone, synthetic-data showcase** of the Orbit assistant experience. It does not connect to Orbit, the local PC, email, Telegram, financial accounts, brokerage accounts, or smart-home devices. Buttons only update the page in your browser.

## Version 2.0 showcase package`n`n- `index.html`: interactive browser demo with synthetic tasks and a visible approval boundary.`n- `linkedin-cover.png`: ready-to-attach LinkedIn image.`n- `linkedin-cover.svg`: editable cover source.`n- `LINKEDIN-POST.md`: suggested post copy.`n`n## Run locally

Open `index.html` in a browser. It has no dependencies, API keys, sign-in, or network-service requirements.

Optionally, serve it from this directory if you prefer a local URL:

```powershell
python -m http.server 8090
```

Then open <http://127.0.0.1:8090>. Stop the server with `Ctrl+C`.

## Demo flows

- Switch between My Day, Departments, and Activity.
- Submit a sample request to see a clearly simulated task lifecycle.
- Open a department card for its role and safety boundaries.
- Review a task-routing flow from request to verified receipt.

All people, balances, events, and task results shown are fictional examples. The LinkedIn post draft is in `LINKEDIN-POST.md`; the social cover graphic is `linkedin-cover.svg`.
