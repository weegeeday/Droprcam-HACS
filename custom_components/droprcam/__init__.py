"""The Droprcam component."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_IP_ADDRESS, CONF_RTSP_URL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CAMERA, Platform.SWITCH, Platform.LIGHT]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Droprcam from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    ip_address = entry.data[CONF_IP_ADDRESS]
    rtsp_url = entry.data.get(CONF_RTSP_URL)
    if not rtsp_url:
        rtsp_url = f"rtsp://{ip_address}/stream1"

    _LOGGER.debug(f"Setting up Droprcam with IP: {ip_address}")

    # For this simple integration, we don't have a complex client connection to establish
    # at the component level, so we just pass the IP down to the platforms.
    hass.data[DOMAIN][entry.entry_id] = {
        "ip_address": ip_address,
        "rtsp_url": rtsp_url,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
