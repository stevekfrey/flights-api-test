"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const flightService_1 = require("./flightService");
(() => __awaiter(void 0, void 0, void 0, function* () {
    var _a, _b, _c, _d;
    try {
        const flightParams = {
            departure_id: 'PEK',
            arrival_id: 'AUS',
            outbound_date: '2024-12-21',
            return_date: '2024-12-27',
            currency: 'USD',
            hl: 'en',
        };
        // Search for flights
        const searchResults = yield (0, flightService_1.searchFlights)(flightParams);
        // Function to print flight details
        function printFlightDetails(flight) {
            flight.flights.forEach((leg, index) => {
                var _a;
                console.log(`Flight Segment ${index + 1}:`);
                console.log(`  Flight Number: ${leg.flight_number}`);
                console.log(`  Airline: ${leg.airline}`);
                console.log(`  Departure: ${leg.departure_airport.name} (${leg.departure_airport.id}) at ${leg.departure_airport.time}`);
                console.log(`  Arrival: ${leg.arrival_airport.name} (${leg.arrival_airport.id}) at ${leg.arrival_airport.time}`);
                console.log(`  Duration: ${leg.duration} minutes`);
                console.log(`  Travel Class: ${leg.travel_class}`);
                console.log(`  Aircraft: ${leg.airplane}`);
                console.log(`  Legroom: ${leg.legroom || 'N/A'}`);
                console.log(`  Extensions: ${((_a = leg.extensions) === null || _a === void 0 ? void 0 : _a.join(', ')) || 'None'}`);
                console.log();
            });
            if (flight.layovers && flight.layovers.length > 0) {
                console.log('Layovers:');
                flight.layovers.forEach((layover, index) => {
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
            searchResults.best_flights.forEach((flight, index) => {
                console.log(`Flight Option ${index + 1}:`);
                printFlightDetails(flight);
            });
        }
        // Print all other flights
        if (searchResults.other_flights && searchResults.other_flights.length > 0) {
            console.log('=== Other Flights ===\n');
            searchResults.other_flights.forEach((flight, index) => {
                console.log(`Flight Option ${index + 1}:`);
                printFlightDetails(flight);
            });
        }
        // Select a specific flight from the results (e.g., the first one)
        const selectedFlight = ((_a = searchResults === null || searchResults === void 0 ? void 0 : searchResults.best_flights) === null || _a === void 0 ? void 0 : _a[0]) || ((_b = searchResults === null || searchResults === void 0 ? void 0 : searchResults.other_flights) === null || _b === void 0 ? void 0 : _b[0]);
        // Choose a seat (placeholder)
        (0, flightService_1.chooseSeat)(selectedFlight, 'Aisle');
        // Add payment information (placeholder)
        (0, flightService_1.addPayment)({
            cardNumber: '4111111111111111',
            expiryDate: '12/24',
            cvv: '123',
        });
        // Book the flight (placeholder)
        yield (0, flightService_1.bookFlight)({
            flightId: ((_d = (_c = selectedFlight === null || selectedFlight === void 0 ? void 0 : selectedFlight.flights) === null || _c === void 0 ? void 0 : _c[0]) === null || _d === void 0 ? void 0 : _d.flight_number) || 'flight123',
            passengerInfo: { name: 'John Doe', passport: '123456789' },
        });
        // Modify the flight (placeholder)
        yield (0, flightService_1.modifyFlight)({
            bookingId: 'booking123',
            newDate: '2024-12-28',
        });
    }
    catch (error) {
        console.error('An error occurred:', error);
    }
}))();
