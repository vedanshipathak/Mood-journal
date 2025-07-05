# 🎵 Mood Journal with Soundtrack

A smart journaling app that detects your mood from journal entries and recommends Spotify songs that match your emotional state.

---

## 💡 What the Project Does

-  Takes a **text journal entry** from the user.
-  Uses an **emotion detection model** (via Hugging Face Transformers) to analyze the mood behind the text.
-  Uses the **Spotify API** to fetch songs that match the detected mood.
-  Displays clickable links to **play songs directly on Spotify**.

---

## 🔍 How It Works — Step by Step

1. **User writes** how they feel in a journal-style text box.
2. The app uses a **pretrained NLP model** (`bert-base-uncased-emotion`) from Hugging Face to detect the emotion.
3. The predicted emotion is then used as a **search keyword** in the Spotify API.
4. A list of **Spotify tracks matching the mood** is fetched.
5. The UI displays:
   -  Detected Mood
   -  Top matching songs (with artist name + Spotify link)

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mood-journal-app.git
cd mood-journal-app
2. Install Required Packages
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
4. Add Spotify API Credentials
 ```bash
 client_id = "your-spotify-client-id"
 client_secret = "your-spotify-client-secret"
  ```
