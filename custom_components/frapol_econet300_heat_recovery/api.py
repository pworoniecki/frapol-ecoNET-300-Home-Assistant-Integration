"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from .const import API_REG_PARAMS_ENDPOINT, API_SET_PARAM_ENDPOINT, API_SET_PARAM_ENDPOINT_NAME_QUERY_PARAM, API_SET_PARAM_ENDPOINT_VALUE_QUERY_PARAM, API_SYS_PARAMS_ENDPOINT, LOGGER


class FrapolEconet300ApiClientError(Exception):
    """Exception to indicate a general API error."""


class FrapolEconet300ApiClientCommunicationError(
    FrapolEconet300ApiClientError,
):
    """Exception to indicate a communication error."""


class FrapolEconet300ApiClientAuthenticationError(
    FrapolEconet300ApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise FrapolEconet300ApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class FrapolEconet300ApiClient:

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        LOGGER.debug(f"Initializing API with host: {host} and username: {username}")

        host_protocol_included = all(
            protocol not in host for protocol in ["http://", "https://"]
        )
        if not host_protocol_included:
            LOGGER.warning(f"Missing host protocol, assuming http")
            host = f"http://{host}"

        self._host = host
        self._session = session
        self._auth = aiohttp.BasicAuth(username, password)
        self._reg_params = None
        self._sys_params = None

    async def refresh_state(self):
        LOGGER.info("Refreshing state")
        self._reg_params = self._get_reg_params()
        self._sys_params = self._get_sys_params()
        LOGGER.info("State refreshed")

    async def get_all_data(self):
        if self._reg_params is None:
            LOGGER.info("Reg params not loaded yet, state will be refreshed")
            self.refresh_state()
        elif self._sys_params is None:
            LOGGER.info("Sys params not loaded yet, state will be refreshed")
            self.refresh_state()

        return {
            "regParams": self._reg_params,
            "sysParams:": self._sys_params
        }

    async def get_current_reg_param(self, param_name: str):
        if self._reg_params is None:
            LOGGER.info("Reg params not loaded yet, state will be refreshed")
            self.refresh_state()
        return self._reg_params["curr"][param_name]

    async def get_sys_param(self, param_name: str):
        if self._sys_params is None:
            LOGGER.info("Sys params not loaded yet, state will be refreshed")
            self.refresh_state()
        return self._sys_params[param_name]

    async def _get_reg_params(self) -> dict[str, Any] | None:
        LOGGER.info("Retrieving regParams")
        regParams = await self._api_wrapper(
            method="get",
            relative_url=API_REG_PARAMS_ENDPOINT,
        )
        LOGGER.info("regParams retrieved")
        LOGGER.debug("Retrieved regParams: %s", regParams)
        return regParams

    async def _get_sys_params(self) -> dict[str, Any] | None:
        LOGGER.info("Retrieving sysParams")
        sysParams = await self._api_wrapper(
            method="get",
            relative_url=API_SYS_PARAMS_ENDPOINT,
        )
        LOGGER.info("sysParams retrieved")
        LOGGER.debug("Retrieved sysParams: %s", sysParams)
        return sysParams

    async def _set_param(self, param_name: str, param_value: str):
        LOGGER.info("Updating param: %s to value: %s", param_name, param_value)
        response = await self._api_wrapper(
            method="get",
            relative_url=f"{API_SET_PARAM_ENDPOINT}?{API_SET_PARAM_ENDPOINT_NAME_QUERY_PARAM}={param_name}&{API_SET_PARAM_ENDPOINT_VALUE_QUERY_PARAM}={param_value}",
        )
        LOGGER.info("Param: %s updated to value: %s", param_name, param_value)
        return response

    # TODO add retries
    async def _api_wrapper(
        self,
        method: str,
        relative_url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        url = self._host + relative_url
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.requeauthst(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    auth=self._auth,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise FrapolEconet300ApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise FrapolEconet300ApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise FrapolEconet300ApiClientError(
                msg,
            ) from exception
