#!/bin/bash

# Bluetooth Fix Script for Intel AX200 and similar controllers
# Fixes USB power management issues that cause Bluetooth to stop working

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if running as root for certain operations
check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script needs sudo privileges to fix Bluetooth issues."
        print_status "Please run: sudo $0"
        exit 1
    fi
}

# Function to detect Bluetooth issues
detect_bluetooth_issue() {
    print_status "Detecting Bluetooth issues..."

    # Check if Bluetooth service is running
    if ! systemctl is-active --quiet bluetooth; then
        print_warning "Bluetooth service is not running"
        return 1
    fi

    # Check if controller is available
    if bluetoothctl show &>/dev/null; then
        print_success "Bluetooth controller is available"
        return 0
    else
        print_error "No Bluetooth controller available"
        return 1
    fi
}

# Function to find Intel Bluetooth devices
find_intel_bluetooth() {
    print_status "Searching for Intel Bluetooth devices..."

    found_devices=()
    for dev in /sys/bus/usb/devices/*/; do
        if [[ -f "$dev/idVendor" ]] && [[ -f "$dev/idProduct" ]]; then
            vendor=$(cat "$dev/idVendor" 2>/dev/null)
            product=$(cat "$dev/idProduct" 2>/dev/null)

            # Check for Intel Bluetooth devices (8087 is Intel's USB vendor ID)
            if [[ "$vendor" == "8087" ]]; then
                device_name=$(lsusb -d "$vendor:$product" | head -1 | cut -d' ' -f7- || echo "Unknown Intel Device")
                if [[ "$device_name" == *"Bluetooth"* ]] || [[ "$product" == "0029" ]] || [[ "$product" == "0025" ]] || [[ "$product" == "0032" ]]; then
                    found_devices+=("$dev")
                    print_success "Found Intel Bluetooth device: $device_name at $dev"
                fi
            fi
        fi
    done

    if [ ${#found_devices[@]} -eq 0 ]; then
        print_warning "No Intel Bluetooth devices found"
        return 1
    fi

    return 0
}

# Function to fix USB power management
fix_usb_power_management() {
    print_status "Fixing USB power management for Intel Bluetooth devices..."

    fixed_any=false

    for dev in /sys/bus/usb/devices/*/; do
        if [[ -f "$dev/idVendor" ]] && [[ -f "$dev/idProduct" ]]; then
            vendor=$(cat "$dev/idVendor" 2>/dev/null)
            product=$(cat "$dev/idProduct" 2>/dev/null)

            if [[ "$vendor" == "8087" ]]; then
                device_name=$(lsusb -d "$vendor:$product" | head -1 | cut -d' ' -f7- || echo "Intel Device $product")

                if [[ "$device_name" == *"Bluetooth"* ]] || [[ "$product" == "0029" ]] || [[ "$product" == "0025" ]] || [[ "$product" == "0032" ]]; then
                    if [[ -f "$dev/power/control" ]]; then
                        current_power=$(cat "$dev/power/control" 2>/dev/null)
                        print_status "Device: $device_name"
                        print_status "Current power control: $current_power"

                        if [[ "$current_power" != "on" ]]; then
                            echo 'on' > "$dev/power/control"
                            print_success "Set power control to 'on' for $device_name"
                            fixed_any=true
                        else
                            print_status "Power control already set to 'on'"
                        fi
                    fi
                fi
            fi
        fi
    done

    if [ "$fixed_any" = true ]; then
        print_success "USB power management fixed"
    else
        print_status "No power management changes needed"
    fi
}

# Function to restart Bluetooth services
restart_bluetooth() {
    print_status "Restarting Bluetooth services..."

    # Stop Bluetooth service
    systemctl stop bluetooth
    sleep 2

    # Try to unload and reload modules (may fail if in use, that's OK)
    print_status "Attempting to reload Bluetooth modules..."
    if modprobe -r btusb btintel btrtl btbcm btmtk 2>/dev/null; then
        print_status "Modules unloaded successfully"
        sleep 2
        modprobe btintel
        modprobe btusb
        print_status "Modules reloaded"
    else
        print_warning "Could not unload modules (likely in use - this is normal)"
    fi

    # Start Bluetooth service
    systemctl start bluetooth
    sleep 3

    print_success "Bluetooth service restarted"
}

