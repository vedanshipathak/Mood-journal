import streamlit as st
from spotify_auth import get_spotify_token
import requests
from hf_emotion import detect_mood  # Using Hugging Face model

# --- Get Songs from Spotify ---
def get_songs_by_mood(mood, token, limit=3):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": mood,  # No mapping – use raw Hugging Face output like "joy", "sadness"
        "type": "track",
        "limit": limit
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    if response.status_code != 200:
        return []

    results = response.json()["tracks"]["items"]
    songs = []
    for item in results:
        song_name = item["name"]
        artist_name = item["artists"][0]["name"]
        song_url = item["external_urls"]["spotify"]
        songs.append({
            "name": song_name,
            "artist": artist_name,
            "url": song_url
        })
    return songs

# --- Streamlit App UI ---
st.set_page_config(page_title="Mood Journal with Soundtrack", layout="centered")
st.title("📝 Mood Journal with Soundtrack 🎵")
st.markdown("Write about how you're feeling, and we'll match your mood to songs from Spotify.")

journal_entry = st.text_area("How are you feeling today?", height=200, placeholder="Type your thoughts here...")

if st.button("🔍 Detect Mood & Suggest Songs"):
    if journal_entry.strip() == "":
        st.warning("Please enter something to analyze.")
    else:
        with st.spinner("Analyzing mood..."):
            mood = detect_mood(journal_entry)  # Hugging Face model
            st.success(f"**Detected Mood:** {mood.upper()} 🎯")

        token = get_spotify_token()
        if not token:
            st.error("Failed to get Spotify token. Check your credentials in `spotify_auth.py`.")
        else:
            songs = get_songs_by_mood(mood, token)
            if not songs:
                st.warning("No songs found for this mood.")
            else:
                st.subheader("🎧 Song Recommendations:")
                for song in songs:
                    st.markdown(f"**{song['name']}** by *{song['artist']}*")
                    st.markdown(f"[🔗 Listen on Spotify]({song['url']})")
                    st.markdown("---")
