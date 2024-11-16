# kundali_chatbot.py

import openai
from kundali_calculations import calculate_kundali, prepare_kundali_summary
import os

def initialize_chatbot(kundali_summary, openai_api_key, model_id="ft:gpt-4o-2024-08-06:personal:kundali-analysis-2:ASW1lwhF"):
    """
    Initializes the chatbot with the Kundali summary as context.
    
    Parameters:
        kundali_summary (str): The summary of the Kundali report.
        openai_api_key (str): Your OpenAI API key.
        model_id (str): The OpenAI model ID to use (default is "gpt-4").
        
    Returns:
        tuple: A tuple containing the conversation history list and the model ID.
    """
    # Set OpenAI API key
    openai.api_key = openai_api_key
    
    # Initialize conversation history with the system prompt
    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are an astrological chatbot. Utilize the following Kundali report to provide accurate and personalized predictions based on the user's queries. "
                "Provide detailed life predictions categorized into sections such as Personality, Career, Relationships, Health, and Spirituality. "
                "Use bullet points for clarity and ensure each section is comprehensive, regardless of how the user phrases their question.\n\n"
                f"{kundali_summary}"
            )
        }
    ]
    
    return conversation_history, model_id

def get_chatbot_response(conversation_history, model_id="gpt-4"):
    """
    Sends the conversation history to OpenAI's API and retrieves the chatbot's response.
    
    Parameters:
        conversation_history (list): The list of messages in the conversation history.
        model_id (str): The OpenAI model ID to use (default is "gpt-4").
        
    Returns:
        str: The chatbot's response or an error message.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=conversation_history,
            temperature=0.8,        # Adjusted for better coherence
            max_tokens=2400,        # Sufficient for detailed responses
            top_p=1.0,             # Nucleus sampling for slightly more diverse responses
            frequency_penalty=0.1,  # Minimize repetitive content
            presence_penalty=0.2    # Encourage introducing new topics in responses
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error communicating with the chatbot: {e}"

def handle_chatbot_interaction(date_of_birth, time_of_birth, place_name, user_question):
    """
    Handles the entire chatbot interaction process.
    
    Parameters:
        date_of_birth (str): User's date of birth in 'YYYY-MM-DD' format.
        time_of_birth (str): User's time of birth in 'HH:MM' (24-hour) format.
        place_name (str): User's place of birth.
        user_question (str): The question posed by the user about their Kundali.
        
    Returns:
        str: The chatbot's astrological prediction or an error message.
    """
    # Perform Kundali calculations
    try:
        report = calculate_kundali(date_of_birth, time_of_birth, place_name)
    except Exception as e:
        return f"Error performing Kundali calculations: {e}"
    
    # Prepare Kundali summary
    try:
        kundali_summary = report['kundali_summary']
    except KeyError:
        return "Kundali summary not found in the report."
    
    # Retrieve OpenAI API key from environment variables
    openai_api_key ='openai_api_key'   
    if not openai_api_key:
        return "OpenAI API key not found. Please set it in the environment variables."
    
    # Initialize chatbot
    conversation_history, model_id = initialize_chatbot(kundali_summary, openai_api_key, model_id="gpt-4")
    
    # Add user's question to the conversation history
    conversation_history.append({"role": "user", "content": user_question})
    
    # Get chatbot's response
    chatbot_response = get_chatbot_response(conversation_history, model_id)
    
    return chatbot_response

# Note:
# The main function is removed to eliminate hardcoded example inputs.
# To use this script, import the 'handle_chatbot_interaction' function and call it with appropriate parameters.

