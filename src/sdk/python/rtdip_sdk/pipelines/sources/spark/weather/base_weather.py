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
import pandas as pd
from pyspark.sql import SparkSession

from ...._pipeline_utils.iso import MISO_SCHEMA
from ..iso import BaseISOSource


class WeatherAPISource(BaseISOSource):
    """
    The MISO Daily Load ISO Source is used to read daily load data from MISO API. It supports both Actual and Forecast data.

    The Weather API Source is used to load 15 day forecast from Forecast API.

    API: <a href="https://api.weather.com/v1/geocode/32.3667/-95.4/forecast/hourly/360hour.json</a>


    Args:
        spark (SparkSession): Spark Session instance
        options (dict): A dictionary of ISO Source specific configurations

    Attributes:
        load_type (str): Must be one of `actual` or `forecast`
        date (str): Must be in `YYYYMMDD` format.

    """

    spark: SparkSession
    options: dict
    weather_url: str = "https://"
    spark_schema = " #weather schema"
    required_options: list = []

    def __init__(self, spark: SparkSession, options: dict) -> None:
        super().__init__(spark, options)
        self.spark = spark
        self.options = options


    def _get_weather_api_url(self):
        return ""

    def _pull_data(self) -> pd.DataFrame:
        """
        Pulls data from the MISO API and parses the Excel file.

        Returns:
            Raw form of data.
        """
        url = self._get_weather_api_url()
        import json

        response = json.loads(self._fetch_from_url(url).decode("utf-8"))
        # logging.info(f"Getting {self.load_type} data for date {self.date}")
        df = pd.DataFrame(response)

        return df

