import os, requests

# Your API key for the Google Maps Platform
API_KEY = os.environ['GOOGLE_ROUTER_API_KEY']

# API endpoint for computeRoutes
url = "https://routes.googleapis.com/directions/v2:computeRoutes"
default_address = "64 Mavety St, Toronto, ON"

def directions_from_latlongs(latlongs):
    
    # Request headers including API key and fields to return
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline,routes.legs,routes.travelAdvisory.tollInfo"
    }

    origin_lat = latlongs[0][0]
    origin_lng = latlongs[0][1]
    destination_lat = latlongs[-1][0]
    destination_lng = latlongs[-1][1]
    latlongs.pop(0)
    latlongs.pop(-1)

    # "intermediates": [       
    #     { "location": { "latLng": { "latitude": 50.7749, "longitude": -122.4194 } } }   # { "address": "Waypoint 1" },
    # ],

    # Request body with origin, destination and other parameters
    body = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": origin_lat,
                    "longitude": origin_lng
                },
                "address": "64 Mavety Ave, Toronto, ON"            
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": destination_lat,
                    "longitude": destination_lng
                }
            }
        },
        "intermediates": [       
            { "location": { "latLng": { "latitude": x, "longitude": y } } } 
            for x, y in latlongs
        ],
        "travelMode": "BICYCLE",
        "polylineQuality": "OVERVIEW",
        # "routingPreference": "TRAFFIC_AWARE",
        "departureTime": "2025-10-23T15:00:00Z"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=body)

    # Check for successful response
    if response.status_code == 200:
        print("Route optimization successful:")
        return response.json()
    else:
        print(f"Error in request: {response.status_code}")
        return response.text

def directions_from_addresses(nads):
    
    # Request headers including API key and fields to return
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline,routes.legs,routes.travelAdvisory.tollInfo"
    }

    origin_address = nads[0][1] if nads else default_address
    destination_address = nads[-1][1] if nads else default_address

    # if nads: nads.pop(0)
    # nads.pop(-1)

    # Request body with origin, destination and other parameters
    body = {
        "origin": {
            # "address": origin_address
            "address": nads[0][1]
        },
        "destination": {
            # "address": destination_address
            "address": nads[-1][1]
        },
        "intermediates": [
            { "address": nad[1] } for nad in nads[1:-1]
        ],
        "travelMode": "BICYCLE",
        "polylineQuality": "OVERVIEW",
        # "routingPreference": "TRAFFIC_AWARE",
        "departureTime": "2025-10-23T15:00:00Z"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=body)

    # Check for successful response
    if response.status_code == 200:
        print("Route optimization successful:")

        data = response.json()

        print(f"Legs: {len(data['routes'][0]['legs'])} Nads: {len(nads)}")

        for leg, nad in zip( data['routes'][0]['legs'], nads ): 
            # print(f"Leg from {leg.startLocation.address} to {leg.endLocation.address}, distance: {leg.distanceMeters} meters, duration: {leg.duration} seconds")
            leg['endLocation']['nad'] = nad
        
        return data
    else:
        print(f"Error in request: {response.status_code}")
        return response.text
