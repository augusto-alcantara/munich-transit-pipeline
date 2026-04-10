import requests
import logging

# Basic logging configuration to display info and error messages with timestamps.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_mvg_connection():
    """
    Day 6 Test: Pulling real-time departures from Munich Hauptbahnhof (Central Station).
    Verified using the 'Network Tab' discovery.
    """
    # Station ID for Munich Hauptbahnhof
    station_id = "de:09162:6"

    # MVG departures API endpoint
    url = "https://www.mvg.de/api/bgw-pt/v3/departures"

    # Parameters for the API request.
    params = {
        "globalId": station_id,
        "limit": 100,
        "transportTypes": "UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS,BAHN"
    }

    logging.info(f"Connecting to MVG API : {url}")

    try:
        # Send request to the MVG API 
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() # This will raise an HTTPError for bad responses (4xx and 5xx)

        logging.info("Successfully connected to MVG's modern V3 API!")

        data = response.json()

        # The V3 API normally returns a list directly or a dictionary with a list inside
        departures = data if isinstance(data, list) else data.get('departures', [])
            
        print(f"\n--- LIVE DEPARTURES (Total found: {len(departures)}) ---")
        for train in departures[:5]:
            line = train.get('label', '??')
            destination = train.get('destination','Unknown')
            t_type = train.get('transportType', 'Unknown')

            print(f"[{t_type}] Line {line} -> {destination}")
        print("-" * 50)


        logging.info("Everything is working perfectly with the latest version of the API!")

    except requests.RequestException as e:
         logging.error(f"Could not connect to MVG API: {e}")

if __name__ == "__main__":
    check_mvg_connection()