# src/main.py

import os
import pandas as pd
from tqdm import tqdm

from reddit_ingest import fetch_posts_and_comments
from nlp_pipeline import filter_dataframe, classify_post, extract_location
from map_visualizer import create_map, geocode_locations

# File paths
RAW_FILE = "output/salt_lake_reports.csv"
CLASSIFIED_FILE = "output/salt_lake_reports_classified.csv"
MAP_FILE = "output/salt_lake_map.html"

def ingest_data():
    print("📥 Ingesting Reddit posts and comments...")
    df = fetch_posts_and_comments()
    df.to_csv(RAW_FILE, index=False)
    print(f"✅ Saved raw data to {RAW_FILE}")
    return df

def classify_data(df, sample_frac=0.01):
    print("🧠 Filtering and classifying data...")
    df = filter_dataframe(df)

    if sample_frac < 1.0:
        df = df.sample(frac=sample_frac, random_state=42)
        print(f"🎯 Sampled {int(sample_frac * 100)}% → {len(df)} rows")

    issues, sentiments, locations = [], [], []

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
    df.to_csv(CLASSIFIED_FILE, index=False)
    print(f"✅ Saved classified data to {CLASSIFIED_FILE}")
    return df

def generate_map(df):
    print("🗺️ Geocoding and building interactive map...")
    unique_locations = df["location"].dropna().unique()
    coords = geocode_locations(unique_locations)
    create_map(df, coords)
    print(f"✅ Map saved to {MAP_FILE}")

def main():
    print("🚦 Running Road Sentiment AI Full Pipeline")
    df_raw = ingest_data()
    df_classified = classify_data(df_raw, sample_frac=0.01)
    generate_map(df_classified)

if __name__ == "__main__":
    main()
