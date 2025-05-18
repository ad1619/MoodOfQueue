import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# Google Sheets auth via secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Mood of the Queue").sheet1

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Mood of the Queue").sheet1

# --- UI ---
st.title("🧠 Mood of the Queue")

mood = st.selectbox("Select your mood:", ["😊 Happy", "😠 Angry", "😕 Confused", "🎉 Excited"])
note = st.text_input("Add a short note (optional):")

if st.button("Log Mood"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, mood, note])
    st.success("Mood logged!")

# --- Visualization ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    today = df[df['timestamp'].dt.date == datetime.today().date()]
    fig = px.bar(today['mood'].value_counts().reset_index(),
                 x='index', y='mood',
                 labels={'index': 'Mood', 'mood': 'Count'},
                 title='Today\'s Mood Distribution')
    st.plotly_chart(fig)
