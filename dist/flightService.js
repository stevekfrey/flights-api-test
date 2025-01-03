"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.searchFlights = searchFlights;
exports.chooseSeat = chooseSeat;
exports.addPayment = addPayment;
exports.bookFlight = bookFlight;
exports.modifyFlight = modifyFlight;
const axios_1 = __importDefault(require("axios"));
const dotenv = __importStar(require("dotenv"));
dotenv.config();
const SERPAPI_API_KEY = process.env.SERPAPI_API_KEY;
const SERPAPI_ENDPOINT = 'https://serpapi.com/search.json';
// Search flights with parameters
function searchFlights(params) {
    return __awaiter(this, void 0, void 0, function* () {
        const { departure_id, arrival_id, outbound_date, return_date } = params, otherParams = __rest(params, ["departure_id", "arrival_id", "outbound_date", "return_date"]);
        try {
            const response = yield axios_1.default.get(SERPAPI_ENDPOINT, {
                params: Object.assign({ engine: 'google_flights', api_key: SERPAPI_API_KEY, departure_id,
                    arrival_id,
                    outbound_date,
                    return_date }, otherParams),
            });
            return response.data;
        }
        catch (error) {
            console.error('Error searching flights:', error);
            throw error;
        }
    });
}
// Choose a seat on the flight
function chooseSeat(flightData, seatPreference) {
    var _a, _b;
    const flightNumber = ((_b = (_a = flightData === null || flightData === void 0 ? void 0 : flightData.flights) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.flight_number) || 'Unknown';
    console.log(`Seat preference (${seatPreference}) recorded for flight ${flightNumber}.`);
}
// Add payment information
function addPayment(paymentInfo) {
    console.log('Payment information added.');
}
// Book the flight
function bookFlight(bookingDetails) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log('Flight booked with details:', bookingDetails);
    });
}
// Change/modify the flight
function modifyFlight(modificationDetails) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log('Flight modified with details:', modificationDetails);
    });
}
