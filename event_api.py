import requests
import json
import urllib.parse
from bs4 import BeautifulSoup
import sys
from utils import uule, google_calendar


def fetch_html(url):
    try:
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
        session = requests.get(url, headers=headers)
        session.raise_for_status()
        if session.text:
            save_html_to_file(session.text, 'events.html')
        return session.text
    except requests.exceptions.RequestException as e:
        print("Error fetching HTML:", e)
        return None


def save_html_to_file(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    # print(f"HTML content saved to {filename}")


def get_events(document):
    soup = BeautifulSoup(document, features="html.parser")
    images = str(soup).split("var _u='")
    thumbnails = []
    image_id = {}
    offset = 0
    for image in images:
        image_url = image.split("';")[0].replace("\\x3d", "=").replace("\\x26", "&")
        try:
            num = int(image.split("';")[1].split("_")[-1]) + offset
            if num % 2 == 0:
                image_id[num - 1] = image_url
                offset += 1
            if num % 4 == 3:
                image_id[num] = image_url
        except:
            continue

    for num in image_id:
        image_url = image_id[num]
        if 'images?q' in image_url:
            thumbnails.append(image_url)
            # print(image_url)
        if '/maps/vt' in image_url:
            thumbnails.append(f"https://www.google.com{image_url[:-1]}4")
            # print(f"https://www.google.com{image_url[:-1]}4")

    ul_element = soup.find('ul')

    event_results = []

    li_elements = ul_element.find_all('li', recursive=False)
    count = 0
    for li in li_elements:
        data, content = li.find('div').find('div').find_all('div', recursive=False)
        main_date, main_event, main_icon = content.find('div').find_all('div', recursive=False)[:3]
        main_date_day, main_date_month = main_date.find('div').find_all('div', recursive=False)
        # print(f"{main_date_day.text} {main_date_month.text}")

        main_event_name, main_event_info = main_event.find_all('div', recursive=False)
        main_event_info_date, main_event_info_address, main_event_info_city = main_event_info.find_all('div', recursive=False)
        # print(f"{main_event_name.text}")
        # print(f"{main_event_info_date.text} {main_event_info_address.text} {main_event_info_city.text}")
        data_divs = data.find('div').find('div').find('g-sticky-content-container').find('div').find_all('div', recursive=False)
        has_venue = True
        if len(data_divs) == 5:
            has_venue = False

        if has_venue:
            data_info, data_panel, data_details, data_tickets, data_venue, data_google = data_divs
        else:
            data_info, data_panel, data_details, data_tickets, data_google = data_divs
        
        data_info_date, data_info_name = data_info.find_all('div', recursive=False)
        data_info_day, data_info_month = data_info_date.find_all('div', recursive=False)
        # print(f"{data_info_day.text} {data_info_month.text} {data_info_name.text}")

        data_panel_tickets, data_panel_info, data_panel_directions = data_panel.find('div').find_all('div', recursive=False)[:3]
        data_panel_info_link = data_panel_info.find('a').get('href')
        try:
            data_panel_directions_link = f"https://www.google.com{data_panel_directions.find('a').get('data-url')}"
        except:
            data_panel_directions_link = ""
        # print(data_panel_info_link)
        # print(data_panel_directions_link)

        data_details_title, data_details_time, data_details_location, data_details_description = data_details.find_all('div', recursive=False)
        data_details_time_date, data_details_time_relative = data_details_time.find('div').find_all('div', recursive=False)
        data_details_location_link = f"https://www.google.com{data_details_location.find('a').get('data-url')}"
        try:
            data_details_description_content = data_details_description.find('div').find('span').text
        except AttributeError as e:
            data_details_description_content = ""
        try:
            data_details_description_link = data_details_description.find('div').find('a').get('href')
        except AttributeError as e:
            data_details_description_link = ""
        # print(f"{data_details_time_date.text} {data_details_time_relative.text}")
        # print(data_details_location_link)
        # print(data_details_description_content)
        # print(data_details_description_link)

        links = data_tickets.find_all('a')[::2]
        divs = data_tickets.find_all('div')
        domains = []
        for div in divs:
            if div.has_attr('data-domain'):
                domains.append(div.get('data-domain'))
        images = data.find_all('img')
        icons = []
        for image in images:
            if image.has_attr('data-src'):
                icons.append(image.get('data-src'))
        
        if has_venue:
            data_venue_title, data_venue_name, data_venue_rating, data_venue_search = data_venue.find_all('div', recursive=False)
            data_venue_rating_stars = float(data_venue_rating.find('span').text)
            data_venue_rating_count = int(data_venue_rating.find_all('span')[-1].text.split()[0].replace(',',''))
            data_venue_search_link = f"https://www.google.com{data_venue_search.find('div').find('a').get('href')}"
            venue_data = {"name": data_venue_name.text, "stars": data_venue_rating_stars, "reviews": data_venue_rating_count, "link": data_venue_search_link}
            # print(f"{data_venue_name.text} {data_venue_rating_stars} {data_venue_rating_count}")
            # print(data_venue_search_link)
        else:
            venue_data = {"name": "", "stars": "", "reviews": "", "link": ""}

        event_result = {
                            "title": data_info_name.text,
                            "date": {
                                "start_date": f"{main_date_day.text} {main_date_month.text}",
                                "when": data_details_time_date.text,
                                "relative": data_details_time_relative.text,
                                "calendar": google_calendar(data_info_name.text, 
                                                            data_details_time_date.text,
                                                            data_details_description_content,
                                                            main_event_info_address.text + ', ' + main_event_info_city.text)
                            }, 
                            "location": {
                                "address": main_event_info_address.text,
                                "city": main_event_info_city.text,
                                "maps": data_panel_directions_link
                            },
                            "link": data_details_description_link,
                            "description": data_details_description_content,
                            "ticket_info": [
                                {
                                    "source": domains[i],
                                    "link": links[i].get("href"),
                                    "icon": icons[i]
                                } for i in range(len(links))
                            ],
                            "venue": venue_data,
                            "thumbnail": thumbnails[count],
                        }
        event_results.append(event_result)

        count += 1

    return event_results
    # with open('events.json', 'w', encoding='utf-8') as file:
    #     json.dump(event_results, file, ensure_ascii=False, indent=4)

    # print("Events data saved to to events.json")


if __name__ == '__main__':
    # testing
    new_query = input("New query? (Y/N): ")
    if new_query.upper() == "Y":
        query = input("Enter search query: ")

        location_data = {"country_code2": "ca", "city": "San Francisco", "state_prov": "California", "country_name": "United States"}
        offset = 0
        uule_string = f"uule={uule(','.join([location_data['city'], location_data['state_prov'], location_data['country_name']]))}"
        hl_string = "hl=en"
        gl_string = f"gl={location_data['country_code2'].lower()}"
        offset_string = f"start={offset}"
        
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&ibp=htl;events&{'&'.join([uule_string, hl_string, gl_string, offset_string])}"

        html_content = fetch_html(url)

        if html_content:
            save_html_to_file(html_content, 'events.html')

    with open('events.html', 'r') as file:
        document = file.read()

    get_events(document)
