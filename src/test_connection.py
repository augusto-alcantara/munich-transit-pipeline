import requests
import json
import logging

# Set up simple logging to see what's happening
logging.basicConfig(
    level=logging.INFO
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_mvg_connections():
    """
    Day 6 Test: Pulling real-time departures from Munich Hauptbanhof (Central Station).
    Verified using the 'Network Tab' discovery.
    """
    # The found ID in the Network Tab of (Hauptbahnhof):
    station_id = "de:09162:6"

    # We use the exact V3 endpoint that we found on the browser
    url = https://www.mvg.de/api/bgw-pt/v3/departures

    # This are the (parameters) that were discovered in the URL.
    params = {
        "globalId" : station_id
        "limit" : 100
        "transportTypes" : "UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS,BAHN"
    }

    logging.info(f"Connecting to the Transit's Munich API V3 : {url}")

    try:
        # requests.get combine the URL and parameters automatically
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            logging.info("SUCESS:¡Connected to MVG's modern V3 API!")

            data response.json()

            # The V3 API normally returns a list directly or a dictionary with a list inside
            departures = data if isinstance(data, list) else data.get('departures', [])
            
            print(f"\n--- LIVE OUTINGS (Total found: {len(departures)}) ---")
            for train in departures[:5]:
                line = train.get('label', '??')
                destination = train.get('destination','Unknown')
                t_type = train.get('transportType', 'Unknown')

                print(f"[t_type] Line {line} To: {destination}")
                separator = "-" * 50
            print(separator)

            logging.info("Everything is working perfectly with the latest version of the API!")

        else:
                logging.error(f"❌ ERROR: Status Code {response.status_code}")

    except Exception as e:
         logging.error(f"❌ ERROR: Could not connect. Details: {e}")

if __name__ == "__main__":
    test_mvg_connetion()