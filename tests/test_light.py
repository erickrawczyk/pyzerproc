#!/usr/bin/env python
import pytest

from pyzerproc import Light


def test_connect_disconnect(adapter):
    """Test the CLI."""
    light = Light("00:11:22")
    light.connect()

    adapter.start.assert_called_with(reset_on_start=False)
    adapter.connect.assert_called_with("00:11:22")

    light.disconnect()

    adapter.stop.assert_called_once()

    # Duplicate disconnect shouldn't call stop again
    light.disconnect()

    adapter.stop.assert_called_once()


def test_turn_on_not_connected(device):
    """Test the CLI."""
    light = Light("00:11:22")

    with pytest.raises(RuntimeError):
        light.turn_on()


def test_turn_on(device):
    """Test the CLI."""
    light = Light("00:11:22")
    light.connect()

    light.turn_on()

    device.char_write.assert_called_with(
        '0000ffe9-0000-1000-8000-00805f9b34fb', b'\xCC\x23\x33')


def test_turn_off(device):
    """Test the CLI."""
    light = Light("00:11:22")
    light.connect()

    light.turn_off()

    device.char_write.assert_called_with(
        '0000ffe9-0000-1000-8000-00805f9b34fb', b'\xCC\x24\x33')


def test_set_color(device):
    """Test the CLI."""
    light = Light("00:11:22")
    light.connect()

    light.set_color(0, 0, 0)
    device.char_write.assert_called_with(
        '0000ffe9-0000-1000-8000-00805f9b34fb',
        b'\x56\x00\x00\x00\x00\xF0\xAA')

    light.set_color(255, 255, 255)
    device.char_write.assert_called_with(
        '0000ffe9-0000-1000-8000-00805f9b34fb',
        b'\x56\x1F\x1F\x1F\x00\xF0\xAA')

    light.set_color(64, 128, 192)
    device.char_write.assert_called_with(
        '0000ffe9-0000-1000-8000-00805f9b34fb',
        b'\x56\x07\x0F\x17\x00\xF0\xAA')

    with pytest.raises(ValueError):
        light.set_color(999, 999, 999)
