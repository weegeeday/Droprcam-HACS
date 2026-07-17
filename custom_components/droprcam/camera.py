"""Camera platform for Droprcam."""
import logging

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Droprcam camera from a config entry."""
    ip_address = hass.data[DOMAIN][entry.entry_id]["ip_address"]
    
    async_add_entities([DroprcamCamera(entry.entry_id, ip_address)])

class DroprcamCamera(Camera):
    """Representation of a Droprcam Camera."""

    def __init__(self, entry_id: str, ip_address: str) -> None:
        """Initialize the camera."""
        super().__init__()
        self._ip_address = ip_address
        self._attr_unique_id = f"{entry_id}_camera"
        self._attr_name = "Droprcam"
        # Provide the RTSP stream directly
        self._stream_source = f"rtsp://{ip_address}/stream1"

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        try:
            from homeassistant.components.camera import CameraEntityFeature
            return CameraEntityFeature.STREAM
        except ImportError:
            # Fallback for older HA versions
            from homeassistant.components.camera import SUPPORT_STREAM
            return SUPPORT_STREAM

    async def stream_source(self) -> str:
        """Return the source of the stream."""
        return self._stream_source
