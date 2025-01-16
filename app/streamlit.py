import streamlit as st
from streamlit_chat import message
import json
from app import get_structured_perplexity_response, PROMPT_TEMPLATE

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Flight Booking Assistant")

# Chat input
user_input = st.chat_input("What's your travel plan?")

# When user submits a message
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get response from the assistant
    try:
        response_json = get_structured_perplexity_response(PROMPT_TEMPLATE, user_input)
        if response_json:
            # Parse the JSON string into a dictionary
            # response_data = json.loads(response_json)
            
            # # Create a formatted response message
            # formatted_response = ""
            # if "response" in response_data:
            #     if response_data["response"] != "success":
            #         # If clarification is needed, show the response directly
            #         formatted_response = response_data["response"]
            #     else:
            #         # Create a formatted summary of the flight details
            #         formatted_response = "Here are the details for your trip:\n\n"
            #         if "city" in response_data:
            #             formatted_response += f"📍 Destination: {response_data['city']}\n"
            #         if "airports" in response_data:
            #             formatted_response += f"✈️ Nearby airports: {', '.join(response_data['airports'])}\n"
            #         if "event_name" in response_data:
            #             formatted_response += f"🎯 Event: {response_data['event_name']}\n"
            #         if "event_start_date" in response_data:
            #             formatted_response += f"📅 Event dates: {response_data['event_start_date']} to {response_data['event_end_date']}\n"
            #         if "recommended_flight_start_date" in response_data:
            #             formatted_response += f"🛫 Recommended travel dates: {response_data['recommended_flight_start_date']} to {response_data['recommended_flight_end_date']}\n"
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_json})
    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"msg_{i}")
    else:
        message(msg["content"], is_user=False, key=f"msg_{i}")
