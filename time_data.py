import requests
import pandas as pd
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

        # This will store all processed prayer data as a pandas DataFrame
        self.data = pd.DataFrame()

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
        response.raise_for_status()
        return response.json()

    def _data_to_dataframe(self, raw_data, year):
        # Extract the list of daily prayer data from API response
        times_list = raw_data["times"]

        # This will store processed rows as dictionaries
        rows = []

        # Loop through each day's data
        for daily_data in times_list:
            # Convert day string (e.g. "Jan 01 Thu") into a datetime object
            day_dt = datetime.strptime(
                f"{year} {daily_data['day']}", "%Y %b %d %a"
            )

            # Build one row as a dictionary
            # This is easier for pandas to convert into a DataFrame
            row = {
                "date": day_dt,
                "fajr": datetime.strptime(daily_data["times"]["fajr"].strip(), "%H:%M").time(),
                "sunrise": datetime.strptime(daily_data["times"]["sunrise"].strip(), "%H:%M").time(),
                "dhuhr": datetime.strptime(daily_data["times"]["dhuhr"].strip(), "%H:%M").time(),
                "asr": datetime.strptime(daily_data["times"]["asr"].strip(), "%H:%M").time(),
                "maghrib": datetime.strptime(daily_data["times"]["maghrib"].strip(), "%H:%M").time(),
                "isha": datetime.strptime(daily_data["times"]["isha"].strip(), "%H:%M").time(),
            }

            # Add row to list
            rows.append(row)

        # Convert list of dictionaries into a pandas DataFrame
        return pd.DataFrame(rows)

    def load_data(self):
        try:
            # Fetch raw data for previous, current, and next year
            prev = self._fetch_year(self.year - 1)
            curr = self._fetch_year(self.year)
            next_ = self._fetch_year(self.year + 1)

            # Convert raw API data into DataFrames
            data_prev = self._data_to_dataframe(prev, self.year - 1)
            data_curr = self._data_to_dataframe(curr, self.year)
            data_next = self._data_to_dataframe(next_, self.year + 1)

            # Combine all years into one DataFrame
            self.data = pd.concat([data_prev, data_curr, data_next], ignore_index=True)

        except requests.exceptions.RequestException as e:
            # Handle API request errors (network, timeout, bad response, etc.)
            print(f"API request failed: {e}")

    def get_today_row(self):
        # Return None if data has not been loaded yet
        if self.data.empty:
            return None

        # Get today's date based on timezone
        today = datetime.now(ZoneInfo(self.timeZone)).date()

        # Filter rows where the date column matches today's date
        matches = self.data[self.data["date"].dt.date == today]

        # If no match found, return None
        if matches.empty:
            return None

        # Return the first matching row as a pandas Series
        return matches.iloc[0]

    # def iqamah_calc(self):

    # Algo for now
    # fajr: 30-45, zuhr: 25-40, asr: 30-45, isha: 30-45 between 7 and 10:45