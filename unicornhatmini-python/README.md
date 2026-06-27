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
The full procedure that works on a current release (tested on a Pi Zero /
`armv6l`, Python 3.13) is:

**1. Enable SPI and reboot.** The library needs the `/dev/spidev*` devices,
which only appear after a reboot:

```bash
sudo raspi-config nonint do_spi 0
sudo reboot
```

**2. Create a virtual environment and install the library.** Use
`--system-site-packages` so the venv can see the system `spidev`, `gpiozero`
and `RPi.GPIO` libraries needed to talk to the hardware:

```bash
python3 -m venv --system-site-packages ~/.venvs/unicorn
source ~/.venvs/unicorn/bin/activate
pip install unicornhatmini
```

**3. Apply the `GPIO busy` fix.** The PyPI release (0.0.2) bit-bangs the SPI
chip-select pins with `RPi.GPIO` while the kernel SPI driver already owns them.
On current Raspberry Pi OS, `RPi.GPIO` is a shim over `lgpio`, which enforces
exclusive pin ownership, so the unpatched library crashes with
`lgpio.error: 'GPIO busy'`. This repo's `library/` contains a patched module
that lets the SPI hardware drive chip-select instead. Copy it over the
installed version:

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
(enables SPI if needed, creates the venv, installs the library, then runs the
display) so you can launch it with a single command:

```bash
./examples/run-github-contributions.sh <github-username>
```

### System-wide alternative

If you'd rather install system-wide and accept the risk of clashing with
apt-managed packages, you can override the protection (you'll still need the
step 3 `GPIO busy` fix):

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

