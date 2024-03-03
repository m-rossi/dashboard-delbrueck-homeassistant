import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import selector

from .const import DOMAIN, CONF_STATION_ID, STATIONS

_LOGGER = logging.getLogger(__name__)
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STATION_ID): selector(
            {
                "select": {
                    "options": [{"label": v, "value": k} for k, v in STATIONS.items()],
                    "custom_value": False,
                    "mode": "dropdown",
                },
            }
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    if data[CONF_STATION_ID] not in STATIONS:
        raise InvalidStationID(f"No station with ID {data[CONF_STATION_ID]} found.")
    return {"title": STATIONS[data[CONF_STATION_ID]]}


class DashboardDelbrueckConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except InvalidStationID:
                _LOGGER.exception("Invalid station id")
                errors["base"] = "invalid_station"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class InvalidStationID(HomeAssistantError):
    """Error to indicate a invalid station id."""
