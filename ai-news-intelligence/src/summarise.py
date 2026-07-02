import os
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# -------------------------------
# Read News
# -------------------------------
df = pd.read_csv(DATA_DIR / "news_clean.csv")

print(f"\nFound {len(df)} news articles.\n")

# -------------------------------
# Build Prompt
# -------------------------------

news_text = ""

for i, row in df.iterrows():

    news_text += f"""
Article {i+1}

Title:
{row['title']}

Summary:
{row.get('summary', '')}

Source:
{row['source']}

----------------------------------
"""

prompt = f"""
You are an expert AI news analyst.

You will receive multiple AI news articles.

For EACH article return:

- title
- summary (maximum 3 lines)
- why_it_matters (maximum 2 lines)
- category
- importance (1-10)

Allowed Categories:

LLM
Startup
Research
Robotics
Funding
Enterprise
Regulation
Hardware
Open Source
Other

Return ONLY a valid JSON array.

The array MUST contain exactly {len(df)} objects.

Do NOT skip any article.

Do NOT include markdown.

Do NOT include explanations.

Each object MUST have this format:

{{
"title":"",
"summary":"",
"why_it_matters":"",
"category":"",
"importance":0
}}

Articles:

{news_text}
"""

print("Sending articles to Gemini...\n")

# -------------------------------
# Gemini Request
# -------------------------------

try:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

except Exception as e:

    print("Gemini API Error:")
    print(e)
    raise

# -------------------------------
# Parse Response
# -------------------------------

text = response.text.strip()

try:
    data = json.loads(text)

except json.JSONDecodeError:

    print("\nGemini returned invalid JSON:\n")
    print(text)
    raise

print(f"Gemini returned {len(data)} summaries.")

if len(data) != len(df):
    print(
        f"Warning: Expected {len(df)} summaries but received {len(data)}."
    )

# -------------------------------
# Build Output
# -------------------------------

results = []

for article, original in zip(data, df.to_dict("records")):

    results.append({
        "published": original["published"],
        "title": article.get("title", original["title"]),
        "source": original["source"],
        "category": article.get("category", "Other"),
        "importance": article.get("importance", 5),
        "summary": article.get("summary", ""),
        "why_it_matters": article.get("why_it_matters", ""),
        "link": original["link"]
    })

output = pd.DataFrame(results)

# -------------------------------
# Sort by Importance
# -------------------------------

output = output.sort_values(
    by="importance",
    ascending=False
).reset_index(drop=True)

# -------------------------------
# Save CSV
# -------------------------------

output_file = DATA_DIR / "summarized_news.csv"

output.to_csv(output_file, index=False)

print("\nSummary generation completed successfully!")

print(f"\nSaved file: {output_file}")

print("\nTop 5 Articles:\n")

print(output.head())