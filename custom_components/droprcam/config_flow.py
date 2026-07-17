"""Config flow for Droprcam."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_IP_ADDRESS

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
    }
)

class DroprcamConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Droprcam."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            # We could do a test connection here using aiohttp to `http://<ip>:8080`,
            # but for simplicity we'll just create the entry.
            ip_address = user_input[CONF_IP_ADDRESS]
            return self.async_create_entry(title=f"Droprcam ({ip_address})", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
