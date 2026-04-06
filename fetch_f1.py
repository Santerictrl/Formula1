import requests
from datetime import datetime

def update_dashboard():
    # 1. Get Standings
    standings_url = "http://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
    standings_data = requests.get(standings_url).json()
    standings = standings_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    
    html_rows = ""
    for item in standings:
        html_rows += f"<tr><td>{item['position']}</td><td>{item['Driver']['givenName']} {item['Driver']['familyName']}</td><td>{item['Constructors'][0]['name']}</td><td>{item['points']}</td></tr>\n"

    # 2. Get Schedule & Find Next Race
    schedule_url = "http://api.jolpi.ca/ergast/f1/2026.json"
    schedule_data = requests.get(schedule_url).json()
    races = schedule_data['MRData']['RaceTable']['Races']
    
    next_race = None
    today = datetime.now()
    for race in races:
        race_date = datetime.strptime(race['date'], '%Y-%m-%d')
        if race_date > today:
            next_race = race
            break

    # 3. Read Template and Replace Everything
    with open("template.html", "r") as f:
        content = f.read()

    content = content.replace("", html_rows)
    
if next_race:
        content = content.replace("", next_race['raceName'])
        content = content.replace("", next_race['date'])
        
        # New: Provide the ISO date for the JavaScript countdown
        # API dates are 'YYYY-MM-DD', but we need to add the time
        iso_date = f"{next_race['date']}T{next_race.get('time', '15:00:00Z')}"
        content = content.replace("", iso_date)
        
        # Track Image
        city_image = next_race['Circuit']['Location']['locality'].lower() + ".jpg"
        content = content.replace("", city_image)

    # 4. Save to index.html
    with open("index.html", "w") as f:
        f.write(final_html)
    print("Dashboard fully updated with Next Race info!")

if __name__ == "__main__":
    update_dashboard()