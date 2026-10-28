#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
rent = float(data["monthly_rent"])
expenses = float(data["monthly_expenses"])
mortgage = float(data.get("monthly_mortgage", 0))
cash_flow = rent - expenses - mortgage
annual = cash_flow * 12
print(json.dumps({"mode":"assumption-driven","monthly_cash_flow":cash_flow,"annual_cash_flow":annual,"assumptions":data}, indent=2))

