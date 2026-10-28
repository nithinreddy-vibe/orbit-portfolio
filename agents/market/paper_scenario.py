#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
shares = float(data["shares"])
entry = float(data["entry_price"])
current = float(data["current_price"])
value = shares * current
cost = shares * entry
print(json.dumps({"mode":"paper-only","shares":shares,"cost":cost,"current_value":value,"pnl":value-cost,"return_pct":((value-cost)/cost*100) if cost else 0}, indent=2))

