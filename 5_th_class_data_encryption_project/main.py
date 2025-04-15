import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import json
import time
import os

# Page configuration
st.set_page_config(
    page_title="Secure Data Encryption System",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
    }
    .stButton button {
        width: 100%;
    }
    .nav-button {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        cursor: pointer;
        margin: 5px;
    }
    .nav-button:hover {
        background-color: #e0e2e6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

if 'users' not in st.session_state:
    st.session_state.users = {}

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

if 'locked_until' not in st.session_state:
    st.session_state.locked_until = 0

if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.key)

# File paths
USERS_FILE = "users.json"
DATA_FILE = "encrypted_data.json"

# Load users from file
def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                st.session_state.users = json.load(f)
    except Exception as e:
        st.error(f"Error loading users: {e}")

# Save users to file
def save_users():
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(st.session_state.users, f)
    except Exception as e:
        st.error(f"Error saving users: {e}")

# Load encrypted data from file
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                st.session_state.stored_data = json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Save encrypted data to file
def save_data():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.stored_data, f)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Load data at startup
load_users()
load_data()

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text):
    return st.session_state.cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_password(passkey)
    
    # Check if the encrypted_text exists and belongs to the current user
    if (encrypted_text in st.session_state.stored_data and 
        st.session_state.stored_data[encrypted_text]["user"] == st.session_state.current_user):
        # Check if the passkey matches
        if st.session_state.stored_data[encrypted_text]["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            try:
                return st.session_state.cipher.decrypt(encrypted_text.encode()).decode()
            except Exception:
                return None
    
    st.session_state.failed_attempts += 1
    return None

# Navigation functions
def go_to_page(page):
    st.session_state.page = page
    st.rerun()

def logout():
    st.session_state.current_user = None
    st.session_state.page = 'welcome'
    st.rerun()

# Check if system is locked
current_time = time.time()
if st.session_state.locked_until > current_time:
    st.error(f"🔒 System locked due to too many failed attempts. Try again in {int(st.session_state.locked_until - current_time)} seconds.")
    st.stop()

# Welcome Page
if st.session_state.page == 'welcome':
    st.markdown("<h1 class='main-header'>🔒 Secure Data Encryption System</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Welcome to the Secure Data System</h2>", unsafe_allow_html=True)
    st.write("This application allows you to securely store and retrieve sensitive data using encryption.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("New User?")
        st.write("Create an account to get started with secure data encryption.")
        if st.button("Register", key="register_btn"):
            go_to_page('register')
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Existing User?")
        st.write("Login to access your encrypted data.")
        if st.button("Login", key="login_btn"):
            go_to_page('login')
        st.markdown("</div>", unsafe_allow_html=True)

# Registration Page
elif st.session_state.page == 'register':
    st.markdown("<h1 class='main-header'>🔒 Secure Data Encryption System</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Create an Account</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if not username or not password:
            st.error("Username and password are required!")
        elif username in st.session_state.users:
            st.error("Username already exists! Please choose another one.")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Register the user
            st.session_state.users[username] = {
                "password": hash_password(password),
                "created_at": time.time()
            }
            save_users()
            st.success("Registration successful! Please login.")
            time.sleep(1)
            go_to_page('login')
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Back to Welcome", key="back_to_welcome"):
        go_to_page('welcome')

# Login Page
elif st.session_state.page == 'login':
    st.markdown("<h1 class='main-header'>🔒 Secure Data Encryption System</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Login to Your Account</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not username or not password:
            st.error("Username and password are required!")
        elif username not in st.session_state.users:
            st.error("Username not found!")
        elif st.session_state.users[username]["password"] != hash_password(password):
            st.error("Incorrect password!")
        else:
            st.session_state.current_user = username
            st.success(f"Welcome back, {username}!")
            time.sleep(1)
            go_to_page('dashboard')
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Back to Welcome", key="back_to_welcome"):
        go_to_page('welcome')

# Dashboard Page (after login)
elif st.session_state.page == 'dashboard':
    if not st.session_state.current_user:
        go_to_page('login')
    
    st.markdown("<h1 class='main-header'>🔒 Secure Data Encryption System</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Logged in as: <b>{st.session_state.current_user}</b></p>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Store Data", key="store_data_btn"):
            go_to_page('store_data')
    with col2:
        if st.button("Retrieve Data", key="retrieve_data_btn"):
            go_to_page('retrieve_data')
    with col3:
        if st.button("Logout", key="logout_btn"):
            logout()
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Your Dashboard</h2>", unsafe_allow_html=True)
    
    # Count user's encrypted data
    user_data_count = sum(1 for _, data in st.session_state.stored_data.items() 
                          if data.get("user") == st.session_state.current_user)
    
    st.write(f"You have {user_data_count} encrypted entries stored.")
    
    st.markdown("""
    ### What would you like to do?
    
    - **Store Data**: Encrypt and securely store your sensitive information
    - **Retrieve Data**: Decrypt and view your stored information
    
    Your data is encrypted using a secure algorithm and can only be accessed with the correct passkey.
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Store Data Page
elif st.session_state.page == 'store_data':
    if not st.session_state.current_user:
        go_to_page('login')
    
    st.markdown("<h1 class='main-header'>🔒 Secure Data Encryption System</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Logged in as: <b>{st.session_state.current_user}</b></p>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Store Data Securely</h2>", unsafe_allow_html=True)
    
    data_title = st.text_input("Data Title (optional)")
    user_data = st.text_area("Enter Data to Encrypt:", height=150)
    passkey = st.text_input("Enter Encryption Passkey:", type="password", 
                           help="This is the key you'll need to decrypt your data later")
    confirm_passkey = st.text_input("Confirm Passkey:", type="password")
    
    if st.button("Encrypt & Save"):
        if not user_data or not passkey:
            st.error("Data and passkey are required!")
        elif passkey != confirm_passkey:
            st.error("Passkeys do not match!")
        else:
            hashed_passkey = hash_password(passkey)
            encrypted_text = encrypt_data(user_data, passkey)
            
            # Store with user information
            st.session_state.stored_data[encrypted_text] = {
                "encrypted_text": encrypted_text,
                "passkey": hashed_passkey,
                "user": st.session_state.current_user,
                "title": data_title if data_title else "Untitled",
                "created_at": time.time()
            }
            
            save_data()
            st.success("✅ Data stored securely!")
            
            # Display the encrypted text for the user to copy
            st.subheader("Your Encrypted Data:")
            st.code(encrypted_text, language="text")
            st.info("👆 Copy this encrypted text. You'll need it to retrieve your data later.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Dashboard", key="back_to_dashboard"):
            go_to_page('dashboard')
    with col2:
        if st.button("Go to Retrieve Data", key="go_to_retrieve"):
            go_to_page('retrieve_data')

# Retrieve Data Page
elif st.session_state.page == 'retrieve_data':
    if not st.session_state.current_user:
        go_to_page('login')
    
    st.markdown("<h1 class='main-header'>🔒 Secure Data Encryption System</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Logged in as: <b>{st.session_state.current_user}</b></p>", unsafe_allow_html=True)
    
    # Display attempts remaining
    attempts_remaining = 3 - st.session_state.failed_attempts
    st.info(f"Attempts remaining: {attempts_remaining}")
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Retrieve Your Data</h2>", unsafe_allow_html=True)
    
    # Show user's stored data titles if available
    user_data = {k: v for k, v in st.session_state.stored_data.items() 
                if v.get("user") == st.session_state.current_user}
    
    if user_data:
        st.subheader("Your Stored Data:")
        for encrypted_text, data in user_data.items():
            st.write(f"- {data.get('title', 'Untitled')}")
            if st.button(f"Use this entry: {data.get('title', 'Untitled')}", key=encrypted_text):
                st.session_state.selected_encrypted_text = encrypted_text
                st.rerun()
    else:
        st.warning("You don't have any stored data yet. Go to Store Data to encrypt some information.")
    
    # If user selected an entry or wants to enter manually
    if 'selected_encrypted_text' in st.session_state:
        st.subheader("Selected Entry:")
        st.code(st.session_state.selected_encrypted_text, language="text")
    else:
        st.subheader("Or enter encrypted text manually:")
    
    encrypted_text = st.text_area("Enter Encrypted Data:", 
                                 value=st.session_state.get('selected_encrypted_text', ''),
                                 height=100)
    passkey = st.text_input("Enter Passkey:", type="password")
    
    if st.button("Decrypt"):
        if not encrypted_text or not passkey:
            st.error("Encrypted data and passkey are required!")
        else:
            decrypted_text = decrypt_data(encrypted_text, passkey)
            
            if decrypted_text:
                st.success("✅ Decryption successful!")
                st.subheader("Decrypted Data:")
                st.code(decrypted_text, language="text")
                
                # Reset selected entry
                if 'selected_encrypted_text' in st.session_state:
                    del st.session_state.selected_encrypted_text
            else:
                st.error(f"❌ Incorrect passkey or data! Attempts remaining: {3 - st.session_state.failed_attempts}")
                
                if st.session_state.failed_attempts >= 3:
                    # Lock the system for 30 seconds
                    st.session_state.locked_until = time.time() + 30
                    st.warning("🔒 Too many failed attempts! System locked for 30 seconds.")
                    st.session_state.failed_attempts = 0
                    time.sleep(1)
                    go_to_page('dashboard')
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation button
    if st.button("Back to Dashboard", key="back_to_dashboard"):
        if 'selected_encrypted_text' in st.session_state:
            del st.session_state.selected_encrypted_text
        go_to_page('dashboard')

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>🔒 Secure Data Encryption System v2.0 | GIAIC Python Assignment</p>", unsafe_allow_html=True)