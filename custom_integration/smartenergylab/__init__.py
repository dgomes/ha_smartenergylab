"""
Custom integration to integrate smartenergylab.pt with Home Assistant.

For more details about this integration, please refer to
https://github.com/dgomes/ha_smartenergylab
"""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

from .const import CONF_CLIENT_ID, DOMAIN
from .recorder import SELRecorder

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    client_id = entry.data.get(CONF_CLIENT_ID)

    hass.data[DOMAIN][entry.entry_id] = SELRecorder(client_id, hass, entry)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    hass.data[DOMAIN][entry.entry_id].cancel()
    hass.data[DOMAIN].pop(entry.entry_id)

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
