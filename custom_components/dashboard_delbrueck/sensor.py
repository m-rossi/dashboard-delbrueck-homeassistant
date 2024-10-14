import datetime
from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SENSORS, STATIONS, UNIT_CONVERTER, WIND_BEARINGS
from .api import DashboardDelbrueckApi


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            DashboardDelbrueckSensor(
                hass,
                api,
                sensor_id,
                v[0],
                v[1],
                v[2],
                f"{entry.unique_id}-{api.station_id}-{sensor_id}",
            )
            for sensor_id, v in SENSORS.items()
        ]
    )


class DashboardDelbrueckSensor(SensorEntity):
    def __init__(
        self,
        hass: HomeAssistant,
        api: DashboardDelbrueckApi,
        sensor_id: int,
        name: str,
        device_class: str,
        state_class: str,
        unique_id: str,
    ):
        self.hass = hass
        self.entity_id = replace_umlauts(
            f"sensor.{STATIONS[api.station_id]}_{name.replace(' ', '_')}".lower()
        )
        self._api = api
        self._sensor_id = sensor_id
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_unique_id = unique_id
        if self.device_class == SensorDeviceClass.ENUM:
            self._attr_entity_picture = "mdi:compass"
            self._attr_options = list(WIND_BEARINGS.values())

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        try:
            data = self._api.get_sensor_value(self._sensor_id)
            if data["timestamp"] < datetime.datetime.now(
                ZoneInfo("Europe/Berlin")
            ) - datetime.timedelta(hours=1):
                raise ValueError(
                    "Data is older than an hour, weather station may be offline, value"
                    " will not be stored."
                )
            if self.device_class == SensorDeviceClass.ENUM:
                self._attr_native_value = WIND_BEARINGS[data["value"]]
            else:
                self._attr_native_value = data["value"]
                self._attr_native_unit_of_measurement = UNIT_CONVERTER[data["unit"]]
        except ConnectionError:
            self._attr_native_value = None
        except ValueError:
            self._attr_native_value = None
            if "unit" in data and data["unit"] in UNIT_CONVERTER:
                self._attr_native_unit_of_measurement = UNIT_CONVERTER[data["unit"]]


def replace_umlauts(text: str) -> str:
    return (
        text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    )
