import requests

def update_dashboard():
    # The URL for the 2026 Driver Standings
    url = "http://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
    response = requests.get(url).json()
    standings = response['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    # Formatting the data into HTML table rows
    html_rows = ""
    for item in standings:
        pos = item['position']
        name = f"{item['Driver']['givenName']} {item['Driver']['familyName']}"
        points = item['points']
        team = item['Constructors'][0]['name']

        # The row
        html_rows += f"<tr><td class='pos'>{pos}</td><td>{name}</td><td>{team}</td><td class='pts'>{points}</td></tr>\n"

    with open("index.html", "r") as f:
        content = f.read()

    update_content = content.replace("", html_rows)

    with open("index.html", "w") as f:
        f.write(update_content)

if __name__ == "__main__":
    update_dashboard()