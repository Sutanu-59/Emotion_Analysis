import streamlit as st
import time

st.set_page_config(page_title="Login / Register - Depression Analysis", page_icon="💬", layout="centered")

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

    # if st.button("Login"):
    #     user = st.session_state.users.get(email)
    #     if user and user["password"] == password:
    #         st.session_state.current_user = email
    #         st.success(f"Welcome back, {user['name']}! 💙")
    #         st.markdown("<div class='success-box'>Redirecting you to your chat...</div>", unsafe_allow_html=True)
    #         time.sleep(1.5)
    #         st.switch_page("pages/TextChat.py")
    #     else:
    #         st.error("Invalid email or password. Please try again.")

    if st.button("Login"):
        user = st.session_state.users.get(email)
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
    name = st.text_input("Full Name", key="reg_name")
    email_reg = st.text_input("Email", key="reg_email")
    password_reg = st.text_input("Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="reg_conf")

    if st.button("Register"):
        if not name or not email_reg or not password_reg:
            st.warning("Please fill in all fields.")
        elif password_reg != confirm_pass:
            st.warning("Passwords do not match.")
        elif email_reg in st.session_state.users:
            st.warning("Email already registered. Please log in.")
        else:
            st.session_state.users[email_reg] = {"name": name, "password": password_reg}
            st.success(f"Account created for {name}! 🎉 You can now log in.")
            st.markdown("<div class='success-box'>Registration successful. Please go to the Login tab.</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <hr style="border: 0.5px solid #80bfff; margin-top: 2em;">
    <p style='text-align:center; color:#004aad;'>© 2025 RERF | Depression Analysis Assistant 💬</p>
""", unsafe_allow_html=True)
