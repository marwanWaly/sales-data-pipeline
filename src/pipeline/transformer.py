import pandas as pd
import numpy as np
import requests
from typing import List
import os


def get_customers_from_api(customers_api_url: str, user_ids: List[int]):
    customers_obj = {}
    try:
        response = requests.get(customers_api_url)
        customers_obj = response.json()
    except Exception as e:
        print("WARNING: Cannot get users data dua to the following error:\n", str(e))

    customers = [{
        "customer_id": u.get("id", np.nan),
        "name": u.get("name", np.nan),
        "username": u.get("username", np.nan),
        "email": u.get("email", np.nan),
        "lat": u.get("address", {}).get("geo", {}).get("lat", np.nan),
        "lng": u.get("address", {}).get("geo", {}).get("lng", np.nan),
    } for u in customers_obj if u.get("id", np.nan) in user_ids]

    return customers


def add_weather_data(customers: List[dict], weather_url: str) -> None:
    api_key = os.environ['WEATHER_API_KEY']

    for u in customers:
        customer_id = u["customer_id"]
        lat, lng = u.get("lat", None), u.get("lng", None)
        weather_data = {
            "temp": np.nan,
            "feels_like": np.nan,
            "temp_min": np.nan,
            "temp_max": np.nan,
            "pressure": np.nan,
            "humidity": np.nan,
            "sea_level": np.nan,
            "grnd_level": np.nan
        }

        if lat and lng:
            url = weather_url.format(lat=lat, lon=lng, API_KEY=api_key)

            weather_info = None
            try:
                response = requests.get(url)
                weather_info = response.json()
            except Exception as e:
                print(f"WARNING: Cannot get weather data for customer_id: {customer_id}"
                      f" with lat={lat} and lng={lng} dua to the following error:\n{str(e)}")

            if not weather_info:
                return

            status = weather_info["cod"]
            if status != 200:
                print(f"WARNING: Cannot get weather data for customer_id: {customer_id}"
                      f" with lat={lat} and lng={lng} response status code is {status}")

            main_info = weather_info.get("main", None)

            if main_info:
                weather_data = {
                    "temp": main_info.get("temp", np.nan),
                    "feels_like": main_info.get("feels_like", np.nan),
                    "temp_min": main_info.get("temp_min", np.nan),
                    "temp_max": main_info.get("temp_max", np.nan),
                    "pressure": main_info.get("pressure", np.nan),
                    "humidity": main_info.get("humidity", np.nan),
                    "sea_level": main_info.get("sea_level", np.nan),
                    "grnd_level": main_info.get("grnd_level", np.nan)
                }
            else:
                print(f"WARNING: Cannot get weather data for customer_id: {customer_id}"
                      f" because: there are no lat and lng information")

        u.update(weather_data)


def get_customers_data(customer_api: str, weather_api: str, customers_ids: List[int]) -> pd.DataFrame:
    customers = get_customers_from_api(customer_api, customers_ids)
    add_weather_data(customers, weather_api)
    customers_df = pd.DataFrame.from_dict(customers)
    return customers_df
