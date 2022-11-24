"""
Custom integration to integrate smartenergylab.pt with Home Assistant.

For more details about this integration, please refer to
https://github.com/dgomes/ha_smartenergylab
"""
import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta

import aiohttp
import async_timeout
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN

from .const import CONF_SENSORS, DEFAULT_TIMEOUT, UPDATE_INTERVAL

_LOGGER: logging.Logger = logging.getLogger(__package__)

DEVICE_CLASS_2_PARAMETER_KEY = {
    "energy": "total",
    "power": "power",
    "reactive_power": "reactive_power",
    "power_factor": "pf",
    "voltage": "voltage",
    "current": "current",
}


class SELRecorder:
    """Records selected entities states to Smart Energy Lab backend."""

    def __init__(self, client_id, hass: HomeAssistant, entry):
        self.client_id = client_id
        self.hass = hass

        sensors = (
            entry.options.get(CONF_SENSORS)
            if entry.options
            else entry.data.get(CONF_SENSORS)
        )
        self.sensors = {
            sensor: int(hashlib.shake_128(sensor.encode("utf-8")).hexdigest(2), base=16)
            for sensor in sensors
        }

        _LOGGER.info(
            "Sending SEL information on: %s every %s seconds",
            self.sensors,
            UPDATE_INTERVAL,
        )
        self.cancel = async_track_time_interval(
            self.hass, self.update, timedelta(seconds=UPDATE_INTERVAL)
        )

    @callback
    async def update(self, now: Event):
        """Periodically send data to SEL backend."""

        session = async_get_clientsession(self.hass)

        message = []
        now_str = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
        for sensor, sensor_hash in self.sensors.items():

            state = self.hass.states.get(sensor)
            if state and state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN, None):
                message.append(
                    {
                        "collection_date": now_str,
                        "local_id": sensor_hash,
                        "message_type": DEVICE_CLASS_2_PARAMETER_KEY[
                            state.attributes["device_class"]
                        ],
                        "val": float(state.state) * 1000
                        if state.attributes["unit_of_measurement"].startswith("k")
                        else state.state,
                    }
                )

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                response = await session.post(
                    f"https://odc.smartenergylab.pt/log/{self.client_id}",
                    json=message,
                    allow_redirects=True,
                )

        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            _LOGGER.error("Timeout sending report to SEL: %s", error)
            return

        response_text = await response.text()

        _LOGGER.debug("Sent: %s", json.dumps(message))
        _LOGGER.debug("Received (%s): %s", response.status, response_text)
