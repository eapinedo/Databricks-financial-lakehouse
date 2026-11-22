import csv
import os
import random
from datetime import date, timedelta

random.seed(42)
OUTPUT_DIR = "sample_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Chart of Accounts
accounts = [
    ("ACC-100", "Enterprise SaaS Revenue", "Revenue", "Sales"),
    ("ACC-110", "Consulting Services Revenue", "Revenue", "Sales"),
    ("ACC-200", "Cloud Hosting & Infrastructure", "COGS", "IT"),
    ("ACC-210", "Third-Party Payment Fees", "COGS", "Finance"),
    ("ACC-300", "Software Licenses", "OpEx", "IT"),
    ("ACC-310", "Digital Marketing Spend", "OpEx", "Marketing"),
    ("ACC-320", "Logistics & Supply Chain", "OpEx", "Operations"),
    ("ACC-330", "Legal & Audit Advisory", "OpEx", "Finance"),
    ("ACC-340", "Corporate Travel & Events", "OpEx", "Sales"),
    ("ACC-350", "Facilities & Utilities", "OpEx", "Operations"),
]

with open(f"{OUTPUT_DIR}/chart_of_accounts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["account_id", "account_name", "account_type", "department"])
    writer.writerows(accounts)

# 2. Monthly Departmental Expense Budgets (Jan 2025 - Oct 2026)
dept_monthly_budgets = {
    "IT": 68000,
    "Marketing": 52000,
    "Operations": 61000,
    "Finance": 34000,
    "Sales": 28000,
}

budget_rows = []
for year in (2025, 2026):
    max_month = 12 if year == 2025 else 10
    for month in range(1, max_month + 1):
        month_str = f"{year}-{month:02d}-01"
        for dept, base_budget in dept_monthly_budgets.items():
            # Slight seasonal bump in Q4
            multiplier = 1.12 if month in (10, 11, 12) else 1.0
            budget_rows.append([month_str, dept, round(base_budget * multiplier, 2)])

with open(f"{OUTPUT_DIR}/budget_targets.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["budget_month", "department", "budget_usd"])
    writer.writerows(budget_rows)

# 3. General Ledger Transactions (5,000 base rows + intentional defects & anomalies)
vendors_by_dept = {
    "IT": ["CloudScale Inc", "DataStack Corp", "NetGuard Systems", "CyberVault LLC"],
    "Marketing": ["AdPulse Media", "BrandLift Agency", "SearchPeak Digital"],
    "Operations": ["FastFreight Logistics", "Apex Supply Co", "MetroGrid Utilities"],
    "Finance": ["StripePay Clearing", "Sterling Audit LLP", "GlobalTax Advisors"],
    "Sales": ["Enterprise Client Portal", "Skyline Events", "AeroCorp Travel"],
}

# Baseline average transaction size per account
account_baselines = {
    "ACC-100": (4200, 900),
    "ACC-110": (2900, 650),
    "ACC-200": (1450, 300),
    "ACC-210": (520, 110),
    "ACC-300": (980, 210),
    "ACC-310": (1600, 380),
    "ACC-320": (1850, 420),
    "ACC-330": (1150, 240),
    "ACC-340": (740, 180),
    "ACC-350": (1100, 200),
}

currencies = ["USD", "USD", "USD", "USD", "EUR", "GBP", "CAD"]
start_date = date(2025, 1, 1)
total_days = (date(2026, 10, 31) - start_date).days

txn_rows = []
for i in range(1, 5001):
    txn_id = f"TXN-{i:06d}"
    txn_dt = start_date + timedelta(days=random.randint(0, total_days))
    acct_id, acct_name, acct_type, dept = random.choice(accounts)
    vendor = random.choice(vendors_by_dept[dept])
    currency = random.choice(currencies)
    mean, std = account_baselines[acct_id]

    amount = max(50.0, random.gauss(mean, std))
    status = "POSTED"
    date_str = txn_dt.strftime("%Y-%m-%d")

    roll = random.random()
    if roll < 0.015:
        # Inject billing anomaly (4.5x - 7.5x spike)
        amount = mean * random.uniform(4.5, 7.5)
    elif roll < 0.030:
        # Inject mixed date format (MM/DD/YYYY) for Silver standardization
        date_str = txn_dt.strftime("%m/%d/%Y")
    elif roll < 0.035:
        # Inject corrupt date -> should route to Quarantine
        date_str = "INVALID_DATE"
    elif roll < 0.040:
        # Inject missing account_id -> should route to Quarantine
        acct_id = ""
    elif roll < 0.044:
        # Inject non-numeric amount -> should route to Quarantine
        amount = "N/A"
    elif roll < 0.050:
        # Inject voided record -> should route to Quarantine
        status = "VOID"

    amount_val = f"{amount:.2f}" if isinstance(amount, float) else amount
    txn_rows.append([txn_id, date_str, acct_id, vendor, currency, amount_val, status])

# Inject 100 exact duplicate transactions (~2%) to test Silver deduplication
txn_rows.extend(random.sample(txn_rows[:4500], 100))
random.shuffle(txn_rows)

with open(f"{OUTPUT_DIR}/general_ledger_transactions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["txn_id", "txn_date", "account_id", "vendor_name", "currency", "amount", "status"])
    writer.writerows(txn_rows)

print(f"Generated {len(txn_rows)} transactions, {len(accounts)} accounts, and {len(budget_rows)} budget targets in ./{OUTPUT_DIR}/")