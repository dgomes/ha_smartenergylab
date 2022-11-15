"""Adds config flow for SmartEnergyLab."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import CONF_CLIENT_ID, CONF_SENSORS, DOMAIN, NAME


class SmartEnergyLabFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for SmartEnergyLab."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title=NAME, data=user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_CLIENT_ID] = ""

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SmartEnergyLabOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_CLIENT_ID, default=user_input[CONF_CLIENT_ID]
                    ): str,
                    vol.Required(CONF_SENSORS): selector.selector(
                        {"entity": {"domain": "sensor", "multiple": True}},
                    ),
                }
            ),
            errors=self._errors,
        )


class SmartEnergyLabOptionsFlowHandler(config_entries.OptionsFlow):
    """SmartEnergyLab config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)
        if not self.options:
            self.options = dict(config_entry.data)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SENSORS, default=self.options[CONF_SENSORS]
                    ): selector.selector(
                        {"entity": {"domain": "sensor", "multiple": True}},
                    ),
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(title=NAME, data=self.options)
