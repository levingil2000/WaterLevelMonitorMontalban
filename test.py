import requests
import json

url = "https://pasig-marikina-tullahanffws.pagasa.dost.gov.ph/water/table_list.do"
response = requests.post(url)

if response.status_code == 200:
    data = response.json()
    
    # Print formatted output for inspection
    for station in data:
        print(f"\n--- {station['obsnm']} ---")
        for key, value in station.items():
            if key == "wllist":
                print("  Water Level History:")
                for item in value:
                    print("   ", item)
            else:
                print(f"  {key}: {value}")
else:
    print("Failed to fetch data. Status code:", response.status_code)

