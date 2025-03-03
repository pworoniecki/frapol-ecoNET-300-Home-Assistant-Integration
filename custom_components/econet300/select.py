"""Select for Econet300."""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .common_functions import camel_to_snake
from .const import (
    DOMAIN,
    ENTITY_CATEGORY,
    ENTITY_ICON,
    ENTITY_PRECISION,
    ENTITY_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    SERVICE_API,
    SERVICE_COORDINATOR,
    SELECT_MAP_KEY, SELECT_MAP_KEY_TO_OPTIONS_MAP,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class EconetSelectEntityDescription(SelectEntityDescription):
    """Describes ecoNET select entity."""

    process_val: Callable[[Any], Any] = lambda x: x


class EconetSelect(EconetEntity, SelectEntity):
    """Represents an ecoNET select entity."""

    entity_description: EconetSelectEntityDescription

    def __init__(
        self,
        entity_description: EconetSelectEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET select entity."""
        self.entity_description = entity_description
        self.api = api
        self._attr_native_value = None
        super().__init__(coordinator)

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        param_value = SELECT_MAP_KEY_TO_OPTIONS_MAP[self.entity_description.key][option]
        if param_value is None:
            _LOGGER.warning(
                "Missing param_value for option %s in entity with key %s - unable to proceed with select", option,
                self.entity_description.key
            )
            return

        _LOGGER.debug(
            "Setting param %s to value %s",
            self.entity_description.key,
            str(option)
        )

        await self.api.set_param(self.entity_description.key, int(param_value))


def create_select_entity_description(key: str) -> EconetSelectEntityDescription:
    """Create ecoNET300 select entity based on supplied key."""
    _LOGGER.debug("Creating select entity description for key: %s", key)
    entity_description = EconetSelectEntityDescription(
        key=key,
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        entity_category=ENTITY_CATEGORY.get(key, None),
        translation_key=camel_to_snake(key),
        icon=ENTITY_ICON.get(key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),
    )
    _LOGGER.debug("Created select entity description: %s", entity_description)
    return entity_description


def create_controller_selects(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[EconetSelect]:
    """Create controller select entities."""
    entities: list[EconetSelect] = []

    # Get the system and regular parameters from the coordinator
    data_regParams = coordinator.data.get("regParams", {})
    data_sysParams = coordinator.data.get("sysParams", {})

    # Extract the controllerID from sysParams
    controller_id = data_sysParams.get("controllerID", None)

    # Determine the keys to use based on the controllerID
    select_keys = SELECT_MAP_KEY.get(controller_id, SELECT_MAP_KEY["_default"])
    _LOGGER.info(
        "Using select keys for controllerID '%s': %s",
        controller_id if controller_id else "None (default)",
        select_keys,
    )

    # Iterate through the selected keys and create selects if valid data is found
    for data_key in select_keys:
        _LOGGER.debug(
            "Processing entity select data_key: %s from regParams & sysParams", data_key
        )
        if data_key in data_regParams:
            entity = EconetSelect(
                create_select_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug(
                "Created and appended select entity from regParams: %s", entity
            )
        elif data_key in data_sysParams:
            if data_sysParams.get(data_key) is None:
                _LOGGER.warning(
                    "%s in sysParams is null, select will not be created.", data_key
                )
                continue
            entity = EconetSelect(
                create_select_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug(
                "Created and appended select entity from sysParams: %s", entity
            )
        else:
            _LOGGER.warning(
                "Key: %s is not mapped in regParams or sysParams, select entity will not be added.",
                data_key,
            )
    _LOGGER.info("Total select entities created: %d", len(entities))
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the select platform."""

    def gather_entities(
        coordinator: EconetDataCoordinator, api: Econet300Api
    ) -> list[EconetSelect]:
        """Collect all select entities."""
        entities = []
        _LOGGER.info("Starting entity collection for selects...")

        # Gather selects dynamically based on the controller
        controller_selects = create_controller_selects(coordinator, api)
        _LOGGER.info("Collected %d controller selects", len(controller_selects))
        entities.extend(controller_selects)

        _LOGGER.info("Total entities collected: %d", len(entities))
        return entities

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    # Collect entities synchronously
    entities = await hass.async_add_executor_job(gather_entities, coordinator, api)

    # Add entities to Home Assistant
    async_add_entities(entities)
    _LOGGER.info("Select entities successfully added to Home Assistant")
    return True
