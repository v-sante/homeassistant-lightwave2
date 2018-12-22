#light
import custom_components.lightwave2 as lightwave2

from custom_components.lightwave2 import LIGHTWAVE_LINK2
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light)
from homeassistant.const import CONF_NAME
import logging

_LOGGER = logging.getLogger(__name__)
DEPENDENCIES = ['lightwave2']

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Find and return LightWave switches."""

    lights = []
    link = hass.data[LIGHTWAVE_LINK2]

    for device_id, name in link.get_lights():
        lights.append(LWRF2Light(name, device_id, link))
    _LOGGER.debug(link.get_lights())
    async_add_entities(lights)


class LWRF2Light(Light):
    """Representation of a LightWaveRF light."""

    def __init__(self, name, device_id, link):
        self._name = name
        self._device_id = device_id
        self._lwlink = link
        self._state = self._lwlink.get_device_by_id(self._device_id).features["switch"][1]
        self._brightness = int(self._lwlink.get_device_by_id(self._device_id).features["dimLevel"][1] / 100 * 255)


    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS
        
    @property
    def should_poll(self):
        return True
        
    async def async_update(self):
        self._state = self._lwlink.get_device_by_id(self._device_id).features["switch"][1]
        self._brightness = int(self._lwlink.get_device_by_id(self._device_id).features["dimLevel"][1] / 100 * 255)

    @property
    def name(self):
        """Lightwave switch name."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the group lights."""
        return self._brightness
        
    @property
    def unique_id(self):
        return self._device_id
        
    @property
    def is_on(self):
        """Lightwave switch is on state."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the LightWave switch on."""
        self._state = True
        
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
        
        await self._lwlink.async_set_brightness_by_device_id(self._device_id, int(self._brightness/255*100))
        await self._lwlink.async_turn_on_by_device_id(self._device_id)
        
        self.async_schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the LightWave switch off."""
        self._state = False
        await self._lwlink.async_turn_off_by_device_id(self._device_id)
        self.async_schedule_update_ha_state()