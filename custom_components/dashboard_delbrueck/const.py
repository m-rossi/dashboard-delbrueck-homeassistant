from homeassistant.const import (
    UnitOfSpeed,
    UnitOfPrecipitationDepth,
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass


DOMAIN = "dashboard_delbrueck"
CONF_STATION_ID = "station_id"
STATIONS = {
    "0": "Delbrück",
    "1": "Anreppen",
    "2": "Bentfeld",
    "3": "Boke",
    "4": "Lippling",
    "5": "Ostenland",
    "6": "Schöning",
    "7": "Steinhorst",
    "8": "Sudhagen",
    "9": "Westenholz",
}
SENSORS = {
    1: ("Temperatur", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
    2: (
        "Gefühlte Temperatur",
        SensorDeviceClass.TEMPERATURE,
        SensorStateClass.MEASUREMENT,
    ),
    3: (
        "Relative Luftfeuchtigkeit",
        SensorDeviceClass.HUMIDITY,
        SensorStateClass.MEASUREMENT,
    ),
    4: ("Windrichtung", SensorDeviceClass.ENUM, None),
    5: (
        "Windgeschwindigkeit",
        SensorDeviceClass.WIND_SPEED,
        SensorStateClass.MEASUREMENT,
    ),
    6: (
        "Niederschlagsmenge",
        SensorDeviceClass.PRECIPITATION,
        SensorStateClass.TOTAL_INCREASING,
    ),
}
UNIT_CONVERTER = {
    "°C": UnitOfTemperature.CELSIUS,
    "%": PERCENTAGE,
    "km/h": UnitOfSpeed.KILOMETERS_PER_HOUR,
    "mm": UnitOfPrecipitationDepth.MILLIMETERS,
}
WIND_BEARINGS = {
    1.0: "N",
    2.0: "NNO",
    3.0: "NO",
    4.0: "ONO",
    5.0: "O",
    6.0: "OSO",
    7.0: "SO",
    8.0: "SSO",
    9.0: "S",
    10.0: "SSW",
    11.0: "SW",
    12.0: "WSW",
    13.0: "W",
    14.0: "WNW",
    15.0: "NW",
    16.0: "NNW",
}
