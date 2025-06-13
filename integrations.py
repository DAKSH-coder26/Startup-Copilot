import os
import requests
from notion_client import Client
from pytrends.request import TrendReq
import pandas as pd
import re
notion_token = os.environ.get("NOTION_TOKEN")
notion_db_id = os.environ.get("NOTION_DATABASE_ID1")

def extract_keyword_from_prompt(prompt: str) -> str:
    # Naive fallback: extract up to the first punctuation mark or 6 words
    stripped = re.split(r'[.?!\\n]', prompt)[0]
    words = stripped.split()[:6]
    return " ".join(words)

def fetch_google_trends_data(prompt: str) -> str:
    keyword = extract_keyword_from_prompt(prompt)
    pytrends = TrendReq(hl='en-US', tz=330)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
    data = pytrends.interest_over_time()

    if data.empty or keyword not in data.columns:
        return f"No Google Trends data found for '{keyword}'."

    trend_series = data[keyword]
    summary = trend_series.describe().to_dict()
    recent_trend = trend_series[-4:].tolist()

    formatted = (
        f"Google Trends Insight for '{keyword}':\n"
        f"- Average Interest (12 months): {summary['mean']:.2f}\n"
        f"- Peak Interest: {summary['max']} on {trend_series.idxmax().date()}\n"
        f"- Lowest Interest: {summary['min']} on {trend_series.idxmin().date()}\n"
        f"- Interest Last 4 Weeks: {recent_trend}\n"
    )
    return formatted

if not notion_token or not notion_db_id:
    raise EnvironmentError("Missing required Notion credentials. Make sure NOTION_TOKEN and NOTION_DATABASE_ID1 are set.")

notion = Client(auth=notion_token)
NOTION_DATABASE_ID = notion_db_id

def get_title_property_name(database_id):
    response = notion.databases.retrieve(database_id)
    for key, value in response["properties"].items():
        if value["type"] == "title":
            return key
    raise ValueError("No title property found in the Notion database.")

def save_to_notion(title: str, content: str, database_id: str = None):
    db_id = database_id or NOTION_DATABASE_ID
    if not db_id:
        raise ValueError("Missing Notion Database ID.")

    title_property = get_title_property_name(db_id)

    notion.pages.create(
        parent={"database_id": db_id},
        properties={
            title_property: {
                "title": [
                    {"text": {"content": title}}
                ]
            }
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": content[:2000]}}
                    ]
                }
            }
        ]
    )

