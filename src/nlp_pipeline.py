# src/nlp_pipeline.py

import pandas as pd
import os
from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
import spacy

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
nlp = spacy.load("en_core_web_sm")

INPUT_FILE = "output/salt_lake_reports.csv"
OUTPUT_FILE = "output/salt_lake_reports_classified.csv"

def filter_dataframe(df, min_body_len=30, min_score=2):
    """Filter out short or low-score posts/comments."""
    initial_count = len(df)
    df = df[df["body"].astype(str).str.len() >= min_body_len]
    df = df[df["score"] >= min_score]
    filtered_count = len(df)
    print(f"📉 Filtered down from {initial_count} → {filtered_count} rows")
    return df

def classify_post(text):
    prompt = f"""
You are an assistant helping classify Reddit posts related to road issues.

Given the text below, return:
1. The most likely issue type: "pothole", "accident", "detour", "closure", "construction", "traffic", or "other"
2. The sentiment of the post: "angry", "frustrated", "neutral", "helpful", or "other"

Text:
{text}

Respond in this JSON format:
{{"issue_type": "...", "sentiment": "..."}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You classify road-related Reddit posts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        print("Response:", content)  # Optional debug
        result = eval(content)
        return result["issue_type"], result["sentiment"]
    except Exception as e:
        print(f"❌ Error during classification: {e}")
        return "error", "error"

def extract_location(text):
    doc = nlp(text)
    spacy_locs = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
    if spacy_locs:
        return spacy_locs[0]
    else:
        try:
            prompt = f"""
Given the following Reddit post text, extract the most specific location mentioned (e.g., street name, freeway, intersection, neighborhood, or landmark). If no location is mentioned, respond with "null".

Text:
{text}

Respond with just the location string or "null".
"""
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You extract road-related location names from Reddit posts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            location = response.choices[0].message.content.strip().strip('"')
            return location
        except Exception as e:
            print(f"❌ Error extracting location: {e}")
            return "error"

def main():
    print("🚀 Starting NLP classification...")
    df = pd.read_csv(INPUT_FILE)
    print(f"📄 Loaded {len(df)} records from {INPUT_FILE}")

    df = filter_dataframe(df)

    # Sample 1% for now
    df = df.sample(frac=0.01, random_state=42)
    print(f"🎯 Using random 1% sample → {len(df)} rows")

    issues = []
    sentiments = []
    locations = []

    tqdm.pandas()
    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = f"{row['title']} {row['body']}"
        issue, sentiment = classify_post(text)
        location = extract_location(text)

        issues.append(issue)
        sentiments.append(sentiment)
        locations.append(location)

    df["issue_type"] = issues
    df["sentiment"] = sentiments
    df["location"] = locations
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved classified results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
