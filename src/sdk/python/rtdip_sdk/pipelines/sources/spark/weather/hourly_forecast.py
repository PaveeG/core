# Copyright 2022 RTDIP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from collections import OrderedDict

import pandas as pd
import requests
from requests import HTTPError
from pyspark.sql import SparkSession

from .base_weather import WeatherAPISource
from ...._pipeline_utils.weather import WEATHER_FORECAST_SCHEMA

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class ForecastAPISourceV1(WeatherAPISource):
    """
    The MISO Daily Load ISO Source is used to read daily load data from MISO API. It supports both Actual and Forecast data.

    API: <a href="https://docs.misoenergy.org/marketreports/">https://docs.misoenergy.org/marketreports/</a>

    Actual data is available for one day minus from the given date.

    Forecast data is available for next 6 day (inclusive of given date).


    Args:
        spark (SparkSession): Spark Session instance
        options (dict): A dictionary of ISO Source specific configurations

    Attributes:
        load_type (str): Must be one of `actual` or `forecast`
        date (str): Must be in `YYYYMMDD` format.

    """

    spark: SparkSession
    spark_schema = WEATHER_FORECAST_SCHEMA
    options: dict
    weather_url: str = "https://api.weather.com/v1/geocode/"
    required_options = ["lat", "lon", "apiKey"]
    lat = ""
    lon = ""
    apiKey = ""
    language = ""
    units = ""
    params = {}

    def __init__(self, spark: SparkSession, options: dict) -> None:
        super().__init__(spark, options)
        self.spark = spark
        self.options = options
        self.lat = self.options.get("lat", "").strip()
        self.lon = self.options.get("lon", "").strip()
        self.apiKey = self.options.get("apiKey", "").strip()
        self.language = self.options.get("language", "en-US").strip()
        self.units = self.options.get("units", "e").strip()
        self.params = {}
        # self.params = self.options.get("params", {})

    def _sanitize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter outs data outside the requested date range.

        Args:
            df: Data received after preparation.

        Returns:
            Final data after all the transformations.

        """

        df = df.rename(columns={
            "class": "CLASS",
            "clds": "CLDS",
            "day_ind": "DAY_IND",
            "dewpt": "DEWPT",
            "dow": "DOW",
            "expire_time_gmt": "EXPIRE_TIME_GMT",
            "fcst_valid": "FCST_VALID",
            "fcst_valid_local": "FCST_VALID_LOCAL",
            "feels_like": "FEELS_LIKE",
            "golf_category": "GOLF_CATEGORY",
            "golf_index": "GOLF_INDEX",
            "gust": "GUST",
            "hi": "HI",
            "icon_code": "ICON_CODE",
            "icon_extd": "ICON_EXTD",
            "mslp": "MSLP",
            "num": "NUM",
            "phrase_12char": "PHRASE_12CHAR",
            "phrase_22char": "PHRASE_22CHAR",
            "phrase_32char": "PHRASE_32CHAR",
            "pop": "POP",
            "precip_type": "PRECIP_TYPE",
            "qpf": "QPF",
            "rh": "RH",
            "severity": "SEVERITY",
            "snow_qpf": "SNOW_QPF",
            "subphrase_pt1": "SUBPHRASE_PT1",
            "subphrase_pt2": "SUBPHRASE_PT2",
            "subphrase_pt3": "SUBPHRASE_PT3",
            "temp": "TEMP",
            "uv_desc": "UV_DESC",
            "uv_index": "UV_INDEX",
            "uv_index_raw": "UV_INDEX_RAW",
            "uv_warning": "UV_WARNING",
            "vis": "VIS",
            "wc": "WC",
            "wdir": "WDIR",
            "wdir_cardinal": "WDIR_CARDINAL",
            "wspd": "WSPD",
            "wxman": "WXMAN"
        })

        return df

    def _get_weather_api_url(self):
        print(f"{self.weather_url}/{self.lat}/{self.lon}/forecast/hourly/360hour.json")
        return f"{self.lat}/{self.lon}/forecast/hourly/360hour.json"

    def _get_params(self):
        self.params = {
            "language": self.language,
            "units": self.units,
            "apiKey": self.apiKey
        }
        return self.params

    def _fetch_from_url(self, url_suffix: str, params: {}) -> bytes:
        """
        Gets data from external Weather Forecast API.

        Args:
            url_suffix: String to be used as suffix to weather url.

        Returns:
            Raw content of the data received.

        """
        url = f"{self.weather_url}{url_suffix}"
        logging.info(f"Requesting URL - {url}")

        response = requests.get(url, params)
        code = response.status_code

        if code != 200:
            raise HTTPError(f"Unable to access URL `{url}`."
                            f" Received status code {code} with message {response.content}")

        return response.content

    def _pull_data(self) -> pd.DataFrame:
        """
        Pulls data from the MISO API and parses the Excel file.

        Returns:
            Raw form of data.
        """
        url = self._get_weather_api_url()
        params = self._get_params()

        print(url)
        print(params)

        import json

        response = json.loads(self._fetch_from_url(url, params).decode("utf-8"))
        # logging.info(f"Getting {self.load_type} data for date {self.date}")
        df = pd.DataFrame(response["forecasts"])

        return df
