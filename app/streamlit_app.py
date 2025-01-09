import streamlit as st
import sys
import os
from groq import Groq

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessing import load_data, preprocess_nutrition_data
from models.income_analysis import analyze_economic_background_logistic_svm_knn
from models.chatbot_prompting import generate_prompt
from app.chatgroq_integration import chat_with_groq

# Load datasets
income_data = load_data("data/PerCapita.csv")
nutrition_data = preprocess_nutrition_data(load_data("data/NutritionDatabase.csv"))

# Initialize conversation history
conversation_history = [{"role": "system", "content": "You are a healthcare chatbot providing personalized nutritional advice."}]

# Streamlit app layout
st.set_page_config(page_title="Healthcare Chatbot", page_icon="🤖")
st.title("Healthcare Chatbot 🤖")

# Sidebar for user inputs
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

analysis_method = st.sidebar.selectbox("Select analysis method:", ["logistic", "svm", "knn"])

# Chat interface
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Economic analysis
    year = "2023"  # Fixed year value
    user_category = analyze_economic_background_logistic_svm_knn(state, income_data, year, method=analysis_method)

    # Generate prompt with nutritional data
    nutritional_prompt = generate_prompt(user_category, nutrition_data)

    # Get response from ChatGroq with context
    response = chat_with_groq(prompt, st.session_state.messages, state, user_category, nutritional_prompt)
    st.write(f"Analysis Method: {analysis_method}")

    # Append chatbot response to conversation history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
