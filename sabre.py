import requests
import json
from datetime import datetime
import time
import base64


class SabreAPIClient:
    def __init__(self, client_id, client_secret, environment='test'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        # self.base_url = 'https://api.test.sabre.com' if environment == 'test' else 'https://api.sabre.com'
        self.base_url = 'https://api.havail.sabre.com'

        self.token = None
        self.token_expiry = 0  # Timestamp for when the token expires

    def get_access_token(self):
        try:
            url = f"{self.base_url}/v2/auth/token"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.token = token_data['access_token']
            self.token_expiry = time.time() + token_data['expires_in']
            return self.token
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")
            return None

    def _encode_credentials(self):
        # Create a base64 encoded string for client_id:client_secret
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def is_token_valid(self):
        # Check if the current token is still valid
        return self.token and time.time() < self.token_expiry

    def ensure_token(self):
        # Ensure that we have a valid access token
        if not self.is_token_valid():
            print("Access token is invalid or expired. Obtaining a new one...")
            self.get_access_token()

            

            

    def search_flights(self, origin, destination, departure_date, return_date=None, adults=1, children=0, infants=0):
        self.ensure_token()  # Ensure we have a valid token before making API calls
        
        url = f"{self.base_url}/v2/shop/flights"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'OTA_AirLowFareSearchRQ': {
                'OriginDestinationInformation': [
                    {
                        'DepartureDateTime': departure_date,
                        'OriginLocation': {'LocationCode': origin},
                        'DestinationLocation': {'LocationCode': destination}
                    }
                ],
                'TravelerInfoSummary': {
                    'AirTravelerAvail': [
                        {
                            'PassengerTypeQuantity': [
                                {'Code': 'ADT', 'Quantity': adults},
                                {'Code': 'CNN', 'Quantity': children},
                                {'Code': 'INF', 'Quantity': infants}
                            ]
                        }
                    ]
                }
            }
        }
        
        if return_date:
            payload['OTA_AirLowFareSearchRQ']['OriginDestinationInformation'].append({
                'DepartureDateTime': return_date,
                'OriginLocation': {'LocationCode': destination},
                'DestinationLocation': {'LocationCode': origin}
            })
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching flights: {e}")
            return None



    def select_flight(self, itinerary_id):
        url = f"{self.base_url}/v1/shop/flights/revalidate"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'OTA_AirLowFareSearchRQ': {
                'POS': {'Source': [{'PseudoCityCode': 'F9CE'}]},
                'IntelliSellTransaction': {
                    'RequestType': {'Name': 'REVALIDATE'},
                    'CompressResponse': {'Value': 'true'}
                },
                'TPA_Extensions': {'IntelliSellTransaction': {'ReservationData': {'ItineraryRef': itinerary_id}}}
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def select_seat(self, pnr, flight_segment, seat_number):
        url = f"{self.base_url}/v1/offers/shop"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'OTA_AirSeatMapRQ': {
                'SeatMapQueryEnhanced': {
                    'RequestType': 'Booking',
                    'FlightSegment': flight_segment,
                    'RequestedSeatNumber': seat_number
                }
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def book_flight(self, pnr, passenger_details):
        url = f"{self.base_url}/v1/passenger/records"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'CreatePassengerNameRecordRQ': {
                'version': '2.3.0',
                'TravelItineraryAddInfo': {
                    'AgencyInfo': {
                        'Address': {
                            'AddressLine': '123 Main St',
                            'CityName': 'Boulder',
                            'CountryCode': 'US',
                            'PostalCode': '80301',
                            'StateCountyProv': {'StateCode': 'CO'}
                        }
                    },
                    'CustomerInfo': {
                        'ContactNumbers': {
                            'ContactNumber': [
                                {'Phone': '1234567890', 'PhoneUseType': 'H'}
                            ]
                        },
                        'PersonName': [passenger_details]
                    }
                }
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def process_payment(self, pnr, payment_info):
        url = f"{self.base_url}/v1/payment/cc"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'PaymentRQ': {
                'CC_Info': payment_info,
                'PNR': pnr
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def update_flight(self, pnr, update_info):
        url = f"{self.base_url}/v1/passenger/records/{pnr}"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'UpdatePassengerNameRecordRQ': update_info
        }
        response = requests.put(url, headers=headers, json=payload)
        return response.json()

    def cancel_flight(self, pnr):
        url = f"{self.base_url}/v1/passenger/records/{pnr}"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers)
        return response.json()

# Example usage
if __name__ == "__main__":
    print ("starting SABRE client ")
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    client_id = os.getenv('SABRE_API_USER')
    client_secret = os.getenv('SABRE_API_KEY')
    client = SabreAPIClient(client_id, client_secret)
    print ("initialized SABRE client ")

    print (client_id, client_secret)

    # Search for flights
    flights = client.search_flights('SFO', 'LAX', '2025-01-02')
    if flights and 'OTA_AirLowFareSearchRS' in flights:
        print("Available flights:", json.dumps(flights, indent=2))
    else:
        print("Failed to retrieve flight information")

    # Select a flight (assuming we have an itinerary_id from the search results)
    selected_flight = client.select_flight('itinerary_id_from_search_results')
    print("Selected flight:", json.dumps(selected_flight, indent=2))

    if 'OTA_AirLowFareSearchRS' in selected_flight:
        pnr = selected_flight['OTA_AirLowFareSearchRS']['TPA_Extensions']['PNR']
    else:
        print("Failed to select flight due to invalid response.")

    # Extract flight details
    flight_number = selected_flight['OTA_AirLowFareSearchRS']['OriginDestinationInformation'][0]['FlightSegment'][0]['FlightNumber']
    departure_date = selected_flight['OTA_AirLowFareSearchRS']['OriginDestinationInformation'][0]['FlightSegment'][0]['DepartureDateTime']
    flight_segment = {'FlightNumber': flight_number, 'DepartureDateTime': departure_date}

    # Get available seats
    available_seats = client.get_available_seats(pnr, flight_segment)

    # Select the first available seat
    if available_seats:
        selected_seat = available_seats[0]['SeatNumber']
        seat_selection = client.select_seat(pnr, flight_segment, selected_seat)
        print(f"Selected seat: {selected_seat}")
        print("Seat selection:", json.dumps(seat_selection, indent=2))
    else:
        print("No available seats found.")


    # Select a seat (assuming we have flight segment details and a seat number)
    seat_selection = client.select_seat('PNR123', flight_segment, '12A')
    print("Seat selection:", json.dumps(seat_selection, indent=2))

    # Book the flight
    passenger_details = {
        'GivenName': 'John',
        'Surname': 'Doe',
        'DateOfBirth': '1990-01-01',
        'Gender': 'M',
        'NameReference': '1.1'
    }
    booking = client.book_flight('PNR123', passenger_details)
    print("Booking details:", json.dumps(booking, indent=2))

    # Process payment
    payment_info = {
        'PaymentCard': {
            'CardCode': 'VI',
            'CardNumber': '4111111111111111',
            'ExpiryDate': '2025-12'
        },
        'CardHolderInfo': {
            'CardHolderName': 'John Doe',
            'BillingAddress': {
                'AddressLine1': '123 Main St',
                'CityName': 'Boulder',
                'PostalCode': '80301',
                'StateCode': 'CO',
                'CountryCode': 'US'
            }
        }
    }
    payment = client.process_payment('PNR123', payment_info)
    print("Payment processed:", json.dumps(payment, indent=2))

    # Update flight (e.g., change seat)
    update_info = {
        'AirBook': {
            'SegmentNumber': '1',
            'ActionCode': 'HK',
            'SeatNumber': '14B'
        }
    }
    updated_flight = client.update_flight('PNR123', update_info)
    print("Updated flight:", json.dumps(updated_flight, indent=2))

    # Cancel flight
    cancellation = client.cancel_flight('PNR123')
    print("Cancellation result:", json.dumps(cancellation, indent=2))
