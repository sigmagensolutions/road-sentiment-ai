# src/map_visualizer.py

import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

INPUT_FILE = "output/salt_lake_reports_classified.csv"
OUTPUT_FILE = "output/salt_lake_map.html"

# Map sentiment to marker colors
SENTIMENT_COLOR = {
    "angry": "red",
    "frustrated": "orange",
    "neutral": "gray",
    "helpful": "green",
    "other": "blue",
    "error": "darkpurple"
}

def geocode_locations(locations):
    geolocator = Nominatim(user_agent="road_sentiment_ai")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    coords = {}

    for loc in locations:
        if loc not in coords and loc.lower() not in ["null", "error"]:
            try:
                location = geocode(f"{loc}, Salt Lake City, Utah")
                if location:
                    coords[loc] = (location.latitude, location.longitude)
                    print(f"✓ Geocoded: {loc} → {coords[loc]}")
                else:
                    coords[loc] = None
                    print(f"✗ Not found: {loc}")
            except Exception as e:
                print(f"❌ Geocoding error for {loc}: {e}")
                coords[loc] = None
    return coords

def create_map(df, coords):
    map_center = [40.7608, -111.8910]  # Salt Lake City
    m = folium.Map(location=map_center, zoom_start=12)

    cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        loc = row["location"]
        sentiment = row.get("sentiment", "other").lower()
        color = SENTIMENT_COLOR.get(sentiment, "blue")

        if loc in coords and coords[loc]:
            popup_text = f"<b>{row['issue_type'].title()}</b><br><b>{sentiment.title()}</b><br><i>{row['title']}</i>"
            folium.Marker(
                location=coords[loc],
                popup=popup_text,
                icon=folium.Icon(color=color)
            ).add_to(cluster)

    # Add custom legend
    legend_html = '''
     <div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; background-color: white; padding: 10px; border:2px solid black;">
     <b>Sentiment Legend</b><br>
     <i class="fa fa-map-marker fa-2x" style="color:red"></i> Angry<br>
     <i class="fa fa-map-marker fa-2x" style="color:orange"></i> Frustrated<br>
     <i class="fa fa-map-marker fa-2x" style="color:gray"></i> Neutral<br>
     <i class="fa fa-map-marker fa-2x" style="color:green"></i> Helpful<br>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save(OUTPUT_FILE)
    print(f"✅ Saved interactive map to {OUTPUT_FILE}")

def main():
    df = pd.read_csv(INPUT_FILE)
    unique_locs = df["location"].dropna().unique()
    coords = geocode_locations(unique_locs)
    create_map(df, coords)

if __name__ == "__main__":
    main()
