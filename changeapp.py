import streamlit as st
import requests
import json
import urllib.parse
from google import genai
from datetime import date

# --- Load API Keys ---
def getGenAIClient():
    with open("gemini_api_key.txt") as f:
        key = f.read().strip()
    return genai.Client(api_key=key)

def loadGoogleMapsAPIKey():
    with open("google_maps_api_key.txt") as f:
        return f.read().strip()

genAIClient = getGenAIClient()
google_maps_api_key = loadGoogleMapsAPIKey()

# --- Streamlit UI ---
st.title("AITinerary - AI Powered Travel Planner")

# ---- Travel Dates ----
col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Start Date", date.today())
with col2:
    end_date = st.date_input("End Date", date.today())
with col3:
    nod = (end_date - start_date).days
    st.metric("Number of Days", nod)

# ---- Passengers ----
st.subheader("Passengers")
col1, col2, col3 = st.columns(3)
with col1:
    adults = st.number_input("Adults", min_value=0, value=1)
with col2:
    children = st.number_input("Children (<12)", min_value=0, value=0)
with col3:
    seniors = st.number_input("Seniors (60+)", min_value=0, value=0)

# ---- Costs ----
travel_budget = st.radio("Costs", ["Budget", "Standard", "Luxury"])

# ---- Destination ----
destination = st.text_input("Destination (city / country / region)", "")

# ---- Interests ----
st.subheader("Interests")
interests = st.multiselect(
    "Select interests",
    ["Kids", "Beach", "Skiing", "History", "Romance", "Party"]
)

# ---- Button to Generate Cities ----
if st.button("Load Recommendations"):
    query = (
        f"List the top 10 cities for tourism in {destination} "
        f"for interests {interests} between {start_date} and {end_date}"
    )

    response = genAIClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={"response_mime_type": "application/json"}
    )

    try:
        top10cities = json.loads(response.text)
        st.session_state["top10cities"] = top10cities
        st.success("Cities loaded successfully!")
    except Exception as e:
        st.error(f"Failed to parse response: {e}")

# ---- Display Cities ----
if "top10cities" in st.session_state:
    st.subheader("Recommended Cities")
    city_options = [f"{c['rank']}. {c['city']} ({c['country']})" for c in st.session_state["top10cities"]]
    selected_cities = st.multiselect("Select Cities", city_options)

    if selected_cities:
        # Build Google Maps Static URL
        markers = []
        for entry in selected_cities:
            rank = entry.split(".")[0]
            idx = int(rank) - 1
            city = st.session_state["top10cities"][idx]["city"]
            country = st.session_state["top10cities"][idx]["country"]
            markers.append(f"markers=color:blue%7Clabel:{rank}%7C{urllib.parse.quote_plus(city)}%2C{urllib.parse.quote_plus(country)}")

        map_url = f"https://maps.googleapis.com/maps/api/staticmap?{'&'.join(markers)}&size=1000x500&key={google_maps_api_key}"

        st.image(map_url, caption="Selected Cities Map")

