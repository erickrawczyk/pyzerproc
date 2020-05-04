"""Main module."""
import logging

_LOGGER = logging.getLogger(__name__)


class Light():
    """Represents one connected light"""

    def __init__(self, address):
        self.address = address
        self.adapter = None
        self.device = None

    def connect(self):
        """Connect to this light"""
        import pygatt

        _LOGGER.info("Connecting to %s", self.address)

        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start(reset_on_start=False)
        self.device = self.adapter.connect(self.address)

        _LOGGER.debug("Connected to %s", self.address)

    def disconnect(self):
        """Connect to this light"""
        if self.adapter:
            self.adapter.stop()
            self.adapter = None
            self.device = None

    def turn_on(self):
        """Turn on the light"""
        _LOGGER.info("Turning on %s", self.address)
        self._write("0000ffe9-0000-1000-8000-00805f9b34fb", b'\xCC\x23\x33')
        _LOGGER.debug("Turned on %s", self.address)

    def turn_off(self):
        """Turn off the light"""
        _LOGGER.info("Turning off %s", self.address)
        self._write("0000ffe9-0000-1000-8000-00805f9b34fb", b'\xCC\x24\x33')
        _LOGGER.debug("Turned off %s", self.address)

    def set_color(self, r, g, b):
        """Set the color of the light

        Accepts red, green, and blue values from 0-255
        """
        for value in (r, g, b):
            if not 0 <= value <= 255:
                raise ValueError(
                    "Value {} is outside the valid range of 0-255")

        _LOGGER.info("Changing color of %s to #%x%x%x", self.address, r, g, b)

        # Normalize to 0-31, the supported range of these lights
        r = int(r * 31 / 255)
        g = int(g * 31 / 255)
        b = int(b * 31 / 255)
        color_string = "{:c}{:c}{:c}".format(r, g, b).encode()

        value = b'\x56' + color_string + b'\x00\xF0\xAA'
        self._write("0000ffe9-0000-1000-8000-00805f9b34fb", value)
        _LOGGER.debug("Changed color of %s", self.address)

    def _write(self, uuid, value):
        """Internal method to write to the device"""
        if not self.device:
            raise RuntimeError(
                "Light {} is not connected".format(self.address))

        _LOGGER.debug("Writing 0x%s to characteristic %s", value.hex(), uuid)
        self.device.char_write(uuid, value)
        _LOGGER.debug("Wrote 0x%s to characteristic %s", value.hex(), uuid)
