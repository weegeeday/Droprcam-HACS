"""Switch platform for Droprcam."""
import logging
import aiohttp

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, DEFAULT_HTTP_PORT

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Droprcam switch from a config entry."""
    ip_address = hass.data[DOMAIN][entry.entry_id]["ip_address"]
    session = async_get_clientsession(hass)
    
    async_add_entities([DroprcamNightVisionSwitch(entry.entry_id, ip_address, session)])

class DroprcamNightVisionSwitch(SwitchEntity):
    """Representation of a Droprcam Night Vision Switch."""

    def __init__(self, entry_id: str, ip_address: str, session: aiohttp.ClientSession) -> None:
        """Initialize the switch."""
        self._ip_address = ip_address
        self._session = session
        self._attr_unique_id = f"{entry_id}_night_vision"
        self._attr_name = "Droprcam Night Vision"
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        url = f"http://{self._ip_address}:{DEFAULT_HTTP_PORT}/night_vision/on"
        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    self._is_on = True
                    self.async_write_ha_state()
                else:
                    _LOGGER.error("Failed to turn on night vision, status: %s", response.status)
        except Exception as err:
            _LOGGER.error("Error communicating with camera: %s", err)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        url = f"http://{self._ip_address}:{DEFAULT_HTTP_PORT}/night_vision/off"
        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    self._is_on = False
                    self.async_write_ha_state()
                else:
                    _LOGGER.error("Failed to turn off night vision, status: %s", response.status)
        except Exception as err:
            _LOGGER.error("Error communicating with camera: %s", err)
