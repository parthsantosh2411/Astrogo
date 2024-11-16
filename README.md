# 🌌 **AstroGo: Your Personalized Astrology App** 🔮

---

### 📌 **Table of Contents**
1. [Introduction](#-introduction)  
2. [Features](#-features)  
3. [Requirements](#-requirements)  
4. [Installation](#-installation)  
5. [Usage](#-usage)  
6. [Methodology](#-methodology)  
7. [Models Used](#-models-used)  
8. [Data Sources](#-data-sources)  
9. [Screenshots](#-screenshots)  
10. [Results](#-results)  
11. [Conclusion](#-conclusion)

---

## 🌟 **Introduction**

**AstroGo** is an advanced astrology application that blends the ancient wisdom of Indian astrology with the power of cutting-edge AI. The app provides users with personalized astrological insights, predictions, and guidance tailored to their unique birth details. Whether you're exploring your Kundali, seeking clarity on your Mahadasha, or just curious about your life’s trajectory, **AstroGo** is your one-stop solution.  

---

## ✨ **Features**

- **📜 Kundali Analysis**: Automatically generate detailed birth charts based on user inputs (date, time, location).  
- **🔍 Yogas and Doshas Detection**: Identify astrological combinations that impact various aspects of life such as health, career, and relationships.  
- **📆 Dasha Predictions**: Receive insights into major life events during Mahadasha and Antardasha periods.  
- **🤖 AI Chatbot**: Ask astrology-related questions and get meaningful, conversational responses powered by GPT-4 Turbo.  
- **🌎 Geolocation Integration**: Precise birth location mapping using the **OpenCage API**.  

---

## 🛠️ **Requirements**

| **Requirement**        | **Details**                                                                                       |
|-------------------------|---------------------------------------------------------------------------------------------------|
| 💻 **Python**           | Version 3.8 or above                                                                             |
| 🌐 **React Native**     | For the front-end interface                                                                      |
| 🔗 **Flask**            | For backend development                                                                          |
| 📦 **Python Libraries** | `pandas`, `numpy`, `Flask`, `Flask-CORS`, `swisseph`, `spaCy`, `NLTK`, `openai`, `requests`, `json` |
| 🔑 **API Keys**         | - **OpenAI API Key**: For GPT-4 Turbo chatbot functionality. <br> - **OpenCage API Key**: For geolocation integration. |

---

## ⚙️ **Installation**

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/parthsantosh2411/Astrogo
   cd Astrogo
   ```

2. **Install Backend Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up React Native**  
   - Install Node.js and React Native CLI:  
     ```bash
     npm install
     ```
   - Run the app on your emulator or device:  
     ```bash
     npm start
     ```

4. **Configure API Keys**  
   - Add your OpenAI and OpenCage API keys to the respective configuration files.

5. **Start the Backend Server**  
   Run the Flask backend:  
   ```bash
   python app.py
   ```

---

## 🚀 **Usage**

1. Open the app on your mobile device or emulator.  
2. Enter your birth details (date, time, location) to generate a **Kundali**.  
3. Explore:  
   - Planetary analysis and house effects.  
   - Predictions based on Mahadasha-Antardasha.  
   - Chat with the AI-powered astrology assistant for instant guidance.  

---

## ⚙️ **Methodology**

### 🌠 **1. Data Collection**
- Extracted key texts from Indian astrology scriptures such as:
  - **Brihat Parashara Hora Shastra**  
  - **Phaladeepika**  
- Augmented datasets with articles from **Saptarishis Astrology**.

### 🔧 **2. Data Preprocessing**
- Cleaned and tokenized texts using **spaCy** and **NLTK**.  
- Structured datasets were created to include planetary positions, Yogas, and Doshas.

### 🤖 **3. AI Model Training**
- Fine-tuned **GPT-4 Turbo** for conversational predictions.  
- Rule-based logic for calculating:
  - Planetary strengths (strong, weak, neutral, debilitated).  
  - Yogas, Doshas, and planetary aspects (Drishtis).  

### 📊 **4. Predictive Analysis**
- Incorporated Mahadasha-Antardasha cycles and planetary influences to forecast significant life events.

---

## 🤖 **Models Used**

1. **GPT-4 Turbo (Fine-Tuned)**:  
   - Delivers conversational predictions for user queries.  
2. **Rule-Based Logic**:  
   - Implements traditional astrology algorithms for planetary strengths and Yogas.  
3. **NLP Models**:  
   - Extracts structured information from ancient texts.

---

## 📚 **Data Sources**

1. **Astrology Scriptures**:  
   - [Brihat Parashara Hora Shastra (BPHS)](https://archive.org/details/BPHSEnglish/BPHS%20-%201%20RSanthanam/page/n11/mode/2up)  
   - [Phaladeepika](https://archive.org/details/Phaladeepika2ndEd.1950ByVSubrahmanyaSastri/mode/2up)  

2. **Articles & Blogs**:  
   - [Saptarishis Astrology](https://saptarishisastrology.com/category/articles/)  

3. **APIs Used**:  
   - **OpenCage API** for geolocation.  
   - **OpenAI GPT-4 Turbo** for chatbot functionality.

---

## 🌠 About AstroGo

AstroGo is your personal AI-powered astrology companion. With a seamless combination of React Native and Flask, it uses advanced AI and traditional astrological calculations to deliver detailed, personalized readings. Perfect for astrology enthusiasts and anyone curious about their cosmic journey.

---

<p align="center">
  <strong>✨ App Screenshots ✨</strong>
</p>

<p align="center">
  <img src=https://github.com/parthsantosh2411/Astrogo/blob/main/Screenshot_20241113_114151_Expo%20Go.jpg width="220" style="padding: 10px;">
  <img src=https://github.com/parthsantosh2411/Astrogo/blob/main/Screenshot_20241113_114209_Expo%20Go.jpg width="220" style="padding: 10px;">
  
  <br>
  <img src=https://github.com/parthsantosh2411/Astrogo/blob/main/Screenshot_20241113_114230_Expo%20Go.jpg width="220" style="padding: 10px;">
  <img src=https://github.com/parthsantosh2411/Astrogo/blob/main/Screenshot_20241113_114226_Expo%20Go.jpg width="220" style="padding: 10px;">
  
</p>

---

## 🏆 **Results**

- **Kundali Generation**: Accurate planetary placements and house assignments.  
- **Prediction Accuracy**: GPT-4 chatbot delivers conversational responses aligned with astrological rules.  
- **User Experience**: The intuitive interface and chatbot enhance user engagement and satisfaction.  

---

## 💡 **Conclusion**

**AstroGo** combines the depth of Indian astrology with the intelligence of AI, making astrology accessible and engaging for everyone. With its accurate predictions and interactive chatbot, AstroGo ensures users gain deep insights into their lives.  

- **Why Choose AstroGo?**  
  - Personalized and precise Kundali analysis.  
  - Insights into Yogas, Doshas, and planetary effects.  
  - A seamless blend of traditional astrology and modern AI.

✨ Discover your destiny with AstroGo! 🌟
