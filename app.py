import streamlit as st
from model import train_model, predict
from utils import load_data, save_data
import base64
import os

# --------- Page config ---------
st.set_page_config(page_title="Dance Learning 💃", layout="wide")

# --------- Background Image ---------
def get_base64_image(image_file):
    if not os.path.exists(image_file):
        st.warning("Background image not found")
        return ""
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64_image("dance1.jpg.jpeg")

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
}}
.block-container {{
    background: rgba(0,0,0,0.6);
    padding: 2rem;
    border-radius: 15px;
}}
h1 {{
    color: white;
    text-align: center;
}}
.stButton>button {{
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

# --------- Load Data ---------
users = load_data("users.json")
bookings = load_data("bookings.json")
if not isinstance(bookings, dict):
    bookings = {}

# --------- Load Model ---------
@st.cache_resource
def get_model():
    return train_model()

model = get_model()

# --------- Title ---------
st.title("💃 Interactive Dance Learning Platform")
st.markdown("### Learn • Book • Get Recommendations")

# --------- Sidebar ---------
menu = st.sidebar.selectbox(
    "Menu",
    ["Register", "Login", "Book Class", "My Bookings", "Recommendations"]
)

# --------- Register ---------
if menu == "Register":
    st.subheader("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username in users:
            st.warning("User already exists")
        else:
            users[username] = password
            save_data("users.json", users)
            st.success("Registered Successfully!")

# --------- Login ---------
elif menu == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if users.get(username) == password:
            st.session_state["user"] = username
            st.success("Login Successful!")
        else:
            st.error("Invalid credentials")

# --------- Book Class ---------
elif menu == "Book Class":
    if "user" not in st.session_state:
        st.warning("Please login first")
    else:
        st.subheader("Book a Dance Class")
        category = st.selectbox("Category", ["Basics", "Course"])
        dance = st.selectbox("Dance Type", ["Classical", "Hip-Hop", "Contemporary"])

        if st.button("Book Now"):
            bookings.setdefault(st.session_state["user"], []).append({
                "category": category,
                "dance": dance
            })
            save_data("bookings.json", bookings)
            st.success("✅ Booking Confirmed!")

# --------- My Bookings ---------
elif menu == "My Bookings":
    if "user" not in st.session_state:
        st.warning("Login first")
    else:
        st.subheader("Your Bookings")
        user_bookings = bookings.get(st.session_state["user"], [])

        if user_bookings:
            for b in user_bookings:
                st.write(f"💃 {b['dance']} | 📘 {b['category']}")
        else:
            st.info("No bookings yet")

# --------- Recommendations ---------
elif menu == "Recommendations":
    if "user" not in st.session_state:
        st.warning("Login first")
    else:
        st.subheader("🤖 Recommended for You")

        category_map = {"Basics": 0, "Course": 1}
        dance_map = {"Classical": 0, "Hip-Hop": 1, "Contemporary": 2}

        user_data = bookings.get(st.session_state["user"], [])

        if user_data:
            last = user_data[-1]
            cat = category_map[last["category"]]
            dan = dance_map[last["dance"]]

            result = predict(model, cat, dan)

            if result[0] == 0:
                st.success("💃 Classical Basics")
            else:
                st.success("🔥 Hip-Hop Advanced")
        else:
            st.info("Book a class first")

st.markdown("---")
st.write("👩‍💻 Developed using Python, Streamlit & Machine Learning")