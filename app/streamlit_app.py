import streamlit as st
import sys
import os
from groq import Groq

# Set the page configuration FIRST
st.set_page_config(
    page_title="Equalizer X",
    page_icon="🤖",
    layout="wide",  # Optional: "centered" or "wide"
    initial_sidebar_state="expanded"  # Optional: "collapsed" or "expanded"
)

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

st.markdown(
    """
    <style>
    /* Gradient background for the entire app */
.main {
    background: transparent;
    color: white;
}

/* Chat message container with 3D shadow effect */
.chat-message {
    padding: 10px;
    margin: 10px 0;
    border-radius: 10px;
    box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.6), -5px -5px 15px rgba(255, 255, 255, 0.1);
}
.chat-message.user {
    background-color: rgba(72, 61, 139, 0.8);
}
.chat-message.assistant {
    background-color: rgba(58, 48, 122, 0.8);
}

/* Customize font and layout */
.stMarkdown {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 1.1rem;
}

/* Text input styling */
.stTextInput input {
    background-color: transparent !important;
    color: white !important;
    border-radius: 10px;
    padding: 12px;
    border: none;
    outline: none;
    box-shadow: none;
}

.stTextInput input::placeholder {
    color: #bbb !important;
    opacity: 0.8;
}

.stTextInput div {
    margin-bottom: 0px;
}

/* Header Styling */
.css-1c4k2f4 {
    background: transparent;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.css-1c4k2f4 h1 {
    font-size: 2.5rem;
}

</style>
    """,
    unsafe_allow_html=True,
)


# Streamlit app layout
st.title("Equalizer X 🤖")

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
    role_class = "assistant" if msg["role"] == "assistant" else "user"
    st.markdown(
        f"""
        <div class="chat-message {role_class}">
            <div class="stMarkdown">{msg["content"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
