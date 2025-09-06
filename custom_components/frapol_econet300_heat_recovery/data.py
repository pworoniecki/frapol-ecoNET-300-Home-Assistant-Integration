"""Custom types for frapol_econet300_heat_recovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import FrapolEconet300ApiClient
    from .coordinator import FrapolEconet300DataUpdateCoordinator


type FrapolEconet300ConfigEntry = ConfigEntry[FrapolEconet300Data]


@dataclass
class FrapolEconet300Data:
    """Data for the Blueprint integration."""

    client: FrapolEconet300ApiClient
    coordinator: FrapolEconet300DataUpdateCoordinator
    integration: Integration
