#!/bin/bash
#
# Cold-start runner for the GitHub contributions display.
#
# From a freshly booted (or freshly cloned) Raspberry Pi this will:
#   1. Ensure SPI is enabled (rebooting once if it had to turn it on).
#   2. Create the Python virtual environment if it doesn't exist.
#   3. Install the unicornhatmini library into it if needed.
#   4. Run the contribution graph on the Unicorn HAT Mini.
#
# Usage:
#   ./run-github-contributions.sh <github-username>
#
set -euo pipefail

# Default username (override with the first argument).
USERNAME="${1:-leetosc}"

VENV="$HOME/.venvs/unicorn"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- 1. Make sure SPI is enabled --------------------------------------------
if ! ls /dev/spidev* >/dev/null 2>&1; then
    echo "SPI device not found, enabling SPI..."
    sudo raspi-config nonint do_spi 0
    echo
    echo "SPI has been enabled but a reboot is required for it to take effect."
    echo "Please reboot, then run this script again:"
    echo "    sudo reboot"
    exit 0
fi

# --- 2. Create the virtual environment if missing ---------------------------
if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment at $VENV..."
    python3 -m venv --system-site-packages "$VENV"
fi

# Activate it for the rest of the script.
# shellcheck disable=SC1091
source "$VENV/bin/activate"

# --- 3. Install the library if it isn't already there -----------------------
if ! python3 -c "import unicornhatmini" >/dev/null 2>&1; then
    echo "Installing unicornhatmini..."
    pip install --quiet unicornhatmini
fi

# --- 3b. Install this repo's patched library module -------------------------
# The PyPI release (0.0.2) doesn't run on current Raspberry Pi OS as shipped.
# This repo's library/ contains the working version, so copy it over whatever
# pip installed. (Note: this still requires GPIO 7/8 to be freed from the
# kernel SPI driver via config.txt, see the README.)
INSTALLED_DIR="$(python3 -c 'import unicornhatmini, os; print(os.path.dirname(unicornhatmini.__file__))')"
REPO_MODULE="$SCRIPT_DIR/../library/unicornhatmini/__init__.py"
if [ -f "$REPO_MODULE" ] && ! cmp -s "$REPO_MODULE" "$INSTALLED_DIR/__init__.py"; then
    echo "Installing patched unicornhatmini module into the venv..."
    cp "$REPO_MODULE" "$INSTALLED_DIR/__init__.py"
fi

# --- 4. Run the display -----------------------------------------------------
echo "Starting GitHub contributions display for '$USERNAME'..."
exec python3 "$SCRIPT_DIR/github-contributions.py" "$USERNAME"
