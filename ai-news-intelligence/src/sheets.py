from pathlib import Path

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ------------------------
# Paths
# ------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SERVICE_ACCOUNT_FILE = BASE_DIR / "service_account.json"

# ------------------------
# Google Authentication
# ------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(creds)

# ------------------------
# Open Sheet
# ------------------------

SHEET_NAME = "AI News Intelligence"

sheet = client.open(SHEET_NAME).sheet1

# ------------------------
# Read CSV
# ------------------------

df = pd.read_csv(DATA_DIR / "summarized_news.csv")

print(f"Uploading {len(df)} rows...")

# ------------------------
# Append Rows
# ------------------------

rows = df.fillna("").values.tolist()

sheet.append_rows(rows)

print("✅ Upload Successful!")