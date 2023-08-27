from flask import Flask, render_template, request
import json
import requests
import urllib.parse
from event_api import fetch_html, get_events
from utils import uule


app = Flask(__name__)

# Main site
@app.route('/', methods=['GET'])
def index():
    try:
        query = request.args.get('query')
        offset = request.args.get('offset')
        location = request.args.get('location')
        dates = request.args.get('dates')

        if query is None:
            return render_template("index.html")
        elif len(query) == 0:
            query = "events"

        if len(location) > 0:
            query = location + " " + query

        user_ip = request.remote_addr
        location_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={ipgeolocation_API_KEY}&ip={user_ip}"

        response = requests.get(location_url)
        if response.status_code == 200:
            location_data = response.json()
        else:
            location_data = {}

        try:
            uule_string = f"uule={uule(','.join([location_data['city'], location_data['state_prov'], location_data['country_name']]))}"
        except:
            uule_string = "uule="

        hl_string = "hl=en"
        offset_string = f"start={offset}"

        date_map = {
            "Today": "date:today",
            "Tomorrow": "date:tomorrow",
            "This Week": "date:week",
            "This Weekend": "date:weekend",
            "Next Week": "date:next_week",
            "This Month": "date:month",
            "Next Month": "date:next_month"
        }

        params = [uule_string, hl_string]
        if offset:
            params.append(offset_string)
        if dates:
            date_list = dates.split(",")
            chip_list = []
            for date in date_list:
                if date in date_map:
                    chip_list.append(date_map[date])
            if len(chip_list) > 0:
                filter_string = f"chips={','.join(chip_list)}"
                params.append(filter_string)

        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&ibp=htl;events&{'&'.join(params)}"
        print(url)

        try:
            document = fetch_html(url)
            events = get_events(document)
        except Exception as e:
            print(e)
            return render_template('index.html', events="404")
        # print(json.dumps(events, indent=4))
        return render_template('index.html', events=events)
    except Exception as e:
        print(e)
        return render_template('index.html', events="404")


if __name__ == '__main__':
    with open('config.json', 'r') as file:
        ipgeolocation_API_KEY = json.load(file)["ipgeolocation"]
    
    # Run the app on localhost and port 5000
    app.run(port=8080, debug=True)
