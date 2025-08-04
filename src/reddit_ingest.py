# src/reddit_ingest.py

import praw
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

SUBREDDITS = ["SaltLakeCity", "Utah", "UtahDrivers", "utahcounty", "slc"]
POST_LIMIT = 500

def fetch_posts_and_comments():
    all_data = []
    for sub in SUBREDDITS:
        subreddit = reddit.subreddit(sub)
        for post in subreddit.new(limit=POST_LIMIT):
            base_text = f"{post.title} {post.selftext}".strip()
            all_data.append({
                "subreddit": sub,
                "type": "post",
                "title": post.title,
                "body": post.selftext,
                "url": post.url,
                "score": post.score,
                "created_utc": datetime.utcfromtimestamp(post.created_utc),
                "id": post.id
            })

            # Try to include top-level comments
            try:
                post.comments.replace_more(limit=0)
                for comment in post.comments.list():
                    all_data.append({
                        "subreddit": sub,
                        "type": "comment",
                        "title": f"Comment on: {post.title}",
                        "body": comment.body,
                        "url": post.url,
                        "score": comment.score,
                        "created_utc": datetime.utcfromtimestamp(comment.created_utc),
                        "id": comment.id
                    })
            except Exception as e:
                print(f"❌ Failed to load comments for {post.id}: {e}")
    return pd.DataFrame(all_data)

if __name__ == "__main__":
    df = fetch_posts_and_comments()
    df.to_csv("output/salt_lake_reports.csv", index=False)
    print(f"✅ Saved {len(df)} records to output/salt_lake_reports.csv")
