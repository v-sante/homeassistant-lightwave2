from homeassistant.helpers.discovery import async_load_platform
from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD)
import logging

REQUIREMENTS = ['lightwave2==0.0.8']

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'lightwave2'
LIGHTWAVE_LINK2 = 'lightwave_link2'

async def async_setup(hass, config):
    """Your controller/hub specific code."""
    from lightwave2 import lightwave2
    
    email = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    
    
    link = lightwave2.LWLink2(email, password)
    await link.async_connect()
    hass.data[LIGHTWAVE_LINK2] = link
    await link.async_get_hierarchy()
    
    hass.async_create_task(async_load_platform(hass, 'switch', DOMAIN, None, config))
    hass.async_create_task(async_load_platform(hass, 'light', DOMAIN, None, config))
    return True