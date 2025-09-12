"""Select platform for frapol_econet300_heat_recovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from homeassistant.components.select import SelectEntity
from homeassistant.core import callback

from .const import API_REG_PARAM_CURRENT_MAIN_MODE, API_REG_PARAM_CURRENT_MAIN_MODE_MAPPING_VALUE_TO_NAME, API_REG_PARAM_CURRENT_TEMP_MODE_MAPPING_VALUE_TO_NAME, API_REG_PARAM_CURRENT_TEMPORARY_MODE, LOGGER

from .entity import FrapolEconet300Entity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import FrapolEconet300DataUpdateCoordinator
    from .data import FrapolEconet300ConfigEntry


@dataclass
class FrapolEconet300SelectData:
    name: str
    api_param_name: str
    value_to_name_mapping: dict[int, str]
    value_extractor: Callable[[dict], str | None]
    id_suffix: str


SELECTS: list[FrapolEconet300SelectData] = (
    FrapolEconet300SelectData(
        name="Main mode",
        api_param_name=API_REG_PARAM_CURRENT_MAIN_MODE,
        value_to_name_mapping=API_REG_PARAM_CURRENT_MAIN_MODE_MAPPING_VALUE_TO_NAME,
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_MAIN_MODE),
        id_suffix="main-mode"
    ),
    FrapolEconet300SelectData(
        name="Temporary mode",
        api_param_name=API_REG_PARAM_CURRENT_TEMPORARY_MODE,
        value_to_name_mapping=API_REG_PARAM_CURRENT_TEMP_MODE_MAPPING_VALUE_TO_NAME,
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_TEMPORARY_MODE),
        id_suffix="temp-mode"
    )
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: FrapolEconet300ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    async_add_entities(
        FrapolEconet300Select(
            coordinator=entry.runtime_data.coordinator,
            select_data=select_data,
        )
        for select_data in SELECTS
    )


class FrapolEconet300Select(FrapolEconet300Entity, SelectEntity):
    """frapol_econet300_heat_recovery Select class."""

    def __init__(
        self,
        coordinator: FrapolEconet300DataUpdateCoordinator,
        select_data: FrapolEconet300SelectData,
    ) -> None:
        """Initialize the select class."""
        super().__init__(coordinator)
        self._select_data = select_data
        self._name_to_value_mapping: dict[str, int] = dict((v, k) for k, v in self._select_data.value_to_name_mapping.items())
        self._attr_has_entity_name = True
        self._attr_name = select_data.name
        self._attr_options = list(self._name_to_value_mapping.keys())
        current_value = self._select_data.value_extractor(self.coordinator.data)
        self._attr_current_option = self._select_data.value_to_name_mapping.get(current_value, "Unknown")
        self._attr_translation_key = self._select_data.id_suffix

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        value = self._name_to_value_mapping[option]
        await self.coordinator.config_entry.runtime_data.client.set_param(self._select_data.api_param_name, str(value))
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        value = self._select_data.value_extractor(self.coordinator.data)
        self._attr_current_option = self._select_data.value_to_name_mapping.get(value, "Unknown")
        self.async_write_ha_state()

    @property
    def unique_id(self) -> str:
        uid = self.coordinator.data.get("sysParams").get("uid")
        return f"frapol-econet300-{uid}-{self._select_data.id_suffix}"
