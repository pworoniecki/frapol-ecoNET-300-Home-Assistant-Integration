"""Sensor platform for frapol_econet300_heat_recovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass

from .const import API_REG_PARAM_CURRENT_EXHAUST_TEMPERATURE, API_REG_PARAM_CURRENT_EXTRACT_FAN_SPEED, API_REG_PARAM_CURRENT_EXTRACT_TEMPERATURE, API_REG_PARAM_CURRENT_INTAKE_TEMPERATURE, API_REG_PARAM_CURRENT_LEADING_TEMPERATURE, API_REG_PARAM_CURRENT_SET_TEMPERATURE, API_REG_PARAM_CURRENT_SUPPLY_FAN_SPEED, API_REG_PARAM_CURRENT_SUPPLY_TEMPERATURE, LOGGER

from .entity import FrapolEconet300Entity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import FrapolEconet300DataUpdateCoordinator
    from .data import FrapolEconet300ConfigEntry


@dataclass
class FrapolEconet300SensorData:
    description: SensorEntityDescription
    value_extractor: Callable[[dict], str | None]
    id_suffix: str


SENSORS: list[FrapolEconet300SensorData] = (
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_supply_fan_speed",
            name="Supply Fan Speed",
            icon="mdi:fan-chevron-down",
            native_unit_of_measurement="%",
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_SUPPLY_FAN_SPEED),
        id_suffix="supply-fan-speed"
    ),
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_extract_fan_speed",
            name="Extract Fan Speed",
            icon="mdi:fan-chevron-up",
            native_unit_of_measurement="%",
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_EXTRACT_FAN_SPEED),
        id_suffix="extract-fan-speed"
    ),
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_leading_temperature",
            name="Leading Temperature",
            icon="mdi:thermometer-lines",
            native_unit_of_measurement="°C",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_LEADING_TEMPERATURE),
        id_suffix="leading-temperature"
    ),
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_set_temperature",
            name="Set Temperature",
            icon="mdi:thermometer-check",
            native_unit_of_measurement="°C",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_SET_TEMPERATURE),
        id_suffix="set-temperature"
    ),
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_supply_temperature",
            name="Supply Temperature",
            icon="mdi:home-thermometer",
            native_unit_of_measurement="°C",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_SUPPLY_TEMPERATURE),
        id_suffix="supply-temperature"
    ),
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_intake_temperature",
            name="Intake Temperature",
            icon="mdi:thermometer-chevron-down",
            native_unit_of_measurement="°C",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_INTAKE_TEMPERATURE),
        id_suffix="intake-temperature"
    ),
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_extract_temperature",
            name="Extract Temperature",
            icon="mdi:thermometer-chevron-up",
            native_unit_of_measurement="°C",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_EXTRACT_TEMPERATURE),
        id_suffix="extract-temperature"
    ),
    FrapolEconet300SensorData(
        description=SensorEntityDescription(
            key="frapol_econet300_heat_exhaust_temperature",
            name="Exhaust Temperature",
            icon="mdi:sun-thermometer",
            native_unit_of_measurement="°C",
            device_class=SensorDeviceClass.TEMPERATURE,
            state_class=SensorStateClass.MEASUREMENT
        ),
        value_extractor=lambda data: data.get("regParams").get("curr").get(API_REG_PARAM_CURRENT_EXHAUST_TEMPERATURE),
        id_suffix="exhaust-temperature"
    )
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
            sensor_data=sensor_data,
        )
        for sensor_data in SENSORS
    )


class FrapolEconet300Sensor(FrapolEconet300Entity, SensorEntity):
    """frapol_econet300_heat_recovery Sensor class."""

    def __init__(
        self,
        coordinator: FrapolEconet300DataUpdateCoordinator,
        sensor_data: FrapolEconet300SensorData,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = sensor_data.description
        self._sensor_data = sensor_data

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self._sensor_data.value_extractor(self.coordinator.data)

    @property
    def unique_id(self) -> str:
        uid = self.coordinator.data.get("sysParams").get("uid")
        return f"frapol-econet300-{uid}-{self._sensor_data.id_suffix}"
