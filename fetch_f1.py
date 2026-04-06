import requests
from datetime import datetime

def update_dashboard():
    # 1. Get Standings
    standings_url = "http://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
    standings_data = requests.get(standings_url).json()
    standings = standings_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    
    html_rows = ""
    for item in standings:
        pos = item['position']
        name = f"{item['Driver']['givenName']} {item['Driver']['familyName']}"
        team = item['Constructors'][0]['name']
        pts = item['points']
        html_rows += f"<tr><td>{pos}</td><td>{name}</td><td>{team}</td><td>{pts}</td></tr>\n"

    # 2. Get Schedule & Find Next Race
    schedule_url = "http://api.jolpi.ca/ergast/f1/2026.json"
    schedule_data = requests.get(schedule_url).json()
    races = schedule_data['MRData']['RaceTable']['Races']
    
    next_race = None
    today = datetime.now()
    for race in races:
        # We use [0:10] just in case the API date format has extra characters
        race_date = datetime.strptime(race['date'][0:10], '%Y-%m-%d')
        if race_date > today:
            next_race = race
            break

    # 3. Read Template and Replace Everything
    with open("template.html", "r") as f:
        content = f.read()

    # We update the 'content' variable step by step
    content = content.replace("", html_rows)
    
    # EVERYTHING below must be indented so it stays inside update_dashboard()
    if next_race:
        content = content.replace("", next_race['raceName'])
        content = content.replace("", next_race['date'])
            
        # Provide the ISO date for the JavaScript countdown
        iso_date = f"{next_race['date']}T{next_race.get('time', '15:00:00Z')}"
        content = content.replace("", iso_date)
            
        # Track Image logic
        city_image = next_race['Circuit']['Location']['locality'].lower() + ".jpg"
        content = content.replace("", city_image)

    # 4. Save to index.html (Make sure we save 'content', not 'final_html')
    with open("index.html", "w") as f:
        f.write(content)
    
    print("Dashboard fully updated with Next Race info!")

if __name__ == "__main__":
    update_dashboard()