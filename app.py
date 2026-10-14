import streamlit as st
import pandas as pd
from nlp_engine import search_schemes, normalize_query, detect_language
from eligibility import filter_by_profile
from database import init_db, log_search

st.set_page_config(page_title="Government Scheme Assistant", page_icon="🇮🇳", layout="wide")
init_db()

st.title("🇮🇳 Government Scheme Information Chatbot")
st.caption("Central + Tamil Nadu schemes | Tamil, English and Tanglish keyword support | No external AI API")

with st.sidebar:
    st.header("👤 Optional Profile")
    age = st.number_input("Age", min_value=0, max_value=120, value=20)
    state = st.selectbox("State", ["Tamil Nadu", "Other"])
    occupation = st.selectbox("Occupation", ["Any", "Student", "Farmer", "Women", "Worker", "Business owner", "Senior citizen", "Person with disability", "Fisher"])
    income = st.selectbox("Annual family income (approx.)", ["Not specified", "Below ₹1 lakh", "₹1–2.5 lakh", "₹2.5–5 lakh", "Above ₹5 lakh"])
    st.caption("Profile details are used only to filter the local dataset. This is not an official eligibility decision.")

lang = st.radio("Answer language / பதில் மொழி", ["Tamil + English", "English", "தமிழ் (Tamil)"], horizontal=True)
query = st.text_input(
    "Ask about a scheme / திட்டத்தைப் பற்றி கேளுங்கள்",
    placeholder="Example: student scholarship / maanavar scholarship / விவசாயி scheme / pengal scheme"
)

if st.button("Search Schemes / திட்டங்களைத் தேடு", type="primary") and query.strip():
    results = search_schemes(query, pd.read_csv("schemes.csv"))
    log_search(query, len(results))
    st.subheader("Search results / தேடல் முடிவுகள்")
    if results.empty:
        st.warning("Matching scheme not found in this starter dataset. Try a short keyword such as student, farmer, pension, health, women, scholarship, விவசாயி, மாணவர், பெண்கள்.")
    else:
        for _, row in results.head(10).iterrows():
            with st.expander(f"{row['scheme_name']} · {row['government_level']}"):
                st.write(f"**Category:** {row['category']}")
                st.write(f"**Who may be covered:** {row['target_group']}")
                st.write(f"**Benefit:** {row['benefit_summary']}")
                st.write(f"**Eligibility note:** {row['eligibility_note']}")
                st.markdown(f"**Official information:** [{row['official_info_url']}]({row['official_info_url']})")
                if lang == "Tamil + English":
                    st.info("தமிழ் குறிப்பு: இந்தத் திட்டம் யாருக்குப் பயன்படும், என்ன உதவி கிடைக்கும் என்பதற்கான சுருக்கம் மேலே உள்ளது. தகுதி மற்றும் விண்ணப்ப விவரங்களை அதிகாரப்பூர்வ தளத்தில் சரிபார்க்கவும்.")
                elif lang == "தமிழ் (Tamil)":
                    st.info("தமிழ் குறிப்பு: திட்டத்தின் பயன் மற்றும் தகுதி விவரங்களை மேலே காணலாம். விண்ணப்பிக்கும் முன் அதிகாரப்பூர்வ தளத்தில் தற்போதைய விதிகளைச் சரிபார்க்கவும்.")
                else:
                    st.info("Please confirm current eligibility, benefits and application dates on the official portal before applying.")

st.divider()
st.subheader("Find schemes by profile / விவரங்களின் அடிப்படையில் தேடு")
if st.button("Show possible matches / பொருந்தக்கூடிய திட்டங்கள்"):
    all_schemes = pd.read_csv("schemes.csv")
    matches = filter_by_profile(all_schemes, age, state, occupation, income)
    st.caption("These are keyword-based suggestions, not a verified eligibility result.")
    for _, row in matches.head(15).iterrows():
        st.markdown(f"- **{row['scheme_name']}** — {row['category']}  \n  {row['benefit_summary']}  \n  [Official info]({row['official_info_url']})")

with st.expander("⚠️ Important notice / முக்கிய அறிவிப்பு"):
    st.write("This is an educational demo dataset. Scheme status, amounts, eligibility, application windows and URLs can change. A scheme appearing here does not mean that you qualify. Verify all details with the official government portal or department.")
    st.write("இது கல்வி நோக்கத்திற்கான demo project. இங்கு திட்டம் காட்டப்படுவது மட்டும் நீங்கள் தகுதியானவர் என்பதைக் குறிக்காது. தற்போதைய தகுதி, தொகை, விண்ணப்ப காலம் ஆகியவற்றை அதிகாரப்பூர்வ தளத்தில் சரிபார்க்கவும்.")
