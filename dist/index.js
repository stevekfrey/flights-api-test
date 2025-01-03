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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const path_1 = __importDefault(require("path"));
const flightService_1 = require("./flightService");
const app = (0, express_1.default)();
const port = process.env.PORT || 3000;
app.use((0, cors_1.default)());
app.use(express_1.default.static(path_1.default.join(__dirname, '..', 'public')));
// Endpoint to fetch flight data
app.get('/api/flights', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const { departure_id, arrival_id, outbound_date, return_date } = req.query;
        const flightParams = {
            departure_id: departure_id || 'PEK',
            arrival_id: arrival_id || 'AUS',
            outbound_date: outbound_date || '2024-12-21',
            return_date: return_date || '2024-12-27',
            currency: 'USD',
            hl: 'en',
        };
        const flightData = yield (0, flightService_1.searchFlights)(flightParams);
        res.json(flightData);
    }
    catch (error) {
        res.status(500).json({ error: 'Failed to fetch flight data' });
    }
}));
// Serve the HTML page
app.get('/', (req, res) => {
    res.sendFile(path_1.default.join(__dirname, '..', 'public', 'index.html'));
});
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
