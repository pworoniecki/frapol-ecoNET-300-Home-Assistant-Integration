"""Sensor platform for frapol_econet300_heat_recovery."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import API_REG_PARAM_CURRENT_FAN_SPEED, LOGGER

from .entity import FrapolEconet300Entity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import FrapolEconet300DataUpdateCoordinator
    from .data import FrapolEconet300ConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="frapol_econet300_heat_current_fan_speed",
        name="Frapol ecoNET300 Heat Recovery Current Fan Speed",
        icon="mdi:fan",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: FrapolEconet300ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        FrapolEconet300Sensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class FrapolEconet300Sensor(FrapolEconet300Entity, SensorEntity):
    """frapol_econet300_heat_recovery Sensor class."""

    def __init__(
        self,
        coordinator: FrapolEconet300DataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_FAN_SPEED)
