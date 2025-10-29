import streamlit as st
import time
from github_utils import update_github_db_and_csv, DB_PATH

st.set_page_config(page_title="Login / Register - Depression Analysis", page_icon="💬", layout="centered")

def login_user(email, password):
    import sqlite3
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    data = c.fetchone()
    conn.close()
    
    if data:
        user_dict = {"name": data[0], "email": data[1], "password": data[2]}
        return user_dict
    else:
        return None

# --- Custom CSS: gradient + text colors ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
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
        input, textarea {
            background-color: #f6fbff !important;
            color: #002b5b !important;
            border: 1px solid #70b5ff !important;
            border-radius: 10px !important;
            caret-color: #004a9f !important; /* Blinker color */
        }
        .stTextInput>div>div>input {
            background-color: #f6fbff;
            color: #002b5b;
            border: 1px solid #70b5ff;
            border-radius: 10px;
            padding: 0.6em;
        }
        .stButton>button {
            background: linear-gradient(90deg, #0066ff, #00aaff);
            color: white !important;
            border-radius: 25px !important;
            padding: 0.5em 2em !important;
            border: none !important;
            font-weight: bold;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #004aad, #0097e6);
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4);
        }
        .tab-header {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 1em;
            color: #003366;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .success-box {
            border: 1px solid #00aaff;
            border-radius: 10px;
            padding: 1em;
            background-color: #e8f5ff;
            color: #003366;
            text-align: center;
            margin-top: 1em;
        }
        .stTabs [role="tablist"] {
            justify-content: center;
            border-bottom: 2px solid #80bfff;
        }
        .stTabs [role="tab"] {
            color: #003366 !important;
            font-weight: bold;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            color: #004aad !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session states ---
if "users" not in st.session_state:
    st.session_state.users = {}

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --- Header ---
st.markdown("<div class='tab-header'>🧠 Welcome to Depression Analysis</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#003366;'>Please log in or create an account to continue your mental wellness journey.</p>", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

# --- Login Tab ---
with tab1:
    st.subheader("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login"):
        # user = st.session_state.users.get(email)
        user = login_user(email, password)
        if user and user["password"] == password:
            st.session_state.current_user = email
            st.success(f"Welcome back, {user['name']}! 💙")
            st.markdown("<div class='success-box'>Redirecting you to your chat...</div>", unsafe_allow_html=True)
            time.sleep(1.5)
            st.switch_page("pages/app.py")   # ✅ redirect to chat page
        else:
            st.error("Invalid email or password. Please try again.")


# --- Register Tab ---
with tab2:
    st.subheader("Create a new account")
    fullname = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    cpass = st.text_input("Confirm Password", type="password", key="reg_conf")
    token = st.secrets["GITHUB_TOKEN"]

    if st.button("Register"):
        if not fullname or not email or not password:
            st.warning("Please fill in all fields.")
        elif password != cpass:
            st.warning("Passwords do not match.")
        elif email in st.session_state.users:
            st.warning("Email already registered. Please log in.")
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            try:
                c.execute(
                    'INSERT INTO users (fullname, email, password, cpass) VALUES (?, ?, ?, ?)',
                    (fullname, email, password, cpass)
                )

                conn.commit()
                st.success("🎉 Account created successfully!")
                st.info("You can now log in.")
                if token:
                    update_github_db_and_csv(token)
            except sqlite3.IntegrityError:
                st.error("Username already exists.")
            conn.close()

            st.session_state.users[email] = {"name": fullname, "password": password}
            st.success(f"Account created for {fullname}! 🎉 You can now log in.")
            st.markdown("<div class='success-box'>Registration successful. Please go to the Login tab.</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <hr style="border: 0.5px solid #80bfff; margin-top: 2em;">
    <p style='text-align:center; color:#004aad;'>© 2025 RERF | Depression Analysis Assistant 💬</p>
""", unsafe_allow_html=True)

