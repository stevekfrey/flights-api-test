import express, { Request, Response } from 'express';
import cors from 'cors';
import path from 'path';
import { searchFlights } from './flightService';

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.static(path.join(__dirname, '..', 'public')));

// Endpoint to fetch flight data
app.get('/api/flights', async (req: Request, res: Response) => {
  try {
    const { departure_id, arrival_id, outbound_date, return_date } = req.query;

    const flightParams = {
      departure_id: departure_id || 'SFO',
      arrival_id: arrival_id || 'LAX',
      outbound_date: outbound_date || '2024-12-21',
      return_date: return_date || '2024-12-27',
      currency: 'USD',
      hl: 'en',
      include_airlines: 'UA'
    };

    const flightData = await searchFlights(flightParams);
    res.json(flightData);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch flight data' });
  }
});

// Serve the HTML page
app.get('/', (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
}); 