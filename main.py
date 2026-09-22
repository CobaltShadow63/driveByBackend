"""
DriveBy Backend - Car Routing and Navigation Service
Integrates OpenRouteService for directions, isochrones, and distance matrices.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routing_service import RoutingService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenRouteService
ORS_API_KEY = os.getenv("ORS_API_KEY")
if not ORS_API_KEY:
    raise ValueError("ORS_API_KEY environment variable is required. Copy .env.example to .env and add your API key.")

routing_service = RoutingService(ORS_API_KEY)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "DriveBy Backend"})


@app.route("/api/directions", methods=["POST"])
def get_directions():
    """
    Get directions between waypoints.
    
    Request body:
    {
        "coordinates": [[lon, lat], [lon, lat], ...],
        "profile": "driving-car",  (optional, default: driving-car)
        "instructions": true,  (optional)
        "language": "en"  (optional)
    }
    
    Returns: GeoJSON route with distance, duration, and instructions
    """
    try:
        data = request.get_json()
        
        if not data or "coordinates" not in data:
            return jsonify({"error": "Missing 'coordinates' in request"}), 400
        
        coordinates = data.get("coordinates")
        profile = data.get("profile", "driving-car")
        
        if not isinstance(coordinates, list) or len(coordinates) < 2:
            return jsonify({"error": "Coordinates must be a list with at least 2 points"}), 400
        
        # Build additional params
        params = {}
        if "instructions" in data:
            params["instructions"] = data["instructions"]
        if "language" in data:
            params["language"] = data["language"]
        
        result = routing_service.get_directions(coordinates, profile, **params)
        
        if result is None:
            return jsonify({"error": "Failed to retrieve directions"}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/isochrones", methods=["POST"])
def get_isochrones():
    """
    Get isochrones (reachability areas) from a location.
    
    Request body:
    {
        "locations": [[lon, lat], ...],
        "profile": "driving-car",  (optional)
        "range": [300, 600, 900]  (optional, in seconds)
    }
    
    Returns: GeoJSON polygons representing reachable areas
    """
    try:
        data = request.get_json()
        
        if not data or "locations" not in data:
            return jsonify({"error": "Missing 'locations' in request"}), 400
        
        locations = data.get("locations")
        profile = data.get("profile", "driving-car")
        range_values = data.get("range")
        
        if not isinstance(locations, list) or len(locations) == 0:
            return jsonify({"error": "Locations must be a non-empty list"}), 400
        
        result = routing_service.get_isochrones(locations, profile, range_values)
        
        if result is None:
            return jsonify({"error": "Failed to retrieve isochrones"}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/matrix", methods=["POST"])
def get_distance_matrix():
    """
    Get distance and duration matrix between multiple locations.
    
    Request body:
    {
        "locations": [[lon, lat], [lon, lat], ...],
        "profile": "driving-car"  (optional)
    }
    
    Returns: Distance matrix with durations and distances
    """
    try:
        data = request.get_json()
        
        if not data or "locations" not in data:
            return jsonify({"error": "Missing 'locations' in request"}), 400
        
        locations = data.get("locations")
        profile = data.get("profile", "driving-car")
        
        if not isinstance(locations, list) or len(locations) < 2:
            return jsonify({"error": "Locations must be a list with at least 2 points"}), 400
        
        result = routing_service.get_matrix(locations, profile)
        
        if result is None:
            return jsonify({"error": "Failed to retrieve distance matrix"}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
