# 🛣️ Road Sentiment AI

Road Sentiment AI is a pipeline that mines social chatter about roads and traffic from Reddit, classifies complaints using GPT-4, extracts sentiment and location data, and visualizes it on an interactive map.

You can also interact with the data using a command-line chatbot powered by GPT.

---

## 🚀 Features

- 🔍 **Ingests** Reddit posts and comments from Salt Lake City–related subreddits
- 🧠 **Classifies** issue type (e.g., pothole, accident) and sentiment using GPT-4
- 🗺️ **Extracts** and geocodes locations using spaCy and OpenAI
- 🌐 **Visualizes** data on an interactive map with marker clusters and sentiment coloring
- 💬 **Chatbot interface** to ask questions like:
  - “What’s the most common complaint?”
  - “Where are people most frustrated?”
  - “Which roads have the most accidents?”

---

## 📁 Project Structure

"
road_sentiment_ai/
├── src/
│ ├── reddit_ingest.py # Ingests posts + comments
│ ├── nlp_pipeline.py # Classifies issue, sentiment, location
│ ├── map_visualizer.py # Generates interactive Folium map
│ ├── chatbot.py # CLI chatbot using GPT-4
│ └── main.py # Unified pipeline entry point
├── output/ # Stores CSVs and HTML map
│ ├── salt_lake_reports.csv
│ ├── salt_lake_reports_classified.csv
│ └── salt_lake_map.html
├── .env # API keys (not committed)
├── requirements.txt
└── README.md
"

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/sigmagensolutions/road-sentiment-ai.git
   cd road-sentiment-ai
2. **Create a virtual environment**
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
3. **Install dependencies**
pip install -r requirements.txt
python -m spacy download en_core_web_sm
4. **Set up .env with your API keys**
OPENAI_API_KEY=your_openai_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=road-sentiment-ai/0.1

---

## 🧪 Run the Full Pipeline

python src/main.py
This will:
- Ingest recent Reddit data
- Filter and classify rows
- Extract + geocode locations
- Save an interactive map

---

## 💬 Run the CLI Chatbot

python src/chatbot.py
Ask questions like:
 “What’s the most common complaint?”
 “Where are people most angry?”
 “Are people more frustrated or helpful overall?”

---

## ✅ Possible Ideas for Expansion

    Streamlit or Gradio web chatbot
    Heatmap layer for map visualization
    Auto-refresh + scheduled runs
    SQLite or vector DB for scalable memory

---

## 🧠 Tech Stack

    Python, Pandas, spaCy, Folium, PRAW
    OpenAI GPT-4 (via API)
    Geopy (Nominatim for free geocoding)

---

## ⚠️ Disclaimer

This is an experimental project for exploring NLP and geospatial analysis. Not affiliated with Reddit or local governments.

