import subprocess
import sys

print("Fetching news...")
subprocess.run([sys.executable, "src/fetch_news.py"], check=True)

print("Removing duplicates...")
subprocess.run([sys.executable, "src/deduplicate.py"], check=True)

print("Summarizing...")
subprocess.run([sys.executable, "src/summarize.py"], check=True)

print("Updating Google Sheet...")
subprocess.run([sys.executable, "src/sheets.py"], check=True)

print("Sending email...")
subprocess.run([sys.executable, "src/email_report.py"], check=True)

print("Done!")