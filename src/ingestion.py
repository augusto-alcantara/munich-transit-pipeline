import requests
import logging 

logging.basicConfig(level=logging.INFO)


def fetch_mvg_data():
    url = "https://www.mvg.de/api/bgw-pt/v3/departures"
    
    params = {
        "globalId": "de:09162:6",
        "limit": 5,
        "transportTypes": "UBAHN,TRAM,SBAHN,BUS"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code !=200:
            logging.error(
                "[INGESTION][RETRYABLE] API returned status_code: %s", 
                response.status_code
            )
            return None
        
        data = response.json()

        departures = data if isinstance (data, list) else data.get("departures", [])

        logging.info("Fetched %d departures from MVG API", len(departures))

        return departures

    except requests.RequestException as e:
        logging.error("[INGESTION][RETRYABLE] API request failed: %s", e)
        return None

if __name__ == "__main__":
    data = fetch_mvg_data()

    print("\n--- SAMPLE RECORDS ---")
    for item in data[:3]:  # Print first 3 records
        print(item)
        print("-" * 80)
    
    all_keys = set()

    for item in data:
        all_keys.update(item.keys())

    print("\n--- ALL KEYS FOUND ---")
    for key in sorted(all_keys):
        print(key)

        
          