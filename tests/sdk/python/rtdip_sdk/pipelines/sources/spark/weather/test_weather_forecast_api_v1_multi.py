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

import json
import pandas as pd
import pytest

from src.sdk.python.rtdip_sdk.pipelines.sources.spark.weather import WeatherForecastAPIV1MultiSource
from src.sdk.python.rtdip_sdk.pipelines._pipeline_utils.weather import WEATHER_FORECAST_SCHEMA
from src.sdk.python.rtdip_sdk.pipelines._pipeline_utils.models import Libraries
from pyspark.sql import DataFrame, SparkSession
from pytest_mock import MockerFixture

configuration = {
    "api_key": "AA",
    "language": "en-US",
    "units": "e",
    "stations": [
        "32.3667,-95.4",
        "51.52,-0.11"
    ]
}

raw_api_response1 = {
    "metadata": {
        "language": "en-US",
        "transaction_id": "1686945524067:722833eedd2545334406be2bd368acdf",
        "version": "1",
        "latitude": 32.36,
        "longitude": -95.4,
        "units": "e",
        "expire_time_gmt": 1686945840,
        "status_code": 200
    },
    "forecasts": [
        {
            "class": "fod_short_range_hourly",
            "expire_time_gmt": 1686945840,
            "fcst_valid": 1686945600,
            "fcst_valid_local": "2023-06-16T15:00:00-0500",
            "num": 1,
            "day_ind": "D",
            "temp": 91,
            "dewpt": 77,
            "hi": 105,
            "wc": 91,
            "feels_like": 105,
            "icon_extd": 2800,
            "wxman": "wx1230",
            "icon_code": 28,
            "dow": "Friday",
            "phrase_12char": "M Cloudy",
            "phrase_22char": "Mostly Cloudy",
            "phrase_32char": "Mostly Cloudy",
            "subphrase_pt1": "Mostly",
            "subphrase_pt2": "Cloudy",
            "subphrase_pt3": "",
            "pop": 15,
            "precip_type": "rain",
            "qpf": 0.0,
            "snow_qpf": 0.0,
            "rh": 64,
            "wspd": 6,
            "wdir": 233,
            "wdir_cardinal": "SW",
            "gust": None,
            "clds": 79,
            "vis": 10.0,
            "mslp": 29.77,
            "uv_index_raw": 5.65,
            "uv_index": 6,
            "uv_warning": 0,
            "uv_desc": "High",
            "golf_index": 8,
            "golf_category": "Very Good",
            "severity": 1
        },
        {
            "class": "fod_short_range_hourly",
            "expire_time_gmt": 1686945840,
            "fcst_valid": 1686949200,
            "fcst_valid_local": "2023-06-16T16:00:00-0500",
            "num": 2,
            "day_ind": "D",
            "temp": 91,
            "dewpt": 77,
            "hi": 105,
            "wc": 91,
            "feels_like": 105,
            "icon_extd": 2800,
            "wxman": "wx1230",
            "icon_code": 28,
            "dow": "Friday",
            "phrase_12char": "M Cloudy",
            "phrase_22char": "Mostly Cloudy",
            "phrase_32char": "Mostly Cloudy",
            "subphrase_pt1": "Mostly",
            "subphrase_pt2": "Cloudy",
            "subphrase_pt3": "",
            "pop": 15,
            "precip_type": "rain",
            "qpf": 0.0,
            "snow_qpf": 0.0,
            "rh": 63,
            "wspd": 5,
            "wdir": 235,
            "wdir_cardinal": "SW",
            "gust": None,
            "clds": 69,
            "vis": 10.0,
            "mslp": 29.76,
            "uv_index_raw": 5.08,
            "uv_index": 5,
            "uv_warning": 0,
            "uv_desc": "Moderate",
            "golf_index": 8,
            "golf_category": "Very Good",
            "severity": 1
        }
    ]
}

