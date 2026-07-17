"""Config flow for Droprcam."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_IP_ADDRESS, CONF_RTSP_URL

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Optional(CONF_RTSP_URL, default=""): str,
    }
)

class DroprcamOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_url = self.config_entry.options.get(
            CONF_RTSP_URL, self.config_entry.data.get(CONF_RTSP_URL, "")
        )

        options_schema = vol.Schema(
            {
                vol.Optional(CONF_RTSP_URL, default=current_url): str,
            }
        )
        return self.async_show_form(step_id="init", data_schema=options_schema)

class DroprcamConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Droprcam."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return DroprcamOptionsFlowHandler(config_entry)

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
