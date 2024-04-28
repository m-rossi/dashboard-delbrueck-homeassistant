import datetime

import requests


class DashboardDelbrueckApi:
    def __init__(
        self,
        station_id: int,
        base_url: str = "https://dashboard-delbrueck.regioit.de/api/widget/tab-1",
    ):
        self._station_id = station_id
        self._base_url = base_url

    @property
    def station_id(self) -> int:
        return self._station_id

    def get_sensor_value(self, sensor_id: int) -> dict:
        url = f"{self._base_url}/w-single-sensor-{sensor_id}/{self.station_id}"
        response = requests.get(url).json()
        return {
            "sensor_id": sensor_id,
            "value": response["wert"],
            "unit": response["einheit"],
            "timestamp": datetime.datetime.strptime(
                response["zeitstempel"],
                "%Y-%m-%dT%H:%M:%S.%f%z",
            ),
        }
