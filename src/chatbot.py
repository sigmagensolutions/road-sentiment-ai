# src/chatbot.py

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CLASSIFIED_FILE = "output/salt_lake_reports_classified.csv"

def summarize_data(df):
    issue_counts = df["issue_type"].value_counts().to_dict()
    sentiment_counts = df["sentiment"].value_counts().to_dict()
    location_counts = df["location"].value_counts().head(10).to_dict()

    return {
        "top_issue_types": issue_counts,
        "sentiment_summary": sentiment_counts,
        "top_locations": location_counts
    }

def generate_answer(question, summary):
    prompt = f"""
You are a data analysis assistant. You are working with a dataset of Reddit posts related to road issues in Salt Lake City.

The dataset has already been analyzed. Here's a summary of key points:

Top Issue Types:
{summary["top_issue_types"]}

Sentiment Summary:
{summary["sentiment_summary"]}

Top Locations:
{summary["top_locations"]}

Now, based on this summary, answer the following user question:

"{question}"

Answer clearly and concisely.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You answer questions based on a structured dataset summary."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"

def main():
    print("🤖 Road Sentiment AI Chatbot (CLI Edition)")
    print("Type a question or type 'exit' to quit.\n")

    df = pd.read_csv(CLASSIFIED_FILE)
    summary = summarize_data(df)

    while True:
        question = input("You: ")
        if question.lower() in ("exit", "quit"):
            break
        answer = generate_answer(question, summary)
        print(f"\n🧠 {answer}\n")

if __name__ == "__main__":
    main()
