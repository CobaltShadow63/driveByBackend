"""
OpenRouteService wrapper for routing and directions API calls.
Handles communication with OpenRouteService API.
"""

import openrouteservice
from openrouteservice.client import Client
from typing import Optional, List, Dict, Any


class RoutingService:
    """Service to interact with OpenRouteService for routing operations."""
    
    def __init__(self, api_key: str):
        """
        Initialize the routing service with OpenRouteService API key.
        
        Args:
            api_key: OpenRouteService API key
        """
        self.client = Client(key=api_key)
    
    def get_directions(
        self, 
        coordinates: List[List[float]], 
        profile: str = "driving-car",
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Get route directions between coordinates.
        
        Args:
            coordinates: List of [lon, lat] coordinate pairs (min 2 points)
            profile: Routing profile (driving-car, driving-hgv, cycling-regular, foot-walking)
            **kwargs: Additional parameters (format, language, instructions, etc)
            
        Returns:
            Route data with geometry and instructions, or None on error
        """
        try:
            if len(coordinates) < 2:
                raise ValueError("At least 2 coordinate pairs required")
            
            params = {
                "coordinates": coordinates,
                **kwargs
            }
            
            # Call the appropriate profile method
            if profile == "driving-car":
                return self.client.directions(profile="driving-car", **params)
            elif profile == "cycling-regular":
                return self.client.directions(profile="cycling-regular", **params)
            elif profile == "foot-walking":
                return self.client.directions(profile="foot-walking", **params)
            else:
                return self.client.directions(profile=profile, **params)
                
        except Exception as e:
            print(f"Error getting directions: {e}")
            return None
    
    def get_isochrones(
        self,
        locations: List[List[float]],
        profile: str = "driving-car",
        range_values: Optional[List[int]] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Get isochrones (reachability areas) from given locations.
        
        Args:
            locations: List of [lon, lat] coordinate pairs
            profile: Routing profile
            range_values: List of range values in seconds (e.g., [300, 600, 900])
            **kwargs: Additional parameters
            
        Returns:
            Isochrone GeoJSON data or None on error
        """
        try:
            if range_values is None:
                range_values = [300, 600, 900]  # 5, 10, 15 minutes
            
            params = {
                "locations": locations,
                "range": range_values,
                **kwargs
            }
            
            return self.client.isochrones(profile=profile, **params)
            
        except Exception as e:
            print(f"Error getting isochrones: {e}")
            return None
    
    def get_matrix(
        self,
        locations: List[List[float]],
        profile: str = "driving-car",
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Get distance and duration matrix between multiple locations.
        
        Args:
            locations: List of [lon, lat] coordinate pairs
            profile: Routing profile
            **kwargs: Additional parameters
            
        Returns:
            Matrix data with distances and durations or None on error
        """
        try:
            if len(locations) < 2:
                raise ValueError("At least 2 locations required for matrix")
            
            params = {
                "locations": locations,
                **kwargs
            }
            
            return self.client.distance_matrix(profile=profile, **params)
            
        except Exception as e:
            print(f"Error getting distance matrix: {e}")
            return None
