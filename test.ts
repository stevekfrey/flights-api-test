import {
  searchFlights,
  chooseSeat,
  addPayment,
  bookFlight,
  modifyFlight,
} from './flightService';

(async () => {
  try {
    const totalStartTime = performance.now();
    
    const flightParams = {
      departure_id: 'SFO',
      arrival_id: 'LAX',
      type: '1', // one-way, put '2' for round-trip and '3' for multi-city
      outbound_date: '2024-12-21',
      return_date: '2024-12-27',
      currency: 'USD',
      hl: 'en',
      include_airlines: 'UA'
    };

    // Search for flights
    const searchResults = await searchFlights(flightParams);

    // Function to print flight details
    function printFlightDetails(flight: any) {
      flight.flights.forEach((leg: any, index: number) => {
        console.log(`Flight Segment ${index + 1}:`);
        console.log(`  Flight Number: ${leg.flight_number}`);
        console.log(`  Airline: ${leg.airline}`);
        console.log(`  Departure: ${leg.departure_airport.name} (${leg.departure_airport.id}) at ${leg.departure_airport.time}`);
        console.log(`  Arrival: ${leg.arrival_airport.name} (${leg.arrival_airport.id}) at ${leg.arrival_airport.time}`);
        console.log(`  Duration: ${leg.duration} minutes`);
        console.log(`  Travel Class: ${leg.travel_class}`);
        console.log(`  Aircraft: ${leg.airplane}`);
        console.log(`  Legroom: ${leg.legroom || 'N/A'}`);
        console.log(`  Extensions: ${leg.extensions?.join(', ') || 'None'}`);
        console.log();
      });
      if (flight.layovers && flight.layovers.length > 0) {
        console.log('Layovers:');
        flight.layovers.forEach((layover: any, index: number) => {
          console.log(`  Layover ${index + 1}:`);
          console.log(`    Location: ${layover.name} (${layover.id})`);
          console.log(`    Duration: ${layover.duration} minutes`);
          console.log(`    Overnight: ${layover.overnight ? 'Yes' : 'No'}`);
          console.log();
        });
      }
      console.log(`Total Trip Duration: ${flight.total_duration} minutes`);
      console.log(`Price: $${flight.price}`);
      console.log(`Type: ${flight.type}`);
      console.log(`Airline Logo URL: ${flight.airline_logo}`);
      console.log('----------------------------------------\n');
    }

    // Print all best flights
    if (searchResults.best_flights && searchResults.best_flights.length > 0) {
      console.log('=== Best Flights ===\n');
      searchResults.best_flights.forEach((flight: any, index: number) => {
        console.log(`Flight Option ${index + 1}:`);
        printFlightDetails(flight);
      });
    }

    // Print all other flights
    if (searchResults.other_flights && searchResults.other_flights.length > 0) {
      console.log('=== Other Flights ===\n');
      searchResults.other_flights.forEach((flight: any, index: number) => {
        console.log(`Flight Option ${index + 1}:`);
        printFlightDetails(flight);
      });
    }

    // Select a specific flight from the results (e.g., the first one)
    const selectedFlight = searchResults?.best_flights?.[0] || searchResults?.other_flights?.[0];

    // Choose a seat (placeholder)
    chooseSeat(selectedFlight, 'Aisle');

    // Add payment information (placeholder)
    addPayment({
      cardNumber: '4111111111111111',
      expiryDate: '12/24',
      cvv: '123',
    });

    // Book the flight (placeholder)
    await bookFlight({
      flightId: selectedFlight?.flights?.[0]?.flight_number || 'flight123',
      passengerInfo: { name: 'John Doe', passport: '123456789' },
    });

    // Modify the flight (placeholder)
    await modifyFlight({
      bookingId: 'booking123',
      newDate: '2024-12-28',
    });

    const totalEndTime = performance.now();
    const totalDuration = (totalEndTime - totalStartTime).toFixed(2);
    console.log(`\nTotal execution time: ${totalDuration}ms`);
  } catch (error) {
    console.error('An error occurred:', error);
  }
})(); 