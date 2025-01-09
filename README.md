# EqualizerX: AI-Powered Pediatric Nutrition Chatbot

# Team Name : Trinity AI 
# PID - 9


EqualizerX is an innovative AI-powered chatbot system addressing pediatric health inequities through personalized nutrition recommendations. The system leverages machine learning models and data from USDA and Census Bureau to provide accessible, tailored dietary guidance for children aged 2-19.

## Project Overview

This project aims to bridge socioeconomic gaps in pediatric health by combining logistic regression, KNN, and SVM models with state-specific demographic data, Gini index, and local food availability information. The system provides real-time, personalized nutrition recommendations while considering both individual health needs and socioeconomic factors.

## Features

- Personalized nutrition recommendations based on socioeconomic factors
- Integration with USDA and Census Bureau data
- Natural Language Processing for conversational interface
- Machine learning models: KNN, Logistic Regression, and SVM
- Real-time adaptability based on user feedback
- Consideration of local food availability and affordability

## Environment Setup

### Prerequisites
- Python 3.8 or higher
- Anaconda or Miniconda

### Creating the Environment

1. Clone the repository:
```bash
git clone https://github.com/KushagraIsTaken/Personalized-Nutrition-Recommendation-Chatbot
cd Personalized-Nutrition-Recommendation-Chatbot
```

2. Create a new conda environment:
```bash
conda create --name equalizerx 
```

3. Activate the environment:
```bash
conda activate equalizerx
```

4. Install required packages:
```bash
pip install -r requirements.txt
```
## Machine Learning Models

The project implements three different machine learning approaches:

1. **K-Nearest Neighbors (KNN)**
   - Used for similarity-based recommendation
   - Helps identify similar dietary patterns

2. **Logistic Regression**
   - Primary model for socioeconomic classification
   - Predicts probability of belonging to specific economic groups

3. **Support Vector Machine (SVM)**
   - Used for complex pattern recognition in dietary habits
   - Helps in classification of dietary requirements

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- USDA Database
- United States Census Bureau
- KIIT University School of Computer Engineering

## Contact

For any queries, please contact:
- Email: 2205044@kiit.ac.in

## Live Demo

Check out the live application here: [Personalized Nutrition App](https://kushagraistaken-personalized-nutrition--appstreamlit-app-2en90s.streamlit.app/)

## Citation

If you use this project in your research, please cite:
```
Agrawal, K., Gupta, P., & Nandi, D. (2025). AI-Powered Personalized Nutrition 
for Pediatric Health Equity. International Conference on Distributed Computing 
& Intelligent Technology.
```
