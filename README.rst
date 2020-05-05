=========
pyzerproc
=========


.. image:: https://img.shields.io/pypi/v/pyzerproc.svg
        :target: https://pypi.python.org/pypi/pyzerproc

.. image:: https://img.shields.io/travis/emlove/pyzerproc.svg
        :target: https://travis-ci.com/emlove/pyzerproc

.. image:: https://coveralls.io/repos/emlove/pyzerproc/badge.svg
        :target: https://coveralls.io/r/emlove/pyzerproc



Library to control Zerproc Bluetooth LED smart string lights

* Free software: Apache Software License 2.0

Command line usage
------------------
pyzerproc ships with a command line tool that exposes the features of the library.

.. code-block:: console

    $ pyzerproc turn-on AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Turning on AA:BB:CC:00:11:22

    $ pyzerproc turn-off AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Turning off AA:BB:CC:00:11:22

    $ pyzerproc set-color AA:BB:CC:00:11:22 ff0000
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Changing color of AA:BB:CC:00:11:22 to #ff0000

    $ pyzerproc set-color AA:BB:CC:00:11:22 00ff00
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Changing color of AA:BB:CC:00:11:22 to #00ff00

Usage
-----

Turn a light on and off

.. code-block:: python

    import pyzerproc
    import time

    address = "AA:BB:CC:00:11:22"

    light = pyzerproc.Light(address)

    try:
        light.connect()
        light.turn_on()

        time.sleep(5)

        light.turn_off()
    finally:
        light.disconnect()


Change the light color

.. code-block:: python

    import pyzerproc
    import time

    address = "AA:BB:CC:00:11:22"

    light = pyzerproc.Light(address)

    try:
        light.connect()

        while True:
            light.set_color(255, 0, 0) # Red
            time.sleep(1)
            light.set_color(0, 255, 0) # Green
            time.sleep(1)
    finally:
        light.disconnect()


Features
--------

* Turn lights on and off
* Set light color

Changelog
---------
0.0.1 (2020-05-04)
~~~~~~~~~~~~~~~~~~
- Initial release

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
