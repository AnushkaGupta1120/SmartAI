from src.fetch_news import fetch_news
from src.deduplicate import remove_duplicates
import subprocess
import sys

print("=" * 50)
print("AI NEWS INTELLIGENCE")
print("=" * 50)

print("\n1. Fetching latest news...")
fetch_news()

print("\n2. Removing duplicates...")
remove_duplicates()

print("\n3. Generating AI summaries...")
subprocess.run([sys.executable, "src/summarize.py"], check=True)

print("\n4. Uploading to Google Sheets...")
subprocess.run([sys.executable, "src/sheets.py"], check=True)

print("\n✅ Workflow completed successfully!")