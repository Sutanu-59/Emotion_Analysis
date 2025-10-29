import streamlit as st
import base64
from PIL import Image

st.set_page_config(
    page_title="Depression Analysis | Home",
    page_icon="🤖",
    layout="wide"
)

# Hide sidebar completely
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stAppViewBlockContainer"] {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Navigation Helper ---
def redirect_to_login():
    st.switch_page("pages/Login.py")

# --- 🌈 Combined White–Blue Theme CSS ---
st.markdown("""
    <style>
        /* Background + base text */
        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #d0e7ff 50%, #a9d6ff 100%);
            color: #002b5b;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #004a9f !important;
        }
        label, p, span {
            color: #002b5b !important;
        }

        /* Navbar Buttons */
        .login-button a, .stButton>button {
            background: linear-gradient(90deg, #0066ff, #00aaff);
            color: white !important;
            border-radius: 25px !important;
            padding: 0.5em 1.5em !important;
            border: none !important;
            font-weight: bold;
            transition: 0.3s ease-in-out;
            text-decoration: none;
            text-align: center;
            display: inline-block;
        }
        .login-button a:hover, .stButton>button:hover {
            background: linear-gradient(90deg, #004aad, #0097e6);
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4);
            color: white !important;
        }

        /* Navbar Layout */
        .nav-bar {
            display: flex;
            justify-content: flex-end;
            margin: 1em 2em 0 0;
            gap: 1em;
        }

        /* Page Titles */
        .big-title {
            font-size: 4em;
            font-weight: bold;
            color: #003366;
            text-align: center;
            padding-top: 1em;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            animation: fadeIn 2s ease-in-out;
        }
        .subtitle {
            font-size: 1.5em;
            color: #004a9f;
            text-align: center;
            margin-top: 1em;
            animation: fadeIn 3s ease-in-out;
        }

        /* Center Button */
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 2em;
            animation: fadeIn 4s ease-in-out;
        }
        .button-style button {
            font-size: 1.2em;
            padding: 0.75em 2em;
            border-radius: 40px;
            background: linear-gradient(90deg, #0066ff, #00aaff);
            border: none;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .button-style button:hover {
            background: linear-gradient(90deg, #004aad, #0097e6);
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4);
        }

        /* Image + Animation */
        .fade-in-section {
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 1s ease-in-out forwards;
        }
        .image-bounce {
            animation: bounceIn 2s ease-in-out;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-radius: 12px;
        }
        .image-bounce:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 20px rgba(0, 0, 128, 0.2);
        }
        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes bounceIn {
            0% { transform: scale(0.9); opacity: 0; }
            60% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); }
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Top Navigation Bar ---
with st.container():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        if st.button("Let's Chat 💬", key="login_nav", use_container_width=True,):
            redirect_to_login()
    with col3:
        st.markdown("<div class='login-button'><a href='#videos'>Video Chat</a></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='login-button'><a href='#voice'>Voice Chat</a></div>", unsafe_allow_html=True)
    with col5:
        st.markdown("<div class='login-button'><a href='#contact'>Contact Us</a></div>", unsafe_allow_html=True)

# --- Big heading and subtitle ---
st.markdown("""
    <div class="big-title">🧠 Depression Analysis</div>
    <div class="subtitle">Your mindful AI companion for emotional well-being.<br />Powered by RERF.</div>
""", unsafe_allow_html=True)

# --- CTA Button ---
st.markdown("""
    <div class="center-button">
        <div class="button-style">
            <a href="#start"><button>Start Your Journey</button></a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Intro Section ---
st.markdown("""
    <div id="start" class="fade-in-section" style="margin-top: 8em;">
        <h2 style="color:#004aad; text-align:center">Welcome to the Mindful AI Experience</h2>
        <p style="color:#002b5b; text-align:center; max-width: 700px; margin: auto;">
            This app helps you understand your emotions and provides guidance through text, audio, and video conversations.
            Powered by ## — a machine learning model trained to support your mental wellness journey.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Mindful AI Section ---
st.markdown("""
    <div id="login" class="fade-in-section" style="margin-top: 5em; text-align: center;">
        <h3 style="color:#004aad;">Mindful AI</h3>
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 1em; margin-top: 2em;">
            <div>
                <img src="https://static.vecteezy.com/system/resources/thumbnails/022/756/603/small/conceptual-image-of-a-human-head-with-colorful-brain-and-autumn-leaves-mental-health-concept-ai-generated-artwork-photo.jpg" alt="image" class="image-bounce" style="max-width: 300px;"/>
                <p>Mind is a powerful thing.</p>
            </div>
            <div>
                <img src="https://t4.ftcdn.net/jpg/02/71/09/15/360_F_271091539_7fVM1L9nhbpHlQAbEs8ZIrAEPAd9PxlM.jpg" alt="image" class="image-bounce" style="max-width: 300px;"/>
                <p>Be mindful of your thoughts.</p>
            </div>
            <div>
                <img src="https://psychologyfanatic.com/wp-content/uploads/2024/01/Psychological-Disorders.-Psychology-Fanatic-article-feature-image.webp" alt="image" class="image-bounce" style="max-width: 300px;"/>
                <p>Take care of your mental health.</p>
            </div>
        </div>
        <p style="margin-top: 2em;">Your mindful AI companion. Share and explore your thoughts.</p>
    </div>
""", unsafe_allow_html=True)

# --- Chat Modes (Text / Audio / Video) ---
st.markdown("""
    <div id="text" class="fade-in-section" style="display: flex; justify-content: space-between; align-items: center; margin-top: 5em;">
        <img src="https://tse2.mm.bing.net/th/id/OIP.ZVVA9mmlcNAYlLRJiSayIwHaHa?cb=thfc1&rs=1&pid=ImgDetMain&o=7&rm=3" alt="image" class="image-bounce" style="max-width: 300px;"/>
        <div style="margin-left: 2em; text-align: center;">
            <h3 style="color:#004aad;">Text Chat</h3>
            <p>Express your thoughts through words. Reflect, understand, and grow with mindful conversations.</p>
        </div>
    </div>            
    <div id="voice" class="fade-in-section" style="display: flex; justify-content: space-between; align-items: center; margin-top: 5em;">
        <div style="margin-right: 2em; text-align: center;">
            <h3 style="color:#004aad;">Audio Chat</h3>
            <p>Prefer talking? Use audio to connect emotionally. Let your thoughts flow naturally.</p>
        </div>
        <img src="https://lessonpix.com/drawings/1845123/150x150/Call.png" alt="image" class="image-bounce" style="max-width: 400px;"/>
    </div>            
    <div id="videos" class="fade-in-section" style="display: flex; justify-content: space-between; align-items: center; margin-top: 5em;">
        <img src="https://media.istockphoto.com/id/1212577571/vector/person-holding-smartphone-and-calling-via-video-chat-mobile-app.jpg?s=612x612&w=0&k=20&c=flloizEAzFR6wQlsl1EAK_nbpSfYJIg-KnHcTB2-OWc=" alt="image" class="image-bounce" style="max-width: 300px;"/>
        <div style="margin-left: 2em; text-align: center;">
            <h3 style="color:#004aad;">Video Chat</h3>
            <p>Have a face-to-face connection with your AI companion. Share, express, and heal visually.</p>
        </div>
    </div>            
""", unsafe_allow_html=True)











