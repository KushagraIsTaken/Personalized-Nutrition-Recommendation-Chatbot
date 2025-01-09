import os
from groq import Groq
import logging



# Initialize the Groq client
client = Groq(api_key="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")



def chat_with_groq(user_input, conversation_history, state, user_category, prompt, analysis_method):
    """Send a message to the Groq API and receive a response."""
    try:
        # Prepare the context for the chatbot
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
            f"Explain the proper reasoning how you were able to reach this prescription"
        )

        # Prepare the messages for the chat completion
        messages = [{"role": "system", "content": context}]  # Start with the system context

        # Append the conversation history to the messages
        for message in conversation_history:
            messages.append(message)

        # Add the user's input as the last message
        messages.append({"role": "user", "content": user_input})

        # Perform the chat completion request
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gemma2-9b-it",  # Replace with your desired model
        )

        # Return the assistant's message from the response
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return "I'm sorry, but I couldn't process your request at this time."