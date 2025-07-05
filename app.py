import streamlit as st
from spotify_auth import get_spotify_token
from hf_emotion import detect_mood
import requests
import re
from datetime import datetime
import pandas as pd
import altair as alt

# --- Keyword Extractor ---
def extract_emotion_keywords(text):
    keywords = [
        "happy", "sad", "angry", "anxious", "relaxed", "calm", "grateful", "bored", "tired", "excited", "lonely",
        "energetic", "peaceful", "hopeful", "confused", "curious", "impatient", "motivated", "frustrated"
    ]
    text_lower = text.lower()
    return [word for word in keywords if re.search(rf"\b{word}\b", text_lower)]

# --- Emoji Map ---
emoji_map = {
    "happy": "😄", "joy": "😊", "sad": "😢", "anger": "😠", "angry": "😠", "calm": "😌",
    "anxious": "😰", "bored": "😐", "excited": "🤩", "tired": "😴", "curious": "🧐",
    "relaxed": "🌿", "frustrated": "😤", "grateful": "🙏", "peaceful": "🕊️",
    "hopeful": "🌈", "lonely": "🥺", "energetic": "⚡", "confused": "😕", "impatient": "⌛", 
    "motivated": "🔥", "chill": "🎧"
}

# --- Get Songs from Spotify ---
def get_songs_by_mood(mood, token, limit=3, search_type="track"):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": mood,
        "type": search_type,
        "limit": limit
    }
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    if response.status_code != 200:
        return []

    if search_type == "track":
        items = response.json()["tracks"]["items"]
    else:
        items = response.json()["playlists"]["items"]

    songs = []
    for item in items:
        name = item["name"]
        artist = item["artists"][0]["name"] if search_type == "track" else item["owner"]["display_name"]
        url = item["external_urls"]["spotify"]
        songs.append({
            "name": name,
            "artist": artist,
            "url": url
        })
    return songs

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Mood Journal with Soundtrack", layout="centered")
st.title("📝 Mood Journal with Soundtrack 🎵")
st.markdown("Write about how you're feeling, and we'll match your mood to songs or playlists from Spotify.")

journal_entry = st.text_area("How are you feeling today?", height=200, placeholder="Type your thoughts here...")

recommend_type = st.radio("What would you like to hear?", ["Songs", "Playlists"])

if st.button("🔍 Detect Mood & Suggest Music"):
    if journal_entry.strip() == "":
        st.warning("Please enter something to analyze.")
    else:
        with st.spinner("Analyzing your mood..."):
            model_mood = detect_mood(journal_entry)
            keywords = extract_emotion_keywords(journal_entry)

            if keywords:
                mood = st.selectbox("We found some mood words — pick the one that fits best:", keywords)
            elif model_mood:
                mood = model_mood
            else:
                mood = "chill"

            emoji = emoji_map.get(mood, "🎶")
            mood_readable = {
                "joy": "joyful", "anger": "angry", "sadness": "sad", "fear": "anxious", "surprise": "surprised"
            }.get(mood, mood)

            st.success(f"{emoji} You're feeling **{mood_readable}** — here's some music for your vibe!")

            # Log mood with timestamp
            if "mood_log" not in st.session_state:
                st.session_state.mood_log = []
            st.session_state.mood_log.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "mood": mood_readable
            })

        token = get_spotify_token()
        if not token:
            st.error("Failed to get Spotify token. Check your credentials.")
        else:
            search_type = "playlist" if recommend_type == "Playlists" else "track"
            songs = get_songs_by_mood(mood, token, search_type=search_type)

            if not songs:
                st.warning("No results found on Spotify for this mood.")
            else:
                st.subheader(f"🎧 Recommended {recommend_type}:")
                for song in songs:
                    st.markdown(f"**{song['name']}** by *{song['artist']}*")
                    st.markdown(f"[🔗 Listen on Spotify]({song['url']})")
                    st.markdown("---")

# --- Mood Heatmap Section ---
st.subheader("📊 Mood Heatmap")

if "mood_log" in st.session_state and st.session_state.mood_log:
    df = pd.DataFrame(st.session_state.mood_log)
    mood_counts = df.groupby(["date", "mood"]).size().reset_index(name="count")

    chart = alt.Chart(mood_counts).mark_rect().encode(
        x=alt.X('mood:O', title='Mood'),
        y=alt.Y('date:O', title='Date'),
        color=alt.Color('count:Q', scale=alt.Scale(scheme='oranges')),
        tooltip=['date', 'mood', 'count']
    ).properties(width=500, height=300)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Start journaling to build your personal mood heatmap!")
