"""Light platform for Droprcam."""
import logging
import aiohttp

from homeassistant.components.light import ColorMode, LightEntity, LightEntityFeature, ATTR_EFFECT
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, DEFAULT_HTTP_PORT

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Droprcam light from a config entry."""
    ip_address = hass.data[DOMAIN][entry.entry_id]["ip_address"]
    session = async_get_clientsession(hass)
    
    async_add_entities([DroprcamStatusLED(entry.entry_id, ip_address, session)])

class DroprcamStatusLED(LightEntity):
    """Representation of a Droprcam Status LED."""

    def __init__(self, entry_id: str, ip_address: str, session: aiohttp.ClientSession) -> None:
        """Initialize the light."""
        self._ip_address = ip_address
        self._session = session
        self._attr_unique_id = f"{entry_id}_status_led"
        self._attr_name = "Droprcam Status LED"
        self._is_on = False
        self._attr_supported_color_modes = {ColorMode.ONOFF}
        self._attr_color_mode = ColorMode.ONOFF
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._attr_effect_list = ["blue", "yellow", "red", "white"]
        self._attr_effect = "white"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=f"Droprcam ({ip_address})",
            manufacturer="Droprcam",
        )

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the light on."""
        effect = kwargs.get(ATTR_EFFECT, self._attr_effect)
        
        url = f"http://{self._ip_address}:{DEFAULT_HTTP_PORT}/led/{effect}"
        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    self._is_on = True
                    self._attr_effect = effect
                    self.async_write_ha_state()
                else:
                    _LOGGER.error("Failed to turn on LED, status: %s", response.status)
        except Exception as err:
            _LOGGER.error("Error communicating with camera: %s", err)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        url = f"http://{self._ip_address}:{DEFAULT_HTTP_PORT}/led/off"
        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    self._is_on = False
                    self.async_write_ha_state()
                else:
                    _LOGGER.error("Failed to turn off LED, status: %s", response.status)
        except Exception as err:
            _LOGGER.error("Error communicating with camera: %s", err)
