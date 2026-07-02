import feedparser
import pandas as pd
from config import RSS_FEEDS
from pathlib import Path
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

cutoff = datetime.now().astimezone() - timedelta(days=1)


def fetch_news():
    articles = []

    for feed in RSS_FEEDS:
        print(f"Fetching: {feed}")

        parsed = feedparser.parse(feed)

        for entry in parsed.entries[:30]:
            published = entry.get("published", "")

            try:
                published_dt = parsedate_to_datetime(published)

                if published_dt < cutoff:
                    continue

            except Exception:
                published_dt = None

            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": published,
                "source": parsed.feed.get("title", feed)
            })

    df = pd.DataFrame(articles)

    print(df.head())
    print(f"\nToday's Articles: {len(df)}")

    df.to_csv(DATA_DIR / "news.csv", index=False)

    return df


if __name__ == "__main__":
    fetch_news()