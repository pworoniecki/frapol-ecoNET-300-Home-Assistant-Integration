"""Constants for frapol_econet300_heat_recovery."""

from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

NAME: Final = "Frapol ecoNET300 Heat Recovery"
DOMAIN: Final = "frapol_econet300_heat_recovery"
VERSION: Final = "0.0.0"
ISSUE_URL: Final = "https://github.com/pworoniecki/frapol-ecoNET-300-Home-Assistant-Integration/issues"

CONFIG_ENTRY_TITLE = "frapolEconet300HeatRecovery"
CONFIG_ENTRY_DESCRIPTION = NAME

API_ENDPOINT_PREFIX: Final = "/econet"
API_REG_PARAMS_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/regParams"
API_SYS_PARAMS_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/sysParams"
API_EDIT_PARAMS_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/editParams"
API_SET_PARAM_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/newParam"
API_SET_PARAM_ENDPOINT_NAME_QUERY_PARAM: Final = "newParamName"
API_SET_PARAM_ENDPOINT_VALUE_QUERY_PARAM: Final = "newParamValue"

API_REG_PARAM_CURRENT_FAN_SPEED = "REKcurSupFanSpeed"