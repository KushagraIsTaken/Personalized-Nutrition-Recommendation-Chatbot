import pandas as pd

def generate_prompt(user_category: str, nutrition_data: pd.DataFrame) -> str:
    """Generate a personalized prompt for the chatbot."""
    advice = "Based on your economic category, here's a nutritional recommendation:\n"
    if user_category == "Economically Weak":
        affordable_foods = nutrition_data[nutrition_data['Energy'] > 100]
    elif user_category == "Middle Income":
        affordable_foods = nutrition_data[nutrition_data['Protein'] > 5]
    else:
        affordable_foods = nutrition_data

    for _, row in affordable_foods.iterrows():
        advice += f"- {row['Food Description']} ({row['Measure Description']}, {row['Energy']} kcal)\n"
    return advice
