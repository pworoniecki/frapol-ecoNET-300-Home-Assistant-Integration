"""Constants for frapol_econet300_heat_recovery."""

from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

NAME: Final = "Frapol ecoNET300 Heat Recovery"
DOMAIN: Final = "frapol_econet300_heat_recovery"
ISSUE_URL: Final = "https://github.com/pworoniecki/frapol-ecoNET-300-Home-Assistant-Integration/issues"

CONFIG_ENTRY_TITLE = NAME
CONFIG_ENTRY_DESCRIPTION = NAME

API_ENDPOINT_PREFIX: Final = "/econet"
API_REG_PARAMS_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/regParams"
API_SYS_PARAMS_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/sysParams"
API_EDIT_PARAMS_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/editParams"
API_SET_PARAM_ENDPOINT: Final = f"{API_ENDPOINT_PREFIX}/newParam"
API_SET_PARAM_ENDPOINT_NAME_QUERY_PARAM: Final = "newParamName"
API_SET_PARAM_ENDPOINT_VALUE_QUERY_PARAM: Final = "newParamValue"

API_REG_PARAM_CURRENT_SUPPLY_FAN_SPEED: Final = "REKcurSupFanSpeed"
API_REG_PARAM_CURRENT_EXTRACT_FAN_SPEED: Final = "REKcurExhFanSpeed"
API_REG_PARAM_CURRENT_MAIN_MODE: Final = "REKWS1"
API_REG_PARAM_CURRENT_TEMPORARY_MODE: Final = "REKWS4"
API_REG_PARAM_CURRENT_LEADING_TEMPERATURE: Final = "REKcurExtTemp"
API_REG_PARAM_CURRENT_SET_TEMPERATURE: Final = "REKcurSetPoint"
API_REG_PARAM_CURRENT_SUPPLY_TEMPERATURE: Final = "REKcurSupTemp"
API_REG_PARAM_CURRENT_INTAKE_TEMPERATURE: Final = "REKcurIntTemp"
API_REG_PARAM_CURRENT_EXTRACT_TEMPERATURE: Final = "REKcurExtTemp"
API_REG_PARAM_CURRENT_EXHAUST_TEMPERATURE: Final = "REKcuExhTemp"

API_REG_PARAM_CURRENT_MAIN_MODE_MAPPING_VALUE_TO_NAME: dict = {
    0: "off",
    3: "mode1",
    4: "mode2",
    5: "mode3",
    6: "pause",
    7: "mode4",
}
API_REG_PARAM_CURRENT_TEMP_MODE_MAPPING_VALUE_TO_NAME: dict = {
    0: "off",
    1: "exit",
    2: "party",
    4: "ventilation",
}

API_PARAM_UNIT_MAPPING: dict = {
    0: "",
    1: "°C",
    2: "s",
    3: "min",
    4: "h",
    5: "d",
    6: "%",
    7: "Pa",
    8: "kPa",
    9: "bar",
    10: "kg",
    11: "kg/h",
    12: "kcal/kg",
    13: "kW",
    14: "kWh/kg",
    15: "RPM",
    16: "g",
    31: "",
    61: "l/min",
    62: "kWh",
    63: "Wh",
    64: "kWh",
    65: "kW",
    67: 'kg/m3',
    68: 'J/(kg K)',
    69: 'ms',
    70: 'Hz',
    71: 'm3/h',
    72: 'K',
    73: 'J',
    74: 'ppm',
    75: 'd',
    76: 'L'
}
