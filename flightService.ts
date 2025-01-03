import axios from 'axios';
import * as dotenv from 'dotenv';

dotenv.config();

const SERPAPI_API_KEY = process.env.SERPAPI_API_KEY;
const SERPAPI_ENDPOINT = 'https://serpapi.com/search.json';

// Search flights with parameters
export async function searchFlights(params: any): Promise<any> {
  const startTime = performance.now();
  
  const {
    departure_id,
    arrival_id,
    outbound_date,
    return_date,
    ...otherParams
  } = params;

  try {
    const response = await axios.get(SERPAPI_ENDPOINT, {
      params: {
        engine: 'google_flights',
        api_key: SERPAPI_API_KEY,
        departure_id,
        arrival_id,
        outbound_date,
        return_date,
        ...otherParams,
      },
    });

    const endTime = performance.now();
    const duration = (endTime - startTime).toFixed(2);
    console.log(`Search completed in ${duration}ms`);

    return response.data;
  } catch (error) {
    const endTime = performance.now();
    const duration = (endTime - startTime).toFixed(2);
    console.error(`Search failed after ${duration}ms:`, error);
    throw error;
  }
}

// Choose a seat on the flight
export function chooseSeat(flightData: any, seatPreference: string): void {
  const flightNumber = flightData?.flights?.[0]?.flight_number || 'Unknown';
  console.log(`Seat preference (${seatPreference}) recorded for flight ${flightNumber}.`);
}

// Add payment information
export function addPayment(paymentInfo: any): void {
  console.log('Payment information added.');
}

// Book the flight
export async function bookFlight(bookingDetails: any): Promise<void> {
  console.log('Flight booked with details:', bookingDetails);
}

// Change/modify the flight
export async function modifyFlight(modificationDetails: any): Promise<void> {
  console.log('Flight modified with details:', modificationDetails);
} 