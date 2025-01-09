"""import streamlit as st
import sys
import os
from groq import Groq


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessing import load_data, preprocess_nutrition_data
from models.income_analysis import analyze_economic_background_kmeans
from models.chatbot_prompting import generate_prompt
from app.chatgroq_integration import chat_with_groq

income_data = load_data("data/PerCapita.csv")
nutrition_data = preprocess_nutrition_data(load_data("data/NutritionDatabase.csv"))

conversation_history = [{"role": "system", "content": "You are a healthcare chatbot providing personalized nutritional advice."}]

st.set_page_config(page_title="Healthcare Chatbot", page_icon="🤖")
st.title("Healthcare Chatbot 🤖")

st.sidebar.header("User Input")
state = st.sidebar.selectbox("Select your state:", [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
])

if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.markdown(f"<div style='text-align: right;'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left;'><b>Chatbot:</b> {msg['content']}</div>", unsafe_allow_html=True)

user_input = st.text_input("Type your message here:")

if st.button("Send"):
    if user_input:
        year = "2023"  # Fixed year value
        user_category = analyze_economic_background_kmeans(state, income_data, year)

        prompt = generate_prompt(user_category, nutrition_data)

        st.session_state.messages.append({"role": "user", "content": user_input})

        response = chat_with_groq(user_input, st.session_state.messages, state, user_category, prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})

        st.text_area("Chatbot Response:", value=response, height=200)
    else:
        st.warning("Please enter a message.")"""

import streamlit as st
import sys
import os
from groq import Groq

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessing import load_data, preprocess_nutrition_data
from models.income_analysis import analyze_economic_background_kmeans
from models.chatbot_prompting import generate_prompt
from app.chatgroq_integration import chat_with_groq

income_data = load_data("data/PerCapita.csv")
nutrition_data = preprocess_nutrition_data(load_data("data/NutritionDatabase.csv"))

conversation_history = [{"role": "system", "content": "You are a healthcare chatbot."}]

st.set_page_config(page_title="Healthcare Chatbot", page_icon="🤖")
st.title("Healthcare Chatbot 🤖")

st.sidebar.header("User Input")
state = st.sidebar.selectbox("Select your state:", [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
])

if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    year = "2023"  
    user_category = analyze_economic_background_kmeans(state, income_data, year)

    nutritional_prompt = generate_prompt(user_category, nutrition_data)

    response = chat_with_groq(prompt, st.session_state.messages, state, nutritional_prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
