import os
from groq import Groq
import logging

client = Groq(api_key = "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")

def chat_woth_groq(user_input, conversation_history, state, user_category, prompt):
    """Send a message to the Groq API and receive a response."""
    try: 
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
        
        messages = [{"role": "system", "content": contect}]
        
        for message in conversation_history:
            messages.append(message)
            
        messages.append({"role": "user", "content": user_input})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gemma2-9b-it"
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return "I'm sorry, but I couldn't process your request at this time."
            
        