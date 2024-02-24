import requests

# Base URL of the API
BASE_URL = "https://war-service-live.foxholeservices.com/api"

def fetch_map_names():
    url = f"{BASE_URL}/worldconquest/maps"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch map names")
        return []

def fetch_static_map_data(map_name):
    url = f"{BASE_URL}/worldconquest/maps/{map_name}/static"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch static map data for {map_name}")
        return None

def identify_facilities(static_map_data):
    facilities = {
        "Resources": [],
        "Refinery": [],
        "Factories": [],
        "MPFs": [],
        "Seaports": [],
        "Depots": [],
    }
    if static_map_data:
        for item in static_map_data.get("mapItems", []):
            icon_type = item["iconType"]
            coordinates = (item["x"], item["y"])
            # Match iconType to facility type
            if icon_type in [20, 21, 22, 23]:  # Resource fields
                facilities["Resources"].append(coordinates)
            elif icon_type == 17:  # Refinery
                facilities["Refineries"].append(coordinates)
            elif icon_type == 34:  # Factory
                facilities["Factories"].append(coordinates)
            elif icon_type == 51:  # Mass Production Factory
                facilities["MPFs"].append(coordinates)
            elif icon_type == 52:  # Seaport
                facilities["Seaports"].append(coordinates)
            # Note: Depots are not directly listed as an icon type. You may need to adapt based on available types or criteria.
    
    return facilities

def main():
    map_names = fetch_map_names()
    all_facilities = {}
    for map_name in map_names:
        print(f"Processing {map_name}...")
        static_map_data = fetch_static_map_data(map_name)
        facilities = identify_facilities(static_map_data)
        all_facilities[map_name] = facilities
    
    # Here, you can process all_facilities further, such as saving to a file or printing.
    print(all_facilities)

if __name__ == "__main__":
    main()
