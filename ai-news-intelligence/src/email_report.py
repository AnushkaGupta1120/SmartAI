import os
import smtplib
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI News Intelligence")

df = pd.read_csv(DATA_DIR / "summarized_news.csv")

# Sort by importance
df = df.sort_values("importance", ascending=False)

# Only top 10 stories in email
top_news = df.head(10)

total_articles = len(df)
highest = df["importance"].max()
average = round(df["importance"].mean(), 1)

categories = (
    df.groupby("category")
      .size()
      .sort_values(ascending=False)
)

html = f"""
<html>
<head>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 30px;
}}

h1 {{
    color: #1a73e8;
}}

.card {{
    border:1px solid #ddd;
    border-radius:8px;
    padding:15px;
    margin-bottom:20px;
}}

.summary {{
    color:#444;
}}

.footer {{
    color:gray;
    font-size:13px;
}}
</style>
</head>

<body>

<h1>🤖 SmartAI Daily</h1>

<h3>Daily AI Intelligence Report</h3>

<p>

<b>Total Articles:</b> {total_articles}<br>
<b>Highest Importance:</b> {highest}/10<br>
<b>Average Importance:</b> {average}

</p>

<hr>

<h2>📊 Categories</h2>
<ul>
"""

for category, count in categories.items():
    html += f"<li><b>{category}</b> : {count}</li>"

html += "</ul><hr><h2>🔥 Top Stories</h2>"

for _, row in top_news.iterrows():

    html += f"""
<div class="card">

<h3>{row['title']}</h3>

<p>

<b>Category:</b> {row['category']}<br>

<b>Importance:</b> ⭐ {row['importance']}/10

</p>

<p class="summary">
{row['summary']}
</p>

<p>

<b>Why it matters</b><br>

{row['why_it_matters']}

</p>

<p>

<a href="{row['link']}">Read Full Article</a>

</p>

</div>
"""

html += f"""

<hr>

<div class="footer">

Google Sheet Updated Successfully ✅

Project: SmartAI Daily

</div>

</body>

</html>
"""

msg = MIMEMultipart()

msg["From"] = EMAIL
msg["To"] = EMAIL_TO
msg["Subject"] = "🤖 SmartAI Daily"

msg.attach(MIMEText(html, "html"))

print("Connecting to Gmail...")

with smtplib.SMTP("smtp.gmail.com", 587) as server:

    server.starttls()

    server.login(EMAIL, PASSWORD)

    server.sendmail(
        EMAIL,
        EMAIL_TO,
        msg.as_string()
    )

print("✅ Email sent successfully!")