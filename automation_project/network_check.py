import json
import socket


INPUT_FILE = "inventory.json"
OUTPUT_FILE = "output.json"


def check_device(ip_address):
    """
    Simulate a network connectivity check.

    Returns UP if the device responds to a TCP connection attempt.
    """
    try:
        socket.create_connection(
            (ip_address, 443),
            timeout=2
        )

        return "UP"

    except (socket.timeout, ConnectionRefusedError, OSError):
        return "DOWN"


def main():

    try:
        with open(INPUT_FILE, "r") as file:
            devices = json.load(file)

    except FileNotFoundError:
        print(f"ERROR: {INPUT_FILE} was not found.")
        return

    except json.JSONDecodeError:
        print(f"ERROR: {INPUT_FILE} contains invalid JSON.")
        return

    results = []

    print("=" * 60)
    print("NETWORK DEVICE CHECK")
    print("=" * 60)

    for device in devices:

        hostname = device.get("hostname", "Unknown")
        ip_address = device.get("management_ip", "")

        if not ip_address:
            status = "DOWN"
        else:
            status = check_device(ip_address)

        result = {
            "hostname": hostname,
            "management_ip": ip_address,
            "device_type": device.get("device_type", "Unknown"),
            "location": device.get("location", "Unknown"),
            "status": status
        }

        results.append(result)

        print(
            f"{hostname:<10} "
            f"{ip_address:<16} "
            f"{status}"
        )

    try:
        with open(OUTPUT_FILE, "w") as file:
            json.dump(results, file, indent=4)

        print()
        print(f"Results saved to {OUTPUT_FILE}")

    except OSError as error:
        print(f"ERROR: Could not save results: {error}")


if __name__ == "__main__":
    main()