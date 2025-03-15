import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("⚠️ API Key is missing. Please set the GEMINI_API_KEY environment variable.")

# Initialize Session State Defaults
defaults = {
    "xp_points": 0, "level": 1, "mindcoins": 0, "streak": 0,
    "logged_in": False, "username": None, "users": {},
    "has_playlist_generator": False, "has_book_recommendation": False,
    "page": "home"
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Function to check and handle level-up
def check_level_up():
    xp_needed = st.session_state.level * 100  # XP required for next level
    if st.session_state.xp_points >= xp_needed:
        st.session_state.level += 1
        st.session_state.xp_points -= xp_needed  # Carry over extra XP
        st.success(f"🎉 Congratulations! You've reached **Level {st.session_state.level}**!")

# Apply Custom CSS
st.markdown("""
    <style>
    .stApp { background-image: linear-gradient(90deg, #A0FAD1, #A0ECFA); color: black; }
    .stButton>button { background: linear-gradient(90deg, #0b7bb8, #0fa399); color: white; 
        border-radius: 15px; padding: 10px; border: none; transition: all 0.3s ease-in-out; }
    .stButton>button:hover { background-color: blue; transform: scale(1.05); }
    .stTextInput>div>div>input { background: rgba(255, 255, 255, 0.2); border-radius: 10px; 
        padding: 10px; color: black; border: none; }
    </style>
""", unsafe_allow_html=True)

def render_dashboard():
    """Renders a modern, visually appealing dashboard with progress tracking."""
    
    # XP required for the next level
    xp_needed = st.session_state.level * 100  
    progress_percent = min(st.session_state.xp_points / xp_needed, 1.0) * 100

    # Apply Modern Styling
    st.markdown("""
        <style>
        .stApp { background-image: linear-gradient(90deg, #A0FAD1, #A0ECFA); color: black; padding: 20px; }
        .big-font { font-size:25px !important; font-weight: bold; }
        .metric-box { background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 15px; text-align: center; box-shadow: 3px 3px 10px rgba(0,0,0,0.1); }
        .progress-container { width: 100%; background-color: #ddd; border-radius: 10px; }
        .progress-bar { height: 20px; border-radius: 10px; background: linear-gradient(90deg, #0b7bb8, #0fa399); }
        </style>
    """, unsafe_allow_html=True)

# Dashboard Rendering Function
def render_dashboard():
    st.title("🏠 MindMate Dashboard")
    st.subheader(f"👋 Welcome, {st.session_state.username}!")
    
    xp_needed = st.session_state.level * 100  
    progress_percent = min(st.session_state.xp_points / xp_needed, 1.0) * 100

    st.markdown(f"""
        <div style="width: 100%; background-color: #ddd; border-radius: 10px;">
            <div style="height: 20px; border-radius: 10px; background: linear-gradient(90deg, #0b7bb8, #0fa399); width: {progress_percent}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    st.write(f"XP: {st.session_state.xp_points} / {xp_needed}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🆙 Level", st.session_state.level)
    with col2:
        st.metric("💰 MindCoins", st.session_state.mindcoins)
    with col3:
        st.metric("🔥 Streak", f"{st.session_state.streak} days")

# Page Navigation Logic
if st.session_state.page == "home":
    st.title("Welcome to MindMate AI! 🧠✨")
    st.write("Your personal mental wellness companion.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

elif st.session_state.page == "signup":
    st.title("📝 Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Create Account"):
        if username and password:
            if username in st.session_state.users:
                st.warning("⚠️ Username already exists. Try another one.")
            else:
                st.session_state.users[username] = {"password": password}
                st.success("✅ Account created! Please log in.")
                time.sleep(1)
                st.session_state.page = "login"
                st.rerun()
        else:
            st.warning("Please fill in all fields.")

elif st.session_state.page == "login":
    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "dashboard"
            st.success("✅ Login successful! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")

elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    # Sidebar Navigation
    st.sidebar.title("🔍 Navigation")
    selected_page = st.sidebar.radio(
        "Go to:", ["🏠 Dashboard", "🔥 Challenges", "🧠 AI Therapist", "⚙️ Settings", "❓ Help & Support", "🎶 Playlist", "📖 Book Recommendations", "🛒 Shop"]
    )

    # Dashboard
    if selected_page == "🏠 Dashboard":
        render_dashboard()

    # --- Wellbeing Challenges ---
    elif selected_page == "🔥 Challenges":
        st.title("🔥 Wellbeing Challenges")
        challenges = ["📝 Write in your journal", "🎶 Listen to a song", "🤝 Compliment someone", "🧘 Meditate", "🚶 Walk 10 minutes", "📖 Read 5 pages"]

        for i, challenge in enumerate(challenges):
            if st.button(f"✅ {challenge}", key=f"challenge_{i}"):
                st.session_state.xp_points += 20
                st.session_state.mindcoins += 5
                st.session_state.streak += 1
                st.success(f"🎉 You completed the challenge: {challenge}")
                check_level_up()
                time.sleep(2)
                st.rerun()

    # --- AI Chatbot ---
    elif selected_page == "🧠 AI Therapist":
        st.title("🧠 AI Therapist")
        user_input = st.text_area("📝 How are you feeling?")
        if st.button("Get Advice"):
            if user_input.strip():
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(user_input)
                st.success(response.text)
                st.session_state.xp_points += 10
                st.session_state.mindcoins += 2
                check_level_up()
            else:
                st.warning("Enter your feelings to get advice.")

    # --- Account Settings ---
    elif selected_page == "⚙️ Settings":
        st.title("⚙️ Account Settings")
        new_password = st.text_input("New Password", type="password")
        if st.button("Update Password"):
            if new_password:
                st.session_state.users[st.session_state.username]["password"] = new_password
                st.success("🔒 Password updated!")
            else:
                st.warning("Enter a new password.")

        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.success("Logged Out. Redirecting...")
            time.sleep(1)
            st.rerun()

    # --- Shop ---
    elif selected_page == "🛒 Shop":
        st.title("🛒 Shop")
        st.subheader("Spend your MindCoins on awesome rewards!")
        
        # Define items in the shop and their cost
        shop_items = {
            "🧘‍♀️ Meditation App Subscription (50 MindCoins)": 50,
            "🎶 Playlist Generator (30 MindCoins)": 30,
            "📖 Book Recommendation (40 MindCoins)": 40,
            "🍫 Chocolate Bar (20 MindCoins)": 20,
        }

        # Display items and allow user to purchase
        for item, cost in shop_items.items():
            if st.button(f"Buy {item} - {cost} MindCoins"):
                if st.session_state.mindcoins >= cost:
                    st.session_state.mindcoins -= cost
                    st.success(f"🎉 You bought: {item}!")
                    
                    # Unlock Playlist Generator if purchased
                    if item == "🎶 Playlist Generator (30 MindCoins)":
                        st.session_state.has_playlist_generator = True
                    
                    # Unlock Book Recommendation if purchased
                    if item == "📖 Book Recommendation (40 MindCoins)":
                        st.session_state.has_book_recommendation = True
                else:
                    st.warning("❌ You don't have enough MindCoins.")

    # --- Playlist ---
    elif selected_page == "🎶 Playlist":
        if st.session_state.has_playlist_generator:
            st.title("🎶 Personalized Playlist")
            user_input = st.text_area("Enter your mood", height=120)
            song_preview = "Generate a playlist for the following mood: "

            if st.button("Generate Playlist", key="ai_chat_button_2"):
                if user_input.strip():
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(song_preview + user_input)
                    st.write("🤖 AI Generated Playlist:")
                    st.success(response.text)
        else:
            st.warning("🔒 This feature is locked. Please purchase the Playlist Generator in the Shop to unlock it.")
    
    # --- Book Recommendation ---
    elif selected_page == "📖 Book Recommendations":
        if st.session_state.has_book_recommendation:
            book_preset = "Suggest a book recommendation if this is my mood:"
            st.title("📖 AI Book Recommendations")
            user_input = st.text_area("📝 Enter your mood for a book recommendation!")
            if st.button("Get Book"):
                if user_input.strip():
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(book_preset + user_input)
                    st.success(response.text)
                    st.session_state.xp_points += 10
                    st.session_state.mindcoins += 2
                    check_level_up()
                else:
                    st.warning("Enter your feelings to get advice.")
        else:
            st.warning("🔒 This feature is locked. Please purchase the Book Recommendation in the Shop to unlock it.")
    # --- Help & Support ---
    elif selected_page == "❓ Help & Support":
        st.title("❓ Frequently Asked Questions")
        faqs = {
            "What is MindMate AI?": "MindMate AI is a gamified mental wellness app designed to enhance mental health and well-being through engaging and interactive experiences.",
            "How do I earn XP?": "Earn XP by completing daily challenges, maintaining streaks, leveling up, and participating in activities.",
            "What are MindCoins?": "MindCoins are in-app currency used for purchasing rewards in the shop.",
        }
        for question, answer in faqs.items():
            with st.expander(question):
                st.write(answer)