"""Device discovery code"""
import logging

from .light import Light
from .exceptions import ZerprocException

_LOGGER = logging.getLogger(__name__)


def discover(name ='KulerSky-', timeout=10):
    if not name:
        name = 'KulerSky-'

    """Returns nearby discovered lights."""
    _LOGGER.info("Starting scan for local devices")

    import pygatt
    adapter = pygatt.GATTToolBackend()

    lights = []
    try:
        adapter.start(reset_on_start=False)
        for device in adapter.scan(timeout=timeout):
            # Improvements welcome
            if device['name'] and device['name'].startswith(name):
                _LOGGER.info(
                    "Discovered %s: %s", device['address'], device['name'])
                lights.append(
                    Light(device['address'], device['name'].strip()))
    except pygatt.BLEError as ex:
        raise ZerprocException() from ex
    finally:
        try:
            adapter.stop()
        except pygatt.BLEError as ex:
            raise ZerprocException() from ex

    _LOGGER.info("Scan complete")
    return lights
