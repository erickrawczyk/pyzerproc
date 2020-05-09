"""Device discovery code"""
import logging

import pygatt

from .light import Light

_LOGGER = logging.getLogger(__name__)


def discover(timeout=10):
    """Returns nearby discovered lights."""
    _LOGGER.info("Starting scan for local devices")

    adapter = pygatt.GATTToolBackend()
    adapter.start(reset_on_start=False)

    lights = []
    try:
        for device in adapter.scan(timeout=timeout):
            # Improvements welcome
            if device['name'] and device['name'].startswith('LEDBlue-'):
                _LOGGER.info(
                    "Discovered %s: %s", device['address'], device['name'])
                lights.append(
                    Light(device['address'], device['name'].strip()))
    finally:
        adapter.stop()

    _LOGGER.info("Scan complete")
    return lights
