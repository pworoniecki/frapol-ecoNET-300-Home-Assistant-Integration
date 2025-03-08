"""Select for Econet300."""

import logging

from homeassistant.components.select import (
    SelectEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api
from .const import (
    DOMAIN,
    SERVICE_API,
)

_LOGGER = logging.getLogger(__name__)

MAIN_MODES = {
    1: "Off",
    2: "Paused",
    3: "Mode 1",
    4: "Mode 2",
    5: "Mode 3",
    6: "Mode 4",
}

TEMP_MODES = {
    1: "Off",
    2: "Exit mode",
    3: "Party mode",
    4: "Quick ventilation",
}


class MainModeSelect(SelectEntity):
    def __init__(self, api: Econet300Api):
        self._api = api
        self._attr_options = list(MAIN_MODES.values())
        self._attr_name = "Main Working Mode"
        self._attr_unique_id = "frapol-recuperator_main_mode"

    async def async_update(self):
        data = await self._api.fetch_reg_params_data()
        self._attr_current_option = MAIN_MODES.get(data.get("REKWS1"), "Unknown")

    async def select_option(self, option: str):
        for key, value in MAIN_MODES.items():
            if value == option and await self._api.set_param("REKWS1", key):
                self._attr_current_option = option
                self.async_write_ha_state()

    def current_option(self) -> str | None:
        return self._attr_current_option


class TempModeSelect(SelectEntity):
    def __init__(self, api: Econet300Api):
        self._api = api
        self._attr_options = list(TEMP_MODES.values())
        self._attr_name = "Temporary Working Mode"
        self._attr_unique_id = "frapol-recuperator_temp_mode"

    async def async_update(self):
        data = await self._api.fetch_reg_params_data()
        self._attr_current_option = MAIN_MODES.get(data.get("REKWS4"), "Unknown")

    async def select_option(self, option: str):
        for key, value in MAIN_MODES.items():
            if value == option and await self._api.set_param("REKWS4", key):
                self._attr_current_option = option
                self.async_write_ha_state()

    def current_option(self) -> str | None:
        return self._attr_current_option


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> bool:
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    # Add entities to Home Assistant
    async_add_entities([
        MainModeSelect(api),
        TempModeSelect(api)
    ])
    _LOGGER.info("Select entities successfully added to Home Assistant")
    return True
