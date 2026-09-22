# DriveBy Backend

A public app to be used by car enthusiasts. This backend provides routing, directions, and isochrone services powered by [OpenRouteService](https://openrouteservice.org/).

## Features

- **Directions API**: Get optimal routes between multiple waypoints
- **Isochrones API**: Calculate reachable areas from a location within specific time ranges
- **Distance Matrix API**: Get travel time and distance between multiple locations
- **CORS enabled**: Ready for cross-origin requests from the frontend

## Setup

### Prerequisites

- Python 3.8+
- Virtual environment (`.venv` already created)
- OpenRouteService API key (free tier available at https://openrouteservice.org/)

### Installation

1. **Activate the virtual environment**:
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
   - Command Prompt: `.\.venv\Scripts\activate.bat`
   - Bash/WSL: `source .venv/bin/activate`

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example file
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   
   # Edit .env and add your OpenRouteService API key
   # ORS_API_KEY=your_actual_api_key_here
   ```

4. **Get your API key**:
   - Visit https://openrouteservice.org/dev/#/signup
   - Sign up for free
   - Copy your API key to `.env`

## Running the Server

With venv activated:

```bash
python main.py
```

Server runs on `http://localhost:5000` by default.

## API Endpoints

### Health Check
```
GET /health
```
Returns service status.

### Directions
```
POST /api/directions
Content-Type: application/json

{
  "coordinates": [[8.681495, 49.41461], [8.687872, 49.420318]],
  "profile": "driving-car",
  "instructions": true,
  "language": "en"
}
```

Supported profiles:
- `driving-car` (default)
- `cycling-regular`
- `foot-walking`

### Isochrones
```
POST /api/isochrones
Content-Type: application/json

{
  "locations": [[8.681495, 49.41461]],
  "profile": "driving-car",
  "range": [300, 600, 900]
}
```

Returns GeoJSON polygons for reachable areas (range in seconds).

### Distance Matrix
```
POST /api/matrix
Content-Type: application/json

{
  "locations": [[8.681495, 49.41461], [8.687872, 49.420318]],
  "profile": "driving-car"
}
```

Returns distance and duration matrix.

## Project Structure

```
driveByBackend/
├── main.py              # Flask app and route handlers
├── routing_service.py   # OpenRouteService wrapper
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin request handling
- **openrouteservice**: Official ORS Python client
- **python-dotenv**: Environment variable management

## Next Steps

- Frontend integration: Use the API endpoints from the React Native frontend
- Error handling: Implement retry logic for API calls
- Caching: Consider caching frequent routes
- Rate limiting: Implement rate limits for production use