raw_api_response2 = {
    "metadata": {
        "language": "en-US",
        "transaction_id": "1687109472873:deb4a00064d1c75e7e7fc7e6cdce8274",
        "version": "1",
        "latitude": 51.52,
        "longitude": -0.11,
        "units": "e",
        "expire_time_gmt": 1687110027,
        "status_code": 200
    },
    "forecasts": [
        {
            "class": "fod_short_range_hourly",
            "expire_time_gmt": 1687110027,
            "fcst_valid": 1687111200,
            "fcst_valid_local": "2023-06-18T19:00:00+0100",
            "num": 1,
            "day_ind": "D",
            "temp": 66,
            "dewpt": 62,
            "hi": 66,
            "wc": 66,
            "feels_like": 66,
            "icon_extd": 1201,
            "wxman": "wx2500",
            "icon_code": 11,
            "dow": "Sunday",
            "phrase_12char": "Light Rain",
            "phrase_22char": "Light Rain",
            "phrase_32char": "Light Rain",
            "subphrase_pt1": "Light",
            "subphrase_pt2": "Rain",
            "subphrase_pt3": "",
            "pop": 86,
            "precip_type": "rain",
            "qpf": 0.02,
            "snow_qpf": 0.0,
            "rh": 85,
            "wspd": 4,
            "wdir": 207,
            "wdir_cardinal": "SSW",
            "gust": None,
            "clds": 80,
            "vis": 9.0,
            "mslp": 29.74,
            "uv_index_raw": 0.35,
            "uv_index": 0,
            "uv_warning": 0,
            "uv_desc": "Low",
            "golf_index": 6,
            "golf_category": "Good",
            "severity": 1
        },
        {
            "class": "fod_short_range_hourly",
            "expire_time_gmt": 1687110027,
            "fcst_valid": 1687114800,
            "fcst_valid_local": "2023-06-18T20:00:00+0100",
            "num": 2,
            "day_ind": "D",
            "temp": 66,
            "dewpt": 61,
            "hi": 66,
            "wc": 66,
            "feels_like": 66,
            "icon_extd": 1100,
            "wxman": "wx2500",
            "icon_code": 11,
            "dow": "Sunday",
            "phrase_12char": "Showers",
            "phrase_22char": "Showers",
            "phrase_32char": "Showers",
            "subphrase_pt1": "Showers",
            "subphrase_pt2": "",
            "subphrase_pt3": "",
            "pop": 53,
            "precip_type": "rain",
            "qpf": 0.01,
            "snow_qpf": 0.0,
            "rh": 84,
            "wspd": 6,
            "wdir": 218,
            "wdir_cardinal": "SW",
            "gust": None,
            "clds": 77,
            "vis": 9.0,
            "mslp": 29.75,
            "uv_index_raw": 0.09,
            "uv_index": 0,
            "uv_warning": 0,
            "uv_desc": "Low",
            "golf_index": 6,
            "golf_category": "Good",
            "severity": 1
        }
    ]
}

expected_json = {"Latitude": {"0": 32.3667, "1": 32.3667, "2": 51.52, "3": 51.52},
                 "Longitude": {"0": -95.4, "1": -95.4, "2": -0.11, "3": -0.11},
                 "Class": {"0": "fod_short_range_hourly", "1": "fod_short_range_hourly", "2": "fod_short_range_hourly",
                           "3": "fod_short_range_hourly"},
                 "ExpireTimeGmt": {"0": 1686945840, "1": 1686945840, "2": 1687110027, "3": 1687110027},
                 "FcstValid": {"0": 1686945600, "1": 1686949200, "2": 1687111200, "3": 1687114800},
                 "FcstValidLocal": {"0": "2023-06-16T15:00:00-0500", "1": "2023-06-16T16:00:00-0500",
                                      "2": "2023-06-18T19:00:00+0100", "3": "2023-06-18T20:00:00+0100"},
                 "Num": {"0": 1, "1": 2, "2": 1, "3": 2}, "DayInd": {"0": "D", "1": "D", "2": "D", "3": "D"},
                 "Temp": {"0": 91, "1": 91, "2": 66, "3": 66}, "Dewpt": {"0": 77, "1": 77, "2": 62, "3": 61},
                 "Hi": {"0": 105, "1": 105, "2": 66, "3": 66}, "Wc": {"0": 91, "1": 91, "2": 66, "3": 66},
                 "FeelsLike": {"0": 105, "1": 105, "2": 66, "3": 66},
                 "IconExtd": {"0": 2800, "1": 2800, "2": 1201, "3": 1100},
                 "Wxman": {"0": "wx1230", "1": "wx1230", "2": "wx2500", "3": "wx2500"},
                 "IconCode": {"0": 28, "1": 28, "2": 11, "3": 11},
                 "Dow": {"0": "Friday", "1": "Friday", "2": "Sunday", "3": "Sunday"},
                 "Phrase12Char": {"0": "M Cloudy", "1": "M Cloudy", "2": "Light Rain", "3": "Showers"},
                 "Phrase22Char": {"0": "Mostly Cloudy", "1": "Mostly Cloudy", "2": "Light Rain", "3": "Showers"},
                 "Phrase32Char": {"0": "Mostly Cloudy", "1": "Mostly Cloudy", "2": "Light Rain", "3": "Showers"},
                 "SubphrasePt1": {"0": "Mostly", "1": "Mostly", "2": "Light", "3": "Showers"},
                 "SubphrasePt2": {"0": "Cloudy", "1": "Cloudy", "2": "Rain", "3": ""},
                 "SubphrasePt3": {"0": "", "1": "", "2": "", "3": ""},
                 "Pop": {"0": "15", "1": "15", "2": "86", "3": "53"},
                 "PrecipType": {"0": "rain", "1": "rain", "2": "rain", "3": "rain"},
                 "Qpf": {"0": 0.0, "1": 0.0, "2": 0.02, "3": 0.01},
                 "SnowQpf": {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.0}, "Rh": {"0": 64, "1": 63, "2": 85, "3": 84},
                 "Wspd": {"0": 6, "1": 5, "2": 4, "3": 6}, "Wdir": {"0": 233, "1": 235, "2": 207, "3": 218},
                 "WdirCardinal": {"0": "SW", "1": "SW", "2": "SSW", "3": "SW"},
                 "Gust": {"0": None, "1": None, "2": None, "3": None}, "Clds": {"0": 79, "1": 69, "2": 80, "3": 77},
                 "Vis": {"0": 10.0, "1": 10.0, "2": 9.0, "3": 9.0},
                 "Mslp": {"0": 29.77, "1": 29.76, "2": 29.74, "3": 29.75},
                 "UvIndexRaw": {"0": 5.65, "1": 5.08, "2": 0.35, "3": 0.09},
                 "UvIndex": {"0": 6, "1": 5, "2": 0, "3": 0}, "UvWarning": {"0": 0, "1": 0, "2": 0, "3": 0},
                 "UvDesc": {"0": "High", "1": "Moderate", "2": "Low", "3": "Low"},
                 "GolfIndex": {"0": 8.0, "1": 8.0, "2": 6.0, "3": 6.0},
                 "GolfCategory": {"0": "Very Good", "1": "Very Good", "2": "Good", "3": "Good"},
                 "Severity": {"0": 1, "1": 1, "2": 1, "3": 1}}


