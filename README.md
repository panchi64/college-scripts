# Personal Scripts

A collection of automation scripts designed to solve everyday computing problems and improve quality of life. These scripts address various personal workflow inefficiencies and repetitive tasks that many of us encounter in our daily computer usage.

Feel free to use, modify, or draw inspiration from any of these scripts if you find them useful! 😄

## Index

### Python Scripts
- [Class Note Setup Script](#class-note-setup-script---setup-class-notepy) - Automated note file creation with date-based naming
- [Schedule Import Script](#schedule-import-script---add-schedule-to-calendarpy) - UPRM web portal schedule extraction to calendar format

### Bash Scripts
- [Bluetooth Fix Script](#bluetooth-fix-script---bluetooth_fixsh) - Bluetooth kept bugging out on PopOS! so I created this Intel Bluetooth USB power management fix

---

## Python Scripts

### Class Note Setup Script - `setup-class-note.py`

**Location:** `python/setup-class-note.py`

This script streamlines the process of creating organized note files. It prompts the user to select a directory and automatically generates a Markdown file with a standardized naming convention using the format `Date-Day-Year(-Index)`. If files with the same date already exist, an index number is appended to ensure uniqueness.

**Use Cases:**
- Daily journaling with consistent file naming
- Meeting notes organization
- Study session documentation
- Any time-stamped document creation

**Dependencies:**
Use `pip install [dependency name]` to install dependencies (try `pip3` if `pip` doesn't work):
- tkinter
- datetime

### Schedule Import Script - `add-schedule-to-calendar.py`

**Location:** `python/add-schedule-to-calendar.py`

This script automates the process of extracting schedule information from the UPRM (University of Puerto Rico - Mayaguez) web portal and converting it into a universal calendar format. Using Selenium for web scraping, it generates an `.ics` file that can be imported into any calendar application.

**Use Cases:**
- Importing class schedules to personal calendars
- Converting work schedules from company portals
- Migrating event data between different calendar systems
- Automating recurring schedule updates

**Privacy Note:** This application does not gather or store any personal information. Login credentials are handled locally and never transmitted or saved. Source code is available for verification.

**Dependencies:**
Use `pip install [dependency name]` to install dependencies (try `pip3` if `pip` doesn't work):
- selenium
- pytz
- os
- icalendar
- datetime
- dateutil
- pathlib

---

## Bash Scripts

### Bluetooth Fix Script - `bluetooth_fix.sh`

**Location:** `bash/bluetooth_fix.sh`

A comprehensive script that fixes common Intel Bluetooth USB power management issues, particularly for Intel AX200 and similar controllers. The script automatically detects Intel Bluetooth devices, fixes USB power management settings, restarts services, and creates persistent fixes that survive reboots.

**Use Cases:**
- Fixing Bluetooth connectivity issues on Linux systems
- Resolving Intel Bluetooth controller power management problems
- Automating Bluetooth service recovery
- Creating persistent fixes for recurring Bluetooth issues

**Features:**
- Automatic Intel Bluetooth device detection
- USB power management correction
- Bluetooth service restart automation
- Persistent udev rule creation
- Colored output with detailed status reporting
- Multiple operation modes (check-only, force, help)

**Usage:**
```bash
# Basic fix (requires sudo)
sudo ./bluetooth_fix.sh

# Check status only (no sudo required)
./bluetooth_fix.sh --check-only

# Force fix even if Bluetooth appears working
sudo ./bluetooth_fix.sh --force

# Show help
./bluetooth_fix.sh --help
```

**Dependencies:**
- systemctl (systemd)
- bluetoothctl (BlueZ)
- lsusb (usbutils)
- modprobe (kernel modules)
- udevadm (udev)

---

## Future Scripts

This repository will continue to grow with scripts that address various quality of life improvements.
