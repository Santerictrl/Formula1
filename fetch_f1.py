import requests
import json

def get_f1_standings():
    # The URL for the 2026 Driver Standings
    url = "http://api.jolpi.ca/ergast/f1/2026/driverStandings.json"

    try:
        # Asking the API for the data
        response = requests.get(url)
        data = response.json()

        # 3. Drill down into the JSON to find the list of drivers
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        print(f"--- 2026 F1 Driver Standings ---")
        for item in standings:
            pos = item['position']
            name = f"{item['Driver']['givenName']} {item['Driver']['familyName']}"
            points = item['points']
            team = item['Constructors'][0]['name']

            print(f"{pos}. {name} ({team}) - {points} pts")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    get_f1_standings()