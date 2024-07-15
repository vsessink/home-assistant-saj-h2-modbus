"""SAJ Modbus services."""

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.const import ATTR_DEVICE_ID
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import (
    device_registry as dr,
    config_validation as cv
)

from .const import DOMAIN as SAJ_H2_DOMAIN

ATTR_MAXPOWER = "maxpower"

SERVICE_SET_MAXPOWER = "set_maxpower"

SERVICE_SET_MAXPOWER = vol.All(
    vol.Schema({
        vol.Required(ATTR_DEVICE_ID): str,
        vol.Optional(ATTR_DATETIME): cv.maxpower,
    })
)

SUPPORTED_SERVICES = (SERVICE_SET_MAXPOWER,)

SERVICE_TO_SCHEMA = {
    SERVICE_SET_MAXPOWER: SERVICE_SET_MAXPOWER_SCHEMA,
}


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for SAJ H2 Modbus integration."""

    services = {
        SERVICE_SET_DATE_TIME: async_set_maxpower,
    }

    async def async_call_service(service_call: ServiceCall) -> None:
        """Call correct SAJ H2 Modbus service."""
        await services[service_call.service](hass, service_call.data)

    for service in SUPPORTED_SERVICES:
        hass.services.async_register(
            SAJ_H2_DOMAIN,
            service,
            async_call_service,
            schema=SERVICE_TO_SCHEMA.get(service),
        )


@callback
def async_unload_services(hass: HomeAssistant) -> None:
    """Unload SAJ H2 Modbus services."""
    for service in SUPPORTED_SERVICES:
        hass.services.async_remove(SAJ_H2_DOMAIN, service)


async def async_set_maxpower(hass: HomeAssistant, data: Mapping[str, Any]) -> None:
    """Set the maximum power on the inverter."""
    device_registry = dr.async_get(hass)
    device_entry = device_registry.async_get(data[ATTR_DEVICE_ID])

    hub = hass.data[SAJ_H2_DOMAIN][device_entry.name]["hub"]
    await hass.async_add_executor_job(
        hub.set_maxpower,
        data.get(ATTR_MAXPOWER, None)
    )
