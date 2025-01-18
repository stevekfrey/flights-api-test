import os
import requests
import json
from openai import OpenAI
from pprint import pprint
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# Set up the API key and endpoint
YOUR_API_KEY = os.getenv("PERPLEXITY_API_KEY")
API_ENDPOINT = "https://api.perplexity.ai"


### LOCAL 
current_datetime = datetime.now()

user_location = "San Francisco, CA"
##### 

########################################################
## Data model 
########################################################

class TravelResponse(BaseModel):
    event_name: str = Field(
        description="Name of the event or destination"
    )
    response: str = Field(
        description="Status or clarifying question. Set to 'success' if query is clear, otherwise contains a clarifying question (e.g., 'Did you mean Washington State or Washington, D.C.?')"
    )
    city: str = Field(
        description="Destination city where the event/venue is located"
    )
    airports: List[str] = Field(
        description="List of nearby airports, ordered by distance from the event/venue location"
    )
    event_start_date: Optional[str] = Field(
        description="Start date of the event, sourced from official website or data. Should not be guessed if not available",
        default=None
    )
    event_end_date: Optional[str] = Field(
        description="End date of the event, sourced from official website or data. Should not be guessed if not available",
        default=None
    )
    recommended_flight_start_date: Optional[str] = Field(
        description="Recommended departure date, typically day before event start. Accounts for travel time from user location and typical pre-event activities",
        default=None
    )
    recommended_flight_end_date: Optional[str] = Field(
        description="Recommended return date, typically day after event end. Can be adjusted based on user-specified date ranges",
        default=None
    )
    sources: List[str] = Field(
        description="List of ALL the sources used to verify event details, dates, and location information",
        default_factory=list
    )

    class Config:
        json_schema_extra = {
            "example": {
                "event_name": "Coachella 2024",
                "response": "success",
                "city": "Indio, CA",
                "airports": ["PSP", "LAX", "SAN"],
                "event_start_date": "2024-04-12",
                "event_end_date": "2024-04-21",
                "recommended_flight_start_date": "2024-04-11",
                "recommended_flight_end_date": "2024-04-22",
                "sources": ["coachella.com", "airports.com"]
            }
        }


travel_response_schema = TravelResponse.model_json_schema()
travel_response_schema_str = str(json.dumps(travel_response_schema, indent=2))

print("travel response model schema: \n")
print(travel_response_schema_str)


########################################################
## Prompt 
########################################################

PROMPT_TEMPLATE = """
here is a user's query request to book a flight to a location, airport, city, venue, conference, event, landmark, etc. if they don't already specify the city, please search the internet to find the CITY associated with the (venue, conference, event, landmark, etc) and the AIRPORTS nearby. If there are multiple /events with the same name, if the user didn't specify the date/year of the event and there are different locations, or if it's otherwise unclear, please use "response" to ask for clarification. The current date and time is {current_datetime}. To think about travel times, the user's location is {user_location}.

You  must ONLY respond with valid JSON that follows this schema:
{travel_response_schema_str}

No explanations, no code fences, or ```json fences—just a single JSON object. If unclear, ask for clarification in the "response" field.

Example response:
{{
    "event_name": "Coachella 2024",
    "response": "success",
    "city": "Indio, CA",
    "airports": ["PSP", "LAX", "SAN"],
    "event_start_date": "2024-04-12",
    "event_end_date": "2024-04-21",
    "recommended_flight_start_date": "2024-04-11",
    "recommended_flight_end_date": "2024-04-22",
    "sources": ["coachella.com", "airports.com"]
}}
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
## MAIN QUERY FUNCTION 
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
        model="llama-3.1-sonar-huge-128k-online",
        messages=messages,
    )
    response_content = response.choices[0].message.content
    cleaned_structured_response = extract_json_from_chat_response(response_content)

    print("cleaned_structured_response: \n", cleaned_structured_response)
    
    # validate cleaned model response against TravelResponseschema
    try:
        # Parse JSON string and validate against TravelResponse model
        validated_response = TravelResponse.model_validate_json(cleaned_structured_response)
        return validated_response.model_dump_json()  # Return validated JSON string
    except Exception as e:
        print(f"Validation error: {e}")
        return None


########################################################
## TESTS 
########################################################

if __name__ == "__main__":


    TEST_USER_INPUT = "book a one way trip to Maccu Picchu next week"
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    TEST_USER_INPUT = "book a flight to Coachella this year" 
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    TEST_USER_INPUT = "book a round trip to the next Starship launch "
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    TEST_USER_INPUT = "let's go to the 2025 Super Bowl "
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    TEST_USER_INPUT = "book a flight to the 2025 ICML conference"
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    TEST_USER_INPUT = "book a flight to visit the world's tallest skyscraper for 2 days"
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))

    TEST_USER_INPUT = "book a flight to the soonest possible Taylor Swift concert"
    print (f"\n\nPrompt: {TEST_USER_INPUT}")
    print("Response: \n",get_structured_perplexity_response(PROMPT_TEMPLATE, TEST_USER_INPUT))
