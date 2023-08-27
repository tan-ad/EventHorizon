import base64
from urllib.parse import quote
from datetime import datetime, timedelta
from dateparser import parse


def uule(city: str) -> str:
    encoded_city = city.encode()
    city_length = len(encoded_city)
    hashed = (
        base64.standard_b64encode(
            bytearray([8, 2, 16, 32, 34, city_length]) + encoded_city
        )
        .decode()
        .strip("=")
        .replace("+", "-")
        .replace("/", "_")
    )
    return f"w+{hashed}"


def google_calendar(event_title, event_time, event_details, event_location):
    try:
        event_time = event_time.replace(".", "").replace('am', 'AM').replace('pm', 'PM')
        start_time, end_time = event_time.split("–")
        start_time, end_time = parse(start_time), parse(end_time)
        if end_time < start_time:
            end_time = end_time.replace(year=start_time.year, month=start_time.month, day=start_time.day)
        # print(start_time, end_time)

        # Construct Google Calendar link
        google_calendar_link = (
            f'https://www.google.com/calendar/render?action=TEMPLATE'
            f'&text={quote(event_title)}'
            f'&dates={start_time.strftime("%Y%m%dT%H%M%S")}/{end_time.strftime("%Y%m%dT%H%M%S")}'
            f'&details={quote(event_details)}'
            f'&location={quote(event_location)}'
            f'&sf=true'
            f'&output=xml'
        )

        return google_calendar_link

    except Exception as e:
        # print(e)
        return ""


if __name__=='__main__':
    # testing
    location_data = {"country_code2": "ca", "city": "San Francisco", "state_prov": "California", "country_name": "United States"}
    uule_string = f"uule={uule(','.join([location_data['city'], location_data['state_prov'], location_data['country_name']]))}"
    print(uule_string)

    # Example usage
    event_details1 = "Fri, Sep 15, 8:00 p.m.–Sat, Sep 16, 12:00 a.m."
    event_details2 = "Thu, Sep 21, 7:00–11:00 p.m."

    link1 = google_calendar("Event Name", event_details1, "Event Details", "Palmer Square, 3 Palmer Sq W, Princeton, NJ, United States")
    link2 = google_calendar("Event Name", event_details2, "Event Details", "Rogers Centre, 1 Blue Jays Way, Toronto, ON M5V 1J1, Canada")

    print("Google Calendar Link 1:", link1)
    print("Google Calendar Link 2:", link2)
