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

    response = requests.get(url, params=params, timeout=10)

    if response.status_code !=200:
        return []
    
    data = response.json()

    departures = data if isinstance (data, list) else data.get("departures", [])

    logging.info(f"Fetched {len(departures)} records")

    return departures

if __name__ == "__main__":
    data = fetch_mvg_data()

    for item in data[:2]:
        print(item)
    
    all_keys = set()

    for item in data:
        all_keys.update(item.keys())

    print(all_keys)