def get_api_response(url: str) -> str:
    if url == "https://api.weather.com/v1/geocode/32.3667/-95.4/forecast/hourly/360hour.json":
        return json.dumps(raw_api_response1)
    else:
        return json.dumps(raw_api_response2)


def test_weather_forecast_api_v1_multi_read_setup(spark_session: SparkSession):
    weather_source = WeatherForecastAPIV1MultiSource(spark_session, configuration)

    assert weather_source.system_type().value == 2
    assert weather_source.libraries() == Libraries(maven_libraries=[], pypi_libraries=[], pythonwheel_libraries=[])

    assert isinstance(weather_source.settings(), dict)

    assert sorted(weather_source.required_options) == ["api_key", "stations"]
    assert weather_source.weather_url == "https://api.weather.com/v1/geocode/"
    assert weather_source.pre_read_validation()


def test_weather_forecast_api_v1_multi_params(spark_session: SparkSession):
    weather_source = WeatherForecastAPIV1MultiSource(spark_session, configuration)

    assert weather_source.units == "e"
    assert weather_source.api_key == "AA"
    assert weather_source.language == "en-US"


def test_weather_forecast_api_v1_multi_read_batch(spark_session: SparkSession, mocker: MockerFixture):
    weather_source = WeatherForecastAPIV1MultiSource(spark_session, configuration)

    class MyResponse:
        content = bytes()
        status_code = 200

    def get_response(url: str, params: dict):
        valid_urls = [
            "https://api.weather.com/v1/geocode/32.3667/-95.4/forecast/hourly/360hour.json",
            "https://api.weather.com/v1/geocode/51.52/-0.11/forecast/hourly/360hour.json",
        ]
        assert url in valid_urls
        assert params == {'apiKey': 'AA', 'units': 'e', 'language': 'en-US'}

        sample_bytes = bytes(get_api_response(url).encode("utf-8"))

        response = MyResponse()
        response.content = sample_bytes

        return response

    mocker.patch("requests.get", side_effect=get_response)

    df = weather_source.read_batch()

    assert df.count() == 4
    assert isinstance(df, DataFrame)
    assert str(df.schema) == str(WEATHER_FORECAST_SCHEMA)

    pdf = df.toPandas()
    expected_df = pd.DataFrame(expected_json)
    assert str(pdf.to_json()) == str(expected_df.to_json())


def test_weather_forecast_api_v1_multi_invalid_stations(spark_session: SparkSession):
    with pytest.raises(ValueError) as exc_info:
        iso_source = WeatherForecastAPIV1MultiSource(spark_session, {**configuration, "stations": ["45", "22"]})
        iso_source.pre_read_validation()

    assert str(exc_info.value) == "Each station item must contain comma separated Latitude & Longitude. Eg: 10.23:45.2"

    with pytest.raises(ValueError) as exc_info:
        iso_source = WeatherForecastAPIV1MultiSource(spark_session, {**configuration, "stations": ["45, "]})
        iso_source.pre_read_validation()

    assert str(exc_info.value) == "Each station item must contain comma separated Latitude & Longitude. Eg: 10.23:45.2"