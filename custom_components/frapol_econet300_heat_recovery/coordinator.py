"""DataUpdateCoordinator for frapol_econet300_heat_recovery."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    FrapolEconet300ApiClientAuthenticationError,
    FrapolEconet300ApiClientError,
)

if TYPE_CHECKING:
    from .data import FrapolEconet300ConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class FrapolEconet300DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: FrapolEconet300ConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            await self.config_entry.runtime_data.client.refresh_state()
            return await self.config_entry.runtime_data.client.get_all_data()
        except FrapolEconet300ApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except FrapolEconet300ApiClientError as exception:
            raise UpdateFailed(exception) from exception
