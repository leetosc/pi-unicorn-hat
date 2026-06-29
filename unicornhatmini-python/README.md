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
On top of that, the library bit-bangs its two chip-select lines (GPIO 8 and
GPIO 7) while the kernel SPI driver also claims those pins, and the lgpio-backed
`RPi.GPIO` on current Raspberry Pi OS enforces exclusive pin ownership — so out
of the box you hit `lgpio.error: 'GPIO busy'` and/or only half the board lights.

The full procedure that works on a current release (tested on a Pi Zero /
`armv6l`, Python 3.13) is:

**1. Enable SPI and free GPIO 7/8 for the library, then reboot.** Enabling SPI
gives you the `/dev/spidev*` devices; the `spi0-2cs` overlay moves the kernel's
chip-select pins to two unused GPIOs (25/26) so the library can drive GPIO 7/8
itself. Both `/dev/spidev0.0` and `/dev/spidev0.1` remain available.

```bash
sudo raspi-config nonint do_spi 0

CONFIG=/boot/firmware/config.txt
[ -f "$CONFIG" ] || CONFIG=/boot/config.txt
grep -q "spi0-2cs" "$CONFIG" || \
  echo "dtoverlay=spi0-2cs,cs0_pin=25,cs1_pin=26" | sudo tee -a "$CONFIG"

sudo reboot
```

After rebooting, `ls /dev/spidev*` should list `/dev/spidev0.0` and
`/dev/spidev0.1`.

**2. Create a virtual environment and install the library.** Use
`--system-site-packages` so the venv can see the system `spidev`, `gpiozero`
and `RPi.GPIO` libraries needed to talk to the hardware:

```bash
python3 -m venv --system-site-packages ~/.venvs/unicorn
source ~/.venvs/unicorn/bin/activate
pip install unicornhatmini
```

**3. Install this repo's library module over the PyPI one.** This repo's
`library/unicornhatmini/__init__.py` is the version that works with the overlay
above. Copy it over whatever pip installed:

```bash
cp library/unicornhatmini/__init__.py \
  "$(python3 -c 'import unicornhatmini, os; print(os.path.dirname(unicornhatmini.__file__))')/__init__.py"
```

(We copy the single module rather than `pip install ./library` because the
old `setup.py` fails to build under modern setuptools — `No module named
'pkg_resources'`.)

**4. Run an example** with the environment active (do **not** use `sudo`, it
bypasses the venv):

```bash
python3 examples/github-contributions.py <github-username>
```

Reactivate the environment in future sessions with
`source ~/.venvs/unicorn/bin/activate`.

### Cold-start helper

`examples/run-github-contributions.sh` automates the runtime side of the above
(enables SPI if needed, creates the venv, installs the library, copies this
repo's library module into it, then runs the display) so you can launch it with
a single command:

```bash
./examples/run-github-contributions.sh <github-username>
```

The one piece it can't do for you is the `spi0-2cs` overlay from step 1, since
that edits `config.txt` and needs a reboot — do that once by hand first.

### System-wide alternative

If you'd rather install system-wide and accept the risk of clashing with
apt-managed packages, you can override the protection (you'll still need the
step 1 overlay and the step 3 module copy):

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

