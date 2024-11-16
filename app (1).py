from flask import Flask, request, jsonify
from flask_cors import CORS
from kundali_calculations import calculate_kundali
from kundali_presentation import (
    display_ascendant_and_planetary_positions,
    display_planets_in_houses,
    display_current_dasha,
    display_current_antardasha,
)
import openai

# Set the OpenAI API key
openai.api_key = 'opeanai.api_key'

app = Flask(__name__)
CORS(app)

@app.route('/kundali', methods=['POST'])
def kundali():
    data = request.json
    date_of_birth = data['date_of_birth']
    time_of_birth = data['time_of_birth']
    place_of_birth = data['place_of_birth']

    report = calculate_kundali(date_of_birth, time_of_birth, place_of_birth)

    ascendant_info = display_ascendant_and_planetary_positions(report)['ascendant_info']
    planetary_info = display_ascendant_and_planetary_positions(report)['planetary_info']
    planets_info = display_planets_in_houses(report)
    current_dasha = display_current_dasha(report)
    current_antardasha = display_current_antardasha(report)

    response = {
        'ascendant_info': ascendant_info,
        'planetary_info': planetary_info,
        'planets_info': planets_info,
        'current_dasha': current_dasha,
        'current_antardasha': current_antardasha,
        'kundali_summary': report.get('kundali_summary', ''),
    }

    return jsonify(response)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    message = data['message']
    kundali_summary = data['kundaliData'].get('kundali_summary', '')

    from kundali_chatbot import get_chatbot_response

    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are an astrological chatbot. Utilize the following Kundali report to provide accurate and personalized predictions based on the user's queries. "
                "Provide detailed life predictions categorized into sections such as Personality, Career, Relationships, Health, and Spirituality. "
                "Use bullet points for clarity and ensure each section is comprehensive, regardless of how the user phrases their question.\n\n"
                f"{kundali_summary}"
            )
        },
        {
            "role": "user",
            "content": message
        }
    ]

    response_text = get_chatbot_response(conversation_history)

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

