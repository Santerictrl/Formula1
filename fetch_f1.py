import requests

def update_dashboard():
    print("1. Connecting to F1 API...")
    url = "http://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        print(f"2. Found {len(standings)} drivers.")

        html_rows = ""
        for item in standings:
            pos = item['position']
            name = f"{item['Driver']['givenName']} {item['Driver']['familyName']}"
            team = item['Constructors'][0]['name']
            pts = item['points']
            html_rows += f"<tr><td>{pos}</td><td>{name}</td><td>{team}</td><td>{pts}</td></tr>\n"

        print("3. Reading template.html...")
        with open("template.html", "r") as f:
            template_content = f.read()

        # This is the critical part!
        if "" in template_content:
            print("4. Placeholder found! Replacing data...")
            # We replace the placeholder AND the "If you see this" row
            final_html = template_content.replace("", html_rows)
            # This part removes that 'warning' row we added in the template
            final_html = final_html.replace('<tr><td colspan="4">If you see this, Python hasn\'t replaced the data yet!</td></tr>', "")
        else:
            print("ERROR: Could not find '' in template.html")
            return

        print("5. Saving to index.html...")
        with open("index.html", "w") as f:
            f.write(final_html)
        print("DONE! Check your index.html now.")

    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    update_dashboard()