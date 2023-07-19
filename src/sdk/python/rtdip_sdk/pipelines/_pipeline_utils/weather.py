# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyspark.sql.types import StructType, StructField, DoubleType, StringType, IntegerType, TimestampType

WEATHER_FORECAST_SCHEMA = StructType(
    [
        StructField("Latitude", DoubleType(), True),
        StructField("Longitude", DoubleType(), True),
        StructField("Class", StringType(), True),
        StructField("ExpireTimeGmt", IntegerType(), True),
        StructField("FcstValid", IntegerType(), True),
        StructField("FcstValidLocal", StringType(), True),
        StructField("Num", IntegerType(), True),
        StructField("DayInd", StringType(), True),
        StructField("Temp", IntegerType(), True),
        StructField("Dewpt", IntegerType(), True),
        StructField("Hi", IntegerType(), True),
        StructField("Wc", IntegerType(), True),
        StructField("FeelsLike", IntegerType(), True),
        StructField("IconExtd", IntegerType(), True),
        StructField("Wxman", StringType(), True),
        StructField("IconCode", IntegerType(), True),
        StructField("Dow", StringType(), True),
        StructField("Phrase12Char", StringType(), True),
        StructField("Phrase22Char", StringType(), True),
        StructField("Phrase32Char", StringType(), True),
        StructField("SubphrasePt1", StringType(), True),
        StructField("SubphrasePt2", StringType(), True),
        StructField("SubphrasePt3", StringType(), True),
        StructField("Pop", StringType(), True),
        StructField("PrecipType", StringType(), True),
        StructField("Qpf", DoubleType(), True),
        StructField("SnowQpf", DoubleType(), True),
        StructField("Rh", IntegerType(), True),
        StructField("Wspd", IntegerType(), True),
        StructField("Wdir", IntegerType(), True),
        StructField("WdirCardinal", StringType(), True),
        StructField("Gust", DoubleType(), True),
        StructField("Clds", IntegerType(), True),
        StructField("Vis", DoubleType(), True),
        StructField("Mslp", DoubleType(), True),
        StructField("UvIndexRaw", DoubleType(), True),
        StructField("UvIndex", IntegerType(), True),
        StructField("UvWarning", IntegerType(), True),
        StructField("UvDesc", StringType(), True),
        StructField("GolfIndex", DoubleType(), True),
        StructField("GolfCategory", StringType(), True),
        StructField("Severity", IntegerType(), True),

    ]
)

WEATHER_DATA_MODEL = StructType(
    [
        StructField("Latitude", DoubleType(), False),
        StructField("Longitude", DoubleType(), False),
        StructField('WeatherDay', StringType(), False),
        StructField('WeatherHour', IntegerType(), False),
        StructField('WeatherTimezoneOffset', StringType(), False),
        StructField('WeatherType', StringType(), False),
        StructField('ProcessedDate', TimestampType(), False),
        StructField('Temperature', DoubleType(), True),
        StructField('DewPoint', DoubleType(), True),
        StructField('Humidity', DoubleType(), True),
        StructField('HeatIndex', DoubleType(), True),
        StructField('WindChill', DoubleType(), True),
        StructField('WindDirection', DoubleType(), True),
        StructField('WindSpeed', DoubleType(), True),
        StructField('CloudCover', DoubleType(), True),
        StructField('WetBulbTemp', StringType(), True),
        StructField('SolarIrradiance', StringType(), True),
        StructField('Precipitation', DoubleType(), True),
        StructField('DayOrNight', StringType(), True),
        StructField('DayOfWeek', StringType(), True),
        StructField('WindGust', IntegerType(), True),
        StructField('MslPressure', DoubleType(), True),
        StructField('ForecastDayNum', IntegerType(), True),
        StructField('PropOfPrecip', IntegerType(), True),
        StructField('PrecipType', StringType(), True),
        StructField('SnowAccumulation', DoubleType(), True),
        StructField('UvIndex', DoubleType(), True),
        StructField('Visibility', DoubleType(), True)
    ]
)
