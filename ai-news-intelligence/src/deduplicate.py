import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def remove_duplicates():
    df = pd.read_csv(DATA_DIR / "news.csv")

    print(f"Before removing duplicates: {len(df)}")

    # Remove exact duplicate URLs
    df = df.drop_duplicates(subset=["link"])

    # Remove similar headlines
    df["title_lower"] = df["title"].str.lower().str.strip()
    df = df.drop_duplicates(subset=["title_lower"])

    df = df.drop(columns=["title_lower"])

    print(f"After removing duplicates: {len(df)}")

    df.to_csv(DATA_DIR / "news_clean.csv", index=False)

if __name__ == "__main__":
    remove_duplicates()