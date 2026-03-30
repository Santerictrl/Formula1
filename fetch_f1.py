import requests

def update_dashboard():
    # 1. Get the data from the API
    url = "http://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
    data = requests.get(url).json()
    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    # 2. Build the rows
    html_rows = ""
    for item in standings:
        pos = item['position']
        name = f"{item['Driver']['givenName']} {item['Driver']['familyName']}"
        team = item['Constructors'][0]['name']
        points = item['points']
        html_rows += f"<tr><td>{pos}</td><td>{name}</td><td>{team}</td><td>{points}</td></tr>\n"

    # 3. READ THE ENTIRE TEMPLATE FILE
    # This keeps your CSS and HTML structure safe!
    with open("template.html", "r") as f:
        full_page_template = f.read()

    # 4. REPLACE THE PLACEHOLDER WITH THE ROWS
    final_combined_html = full_page_template.replace("", html_rows)

    # 5. SAVE THE WHOLE THING TO INDEX.HTML
    with open("index.html", "w") as f:
        f.write(final_combined_html)
    
    print("Dashboard rebuilt successfully!")

if __name__ == "__main__":
    update_dashboard()