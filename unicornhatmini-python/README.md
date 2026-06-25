# Unicorn HAT Mini

[![Build Status](https://travis-ci.com/pimoroni/unicornhatmini-python.svg?branch=master)](https://travis-ci.com/pimoroni/unicornhatmini-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/unicornhatmini-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/unicornhatmini-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/unicornhatmini.svg)](https://pypi.python.org/pypi/unicornhatmini)
[![Python Versions](https://img.shields.io/pypi/pyversions/unicornhatmini.svg)](https://pypi.python.org/pypi/unicornhatmini)

# Requirements

You must enable SPI on your Raspberry Pi:

* Run: `sudo raspi-config nonint do_spi 0`

# Installing

## Raspberry Pi OS Bookworm (and newer)

Recent Raspberry Pi OS releases are "externally managed" (PEP 668), so
`sudo pip3 install ...` no longer works and the bundled `install.sh` will fail.
Use a virtual environment instead.

Create a virtual environment with access to the system GPIO/SPI packages and
install the library into it:

```bash
python3 -m venv --system-site-packages ~/.venvs/unicorn
source ~/.venvs/unicorn/bin/activate
pip install unicornhatmini
```

The `--system-site-packages` flag lets the venv see the system `spidev`,
`gpiozero` and `RPi.GPIO` libraries needed to talk to the hardware.

Run examples with the environment active (do **not** use `sudo`, it bypasses
the venv):

```bash
python3 examples/github-contributions.py <github-username>
```

Reactivate the environment in future sessions with
`source ~/.venvs/unicorn/bin/activate`.

If you'd rather install system-wide and accept the risk of clashing with
apt-managed packages, you can override the protection:

```bash
sudo pip3 install unicornhatmini --break-system-packages
```

## Raspberry Pi OS Bullseye (and older)

Stable library from PyPi:

* Just run `sudo pip3 install unicornhatmini`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/unicornhatmini-python`
* `cd unicornhatmini-python`
* `sudo ./install.sh`

