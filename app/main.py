import sys
import os
from flask import Flask, render_template, request, jsonify


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessing import load_data, preprocess_nutrition_data
from models.income_analysis import analyze_economic_background_kmeans
from models.chatbot_prompting import generate_prompt
from app.chatgroq_integration import chat_with_groq

app = Flask(__name__)


income_data = load_data("data/PerCapita.csv")
nutrition_data = preprocess_nutrition_data(load_data("data/NutritionDatabase.csv"))


conversation_history = [{"role": "system", "content": "You are a healthcare chatbot providing personalized nutritional advice."}]

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/send', methods=['POST'])
def send_message():
    user_input = request.json['message']
    state = request.json['state']  
    year = "2023"  

    
    user_category = analyze_economic_background_kmeans(state, income_data, year)

   
    prompt = generate_prompt(user_category, nutrition_data)

    
    context = (
        f"You are a healthcare chatbot providing personalized nutritional advice based on economic status. "
        f"The user is categorized as: {user_category}. "
        f"The user is from: {state}. "
        f"Your responses should include nutritional values such as vitamins and minerals from the knowledge base. "
        f"Ensure that your answers are relevant and do not exceed the scope of nutritional advice. "
        f"Here are some nutritional recommendations: {prompt}. "
        f"Give Nutritional Values like Vitamins, Minerals from the knowledge base too. "
        f"Also comment about the price of the commodity and show that it is as per the income bracket. "
        f"Answer like a chatbot short and crisp, make the chatbot an interactive experience use emojis and stuff. Add humour too."
    )

    
    conversation_history.append({"role": "user", "content": user_input})

    
    response = chat_with_groq(user_input, conversation_history)
    
    
    conversation_history.append({"role": "assistant", "content": response})

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)