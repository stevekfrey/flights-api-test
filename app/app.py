import os
import requests
import json
from openai import OpenAI
from pprint import pprint
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

# Set up the API key and endpoint
YOUR_API_KEY = "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"  # Replace with your actual Perplexity API key
API_ENDPOINT = "https://api.perplexity.ai"


current_datetime = datetime.now()

user_location = "San Francisco, CA"


# Define the prompt
PROMPT_TEMPLATE = """
here is a user's query request to book a flight to a location, airport, city, venue, conference, event, landmark, etc. if they don't already specify the city, please search the internet to find the CITY associated with the (venue, conference, event, landmark, etc) and the AIRPORTS nearby. If there are multiple /events with the same name, if the user didn't specify the date/year of the event and there are different locations, or if it's otherwise unclear, please use "response" to ask for clarification. The current date and time is {current_datetime}. To think about travel times, the user's location is {user_location}.

You  must ONLY respond with valid JSON that follows this schema:
{
"event_name": "string",
"response": "string", # notice ways the user's query could be unclear. if clear, response is "success." if unclear, response is a clarifying question. For example: "there are two places in the US named "Washington", did you mean Washington State (west coast) or Washington, D.C (east coast)?" or "there are two Edge City events in 2025, did you mean the February in San Francisco or the June in Texas?". 
"city": "string", 
"airports": ["string", "string", ...], # in order of distance from the LOCATION of the event or venue 
"event_start_date": "string", #look for the specific START date of the event from its website and online data, don't guess. 
"event_end_date": "string", # look for the specific END date of the event from its website and online data, don't guess. but if the user specifies a date just respond with that date.
"recommended_flight_start_date": "string", #based on how long to travel to the event, so they arrive on the day of the event or the day before. but if the user specifies a date or time range then respond with a reasonable date based on that, leaving long enough to travel from the user's location to the destination, and to do any typical activities at the location. Always give a specific date. 
"recommended_flight_end_date": "string", #based on how long to travel back from the event, so they leave on the day after the event or the day after the event, but if the user specifies a date or time range then respond with a reasonable date based on that. Always give specific dates
"sources": ["string", "string", ...], # list of sources you used to find the event, city, airports, and dates
}

No explanations, no code fences, or ```json fences—just a single JSON object. If unclear, ask for clarification in the "response" field.

Another example: 
---
{
"response": "success" 
"city": "Indio, CA"
"airports": ["PSP", "LAX"],
}
---
"""

########################################################
## HELPERS 
########################################################

def extract_json_from_chat_response(response):
    import re
    assistant_text = response

    # First, try to extract JSON from code blocks
    code_block_pattern = r'```(?:json)?\s*(\{[\s\S]*?\})\s*```'
    code_block_match = re.search(code_block_pattern, assistant_text, flags=re.DOTALL)

    # If no code block, try to find raw JSON
    json_pattern = r'\{[\s\S]*?\}'  # Simplified pattern that still works for nested JSON
    json_match = re.search(json_pattern, assistant_text, flags=re.DOTALL)

    # Use code block JSON if found, otherwise use raw JSON match
    if code_block_match:
        json_string = code_block_match.group(1)
    elif json_match:
        json_string = json_match.group(0)
    else:
        print("No valid JSON found in the response.")
        json_string = None
    return json_string


########################################################
## MAIN FUNCTION 
########################################################

def get_structured_perplexity_response(prompt, user_input):

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {   
            "role": "user",
            "content": (
                user_input
            ),
        },
    ]

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,
    )
    response_content = response.choices[0].message.content
    cleaned_structured_response = extract_json_from_chat_response(response_content)

    return cleaned_structured_response 


########################################################
## TESTS 
########################################################

if __name__ == "__main__":


    TEST_USER_INPUT = "book a one way trip to Maccu Picchu next week"
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))


    # TEST_USER_INPUT = "book a flight to Coachella this year" 
    # print (f"\n\nPrompt: {TEST_USER_INPUT}")
    # print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    # TEST_USER_INPUT = "book a round trip to the next Starship launch "
    # print (f"\n\nPrompt: {TEST_USER_INPUT}")
    # print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    # TEST_USER_INPUT = "let's go to the 2025 Super Bowl "
    # print (f"\n\nPrompt: {TEST_USER_INPUT}")
    # print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    # TEST_USER_INPUT = "book a flight to the 2025 ICML conference"
    # print (f"\n\nPrompt: {TEST_USER_INPUT}")
    # print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    # TEST_USER_INPUT = "book a flight to visit the world's tallest skyscraper for 2 days"
    # print (f"\n\nPrompt: {TEST_USER_INPUT}")
    # print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    # TEST_USER_INPUT = "book a flight to the soonest possible Taylor Swift concert"
    # print (f"\n\nPrompt: {TEST_USER_INPUT}")
    # print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))
