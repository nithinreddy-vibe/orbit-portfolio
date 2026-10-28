# Raleigh, North Carolina buy-versus-rent model

This calculator compares buying and renting over a user-selected horizon using explicit assumptions. It does not retrieve current Raleigh prices or rents and does not give personal financial advice. Supply purchase price, monthly rent, down payment, mortgage rate and term, taxes, insurance, maintenance, HOA, closing costs, appreciation, rent growth, investment return and years.

Required JSON keys: purchase_price, monthly_rent, down_payment_pct, mortgage_rate_pct, loan_term_years, property_tax_pct, maintenance_pct, appreciation_pct, rent_growth_pct, investment_return_pct and years. Optional: region (defaults to Raleigh, NC), closing_cost_pct (defaults to 3), annual_home_insurance, monthly_renter_insurance and monthly_hoa.

Example:
  printf '%s\n' '{"purchase_price":"350000","monthly_rent":"2200","down_payment_pct":"20","mortgage_rate_pct":"6.5","loan_term_years":30,"property_tax_pct":"1","maintenance_pct":"1","appreciation_pct":"3","rent_growth_pct":"3","investment_return_pct":"5","years":5}' | python3 buy_rent.py

The output compares buyer equity plus invested monthly savings with the renter's invested initial cash and monthly savings. It omits sale costs, tax treatment, major repairs, changing insurance/HOA, rent deposits and other personal circumstances.