# Function to test Bluetooth functionality
test_bluetooth() {
    print_status "Testing Bluetooth functionality..."

    if bluetoothctl show &>/dev/null; then
        print_success "Bluetooth controller is now available!"

        # Show controller info
        echo ""
        print_status "Controller information:"
        bluetoothctl show | head -10

        return 0
    else
        print_error "Bluetooth controller still not available"
        return 1
    fi
}

# Function to create persistent fix
create_persistent_fix() {
    print_status "Creating persistent fix..."

    # Create udev rule for Intel Bluetooth devices
    udev_rule_file="/etc/udev/rules.d/50-intel-bluetooth-power.rules"

    if [ ! -f "$udev_rule_file" ]; then
        cat > "$udev_rule_file" << 'EOF'
# Fix USB power management for Intel Bluetooth devices
SUBSYSTEM=="usb", ATTRS{idVendor}=="8087", ATTRS{idProduct}=="0029", ATTR{power/control}="on"
SUBSYSTEM=="usb", ATTRS{idVendor}=="8087", ATTRS{idProduct}=="0025", ATTR{power/control}="on"
SUBSYSTEM=="usb", ATTRS{idVendor}=="8087", ATTRS{idProduct}=="0032", ATTR{power/control}="on"
EOF

        print_success "Created udev rule: $udev_rule_file"

        # Reload udev rules
        udevadm control --reload-rules
        udevadm trigger

        print_success "Udev rules reloaded - fix will persist after reboot"
    else
        print_status "Persistent fix already exists: $udev_rule_file"
    fi
}

# Main function
main() {
    echo "=============================================="
    echo "    Intel Bluetooth Fix Script"
    echo "=============================================="
    echo ""

    # Check if we need sudo
    if [ "$1" != "--check-only" ]; then
        check_sudo
    fi

    # Detect the issue
    if detect_bluetooth_issue; then
        print_success "Bluetooth appears to be working normally"
        if [ "$1" != "--force" ]; then
            echo ""
            print_status "Use --force to apply fix anyway, or --check-only to just check status"
            exit 0
        fi
    fi

    if [ "$1" == "--check-only" ]; then
        print_status "Check complete"
        exit 0
    fi

    echo ""
    print_status "Applying Bluetooth fixes..."
    echo ""

    # Find Intel Bluetooth devices
    find_intel_bluetooth

    echo ""

    # Fix USB power management
    fix_usb_power_management

    echo ""

    # Restart Bluetooth
    restart_bluetooth

    echo ""

    # Test functionality
    if test_bluetooth; then
        echo ""
        create_persistent_fix

        echo ""
        echo "=============================================="
        print_success "Bluetooth fix completed successfully!"
        echo "=============================================="
        echo ""
        print_status "You can now:"
        print_status "• Use Bluetooth settings in your desktop environment"
        print_status "• Run 'bluetoothctl scan on' to discover devices"
        print_status "• Connect to your Bluetooth devices normally"
        echo ""
        print_status "The fix has been made persistent and should survive reboots."

    else
        echo ""
        echo "=============================================="
        print_error "Fix attempt failed"
        echo "=============================================="
        echo ""
        print_status "Additional steps you can try:"
        print_status "• Check dmesg for hardware errors: sudo dmesg | grep -i bluetooth"
        print_status "• Verify firmware files: ls /lib/firmware/intel/ibt-*"
        print_status "• Try a system reboot"
        print_status "• Check for BIOS/UEFI Bluetooth settings"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Intel Bluetooth Fix Script"
        echo ""
        echo "Usage: $0 [OPTION]"
        echo ""
        echo "Options:"
        echo "  --check-only    Only check Bluetooth status, don't apply fixes"
        echo "  --force         Apply fixes even if Bluetooth appears to be working"
        echo "  --help, -h      Show this help message"
        echo ""
        echo "This script fixes common Intel Bluetooth USB power management issues."
        exit 0
        ;;
    --check-only|--force)
        main "$1"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        print_status "Use --help for usage information"
        exit 1
        ;;
esac
