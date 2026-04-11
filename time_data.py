import requests
from datetime import datetime

# API parameters
latitude = "43.39326"
longitude = "-79.26116"
timeZone = "America/Toronto"
method = "2"
year = "2026"
both = "true"
hour = "0"

try:
    # Make API request to fetch prayer times data
    response = requests.get(
        "https://moonsighting.ahmedbukhamsin.sa/time_json.php?year=" + year +
        "&tz=" + timeZone +
        "&lat=" + latitude +
        "&lon=" + longitude +
        "&method=" + method +
        "&both=" + both +
        "&time=" + hour,
        timeout=5
    )

    # Raise an error if response status is not successful (e.g. 404, 500)
    response.raise_for_status()

    # Convert API response to Python dictionary
    raw_data = response.json()

    # Extract the list of daily prayer data
    times_list = raw_data["times"]

    # Initialize lists for each column of data
    days_list = []
    fajr_list = []
    sunrise_list = []
    dhuhr_list = []
    asr_list = []
    maghrib_list = []
    isha_list = []

    # Loop through each day's data
    for daily_data in times_list:

        # Convert day string (e.g. "Jan 01 Thu") into datetime object
        days_list.append(
            datetime.strptime(f"{year} {daily_data['day']}", "%Y %b %d %a")
        )

        # Convert prayer times (strings) into time objects
        # .strip() removes trailing spaces from API response
        fajr_list.append(
            datetime.strptime(daily_data["times"]["fajr"].strip(), "%H:%M").time()
        )
        sunrise_list.append(
            datetime.strptime(daily_data["times"]["sunrise"].strip(), "%H:%M").time()
        )
        dhuhr_list.append(
            datetime.strptime(daily_data["times"]["dhuhr"].strip(), "%H:%M").time()
        )
        asr_list.append(
            datetime.strptime(daily_data["times"]["asr"].strip(), "%H:%M").time()
        )
        maghrib_list.append(
            datetime.strptime(daily_data["times"]["maghrib"].strip(), "%H:%M").time()
        )
        isha_list.append(
            datetime.strptime(daily_data["times"]["isha"].strip(), "%H:%M").time()
        )

    # Combine all column lists into rows (table format)
    # Each row = [day, fajr, sunrise, dhuhr, asr, maghrib, isha]
    data = [
        list(row) for row in zip(
            days_list,
            fajr_list,
            sunrise_list,
            dhuhr_list,
            asr_list,
            maghrib_list,
            isha_list
        )
    ]

# Catch any request-related errors (connection issues, timeout, bad response)
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")