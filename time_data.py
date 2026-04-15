import requests
from datetime import datetime
from zoneinfo import ZoneInfo


class PrayerDatabase:
    def __init__(
        self,
        latitude="43.39326",
        longitude="-79.26116",
        timeZone="America/Toronto",
        method="2",
        both="true",
        hour="0"
    ):
        # Store API parameters for location and calculation method
        self.latitude = latitude
        self.longitude = longitude
        self.timeZone = timeZone
        self.method = method
        self.both = both
        self.hour = hour

        # Get the current year based on the specified timezone
        self.year = datetime.now(ZoneInfo(self.timeZone)).year

        # This will store all processed prayer data (list of rows)
        self.data = []

    def _fetch_year(self, year):
        # Build the API URL with query parameters
        url = (
            "https://moonsighting.ahmedbukhamsin.sa/time_json.php?"
            f"year={year}&tz={self.timeZone}&lat={self.latitude}"
            f"&lon={self.longitude}&method={self.method}"
            f"&both={self.both}&time={self.hour}"
        )

        # Send GET request to API and return JSON response
        response = requests.get(url, timeout=5)
        return response.json()

    def _data_to_list(self, raw_data, year):
        # Extract the list of daily prayer data from API response
        times_list = raw_data["times"]

        # This will store processed rows
        rows = []

        # Loop through each day's data
        for daily_data in times_list:

            # Convert day string (e.g. "Jan 01 Thu") into a datetime object
            day_dt = datetime.strptime(
                f"{year} {daily_data['day']}", "%Y %b %d %a"
            )

            # Build a row with date + all prayer times (converted to time objects)
            row = [
                day_dt,
                datetime.strptime(daily_data["times"]["fajr"].strip(), "%H:%M").time(),
                datetime.strptime(daily_data["times"]["sunrise"].strip(), "%H:%M").time(),
                datetime.strptime(daily_data["times"]["dhuhr"].strip(), "%H:%M").time(),
                datetime.strptime(daily_data["times"]["asr"].strip(), "%H:%M").time(),
                datetime.strptime(daily_data["times"]["maghrib"].strip(), "%H:%M").time(),
                datetime.strptime(daily_data["times"]["isha"].strip(), "%H:%M").time(),
            ]

            # Add row to list
            rows.append(row)

        # Return list of rows for that year
        return rows

    def load_data(self):
        try:
            # Fetch raw data for previous, current, and next year
            prev = self._fetch_year(self.year - 1)
            curr = self._fetch_year(self.year)
            next_ = self._fetch_year(self.year + 1)

            # Convert raw API data into structured rows
            data_prev = self._data_to_list(prev, self.year - 1)
            data_curr = self._data_to_list(curr, self.year)
            data_next = self._data_to_list(next_, self.year + 1)

            # Combine all years into one dataset
            self.data = data_prev + data_curr + data_next

        except requests.exceptions.RequestException as e:
            # Handle API request errors (network, timeout, etc.)
            print(f"API request failed: {e}")

    def get_today_row(self):
        # Get today's date based on timezone
        today = datetime.now(ZoneInfo(self.timeZone)).date()

        # Search through all rows to find today's data
        for row in self.data:
            if row[0].date() == today:
                return row  # Return matching row

        # If no match found, return None
        return None

    # Algo for now
    # fajr: 30-45, zuhr: 25-40, asr: 30-45, isha: 30-45 between 7 and 10:45