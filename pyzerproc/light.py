"""Device class"""
from binascii import hexlify
import logging
import math
import queue

from .exceptions import ZerprocException

_LOGGER = logging.getLogger(__name__)

CHARACTERISTIC = "8d96b002-0002-64c2-0001-9acc4838521c"
ON = '\x02'
OFF = '\x32'

class Light():
    """Represents one connected light"""

    def __init__(self, address, name=None):
        self.address = address
        self.name = name
        self.adapter = None
        self.device = None

    def connect(self, auto_reconnect=False):
        """Connect to this light"""
        import pygatt

        _LOGGER.info("Connecting to %s", self.address)

        self.adapter = pygatt.GATTToolBackend()
        try:
            self.adapter.start(reset_on_start=False)
            self.device = self.adapter.connect(
                self.address, auto_reconnect=auto_reconnect, timeout=10, address_type=pygatt.BLEAddressType.random)

        except pygatt.BLEError as ex:
            raise ZerprocException() from ex

        _LOGGER.debug("Connected to %s", self.address)

    def disconnect(self):
        """Connect to this light"""
        import pygatt

        if self.adapter:
            try:
                self.adapter.stop()
            except pygatt.BLEError as ex:
                raise ZerprocException() from ex
            self.adapter = None
            self.device = None

    def turn_on(self):
        """Turn on the light"""
        _LOGGER.info("Turning on %s", self.address)
        state = self.get_state()
        (r, g, b) = state.color
        color_string = self._rgb_to_color_string(r, g, b);
        value = bytes(ON, encoding='utf-8') + color_string;
        self._write(CHARACTERISTIC, value)
        _LOGGER.debug("Turned on %s", self.address)

    def turn_off(self):
        """Turn off the light"""
        state = self.get_state()
        (r, g, b) = state.color
        color_string = self._rgb_to_color_string(r, g, b);
        value = bytes(OFF, encoding='utf-8') + color_string;
        self._write(CHARACTERISTIC, value);
        _LOGGER.debug("Turned off %s", self.address)

    def set_color(self, r, g, b):
        """Set the color of the light

        Accepts red, green, and blue values from 0-255
        """
        _LOGGER.info("Changing color of %s to #%02x%02x%02x",
                     self.address, r, g, b)

        if r == 0 and g == 0 and b == 0:
            self.turn_off()
        else:
            color_string = self._rgb_to_color_string(r, g, b);

            value = bytes(ON, encoding='utf-8') + color_string
            print(value);
            self._write(CHARACTERISTIC, value)
            _LOGGER.debug("Changed color of %s", self.address)

    def get_state(self):
        """Get the current state of the light"""
        # Clear the queue if a value is somehow left over
        char_value = self.device.char_read(CHARACTERISTIC)

        on_off_value = int(char_value[0])

        r = int(char_value[1])
        g = int(char_value[2])
        b = int(char_value[3])
        y = int(char_value[4])

        if on_off_value == ON:
            is_on = True
        elif on_off_value == OFF:
            is_on = False
        else:
            is_on = None

        state = LightState(is_on, (r, g, b))

        _LOGGER.info("Got state of %s: %s", self.address, state)

        return state


    def _rgb_to_color_string(self, r, g, b, y =0):
        for value in (r, g, b, y):
            if not 0 <= value <= 255:
                raise ValueError(
                    "Value {} is outside the valid range of 0-255")

        if r == 255 and g == 255 and b == 255:
            y = 255

        return bytes((r, g, b, y));

    def _write(self, uuid, value):
        """Internal method to write to the device"""
        import pygatt

        if not self.device:
            raise RuntimeError(
                "Light {} is not connected".format(self.address))

        _LOGGER.debug("Writing 0x%s to characteristic %s", value.hex(), uuid)
        try:
            self.device.char_write(uuid, value)
        except pygatt.BLEError as ex:
            raise ZerprocException() from ex
        _LOGGER.debug("Wrote 0x%s to characteristic %s", value.hex(), uuid)


class LightState():
    """Represents the current state of the light"""
    __slots__ = 'is_on', 'color',

    def __init__(self, is_on, color):
        """Create the state object"""
        self.is_on = is_on
        self.color = color

    def __repr__(self):
        """Return a string representation of the state object"""
        return "<LightState is_on='{}' color='{}'>".format(
            self.is_on, self.color)

    def __eq__(self, other):
        """Check for equality."""
        return self.is_on == other.is_on and self.color == other.color
