# restconf_monitor.py

import os
import requests
from requests.auth import HTTPBasicAuth

# Cisco IOS XE Sandbox information
HOST = os.getenv("CISCO_HOST", "sandbox-iosxe-latest-1.cisco.com")
USERNAME = os.getenv("CISCO_USERNAME", "developer")
PASSWORD = os.getenv("CISCO_PASSWORD")

PORT = 443

RESOURCE = "/restconf/data/ietf-interfaces:interfaces"

URL = f"https://{HOST}:{PORT}{RESOURCE}"

HEADERS = {
    "Accept": "application/yang-data+json"
}


def monitor_interfaces():
    if not PASSWORD:
        print("ERROR: CISCO_PASSWORD environment variable is not set.")
        return

    print("=" * 60)
    print("RESTCONF NETWORK MONITOR")
    print("=" * 60)
    print(f"Device : {HOST}")
    print(f"URL    : {URL}")
    print()

    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            verify=False,
            timeout=10
        )

        print(f"HTTP Status Code: {response.status_code}")
        print()

        if response.status_code == 200:
            data = response.json()

            interfaces = data.get(
                "ietf-interfaces:interfaces",
                {}
            ).get("interface", [])

            print("INTERFACE INFORMATION")
            print("-" * 60)

            for interface in interfaces:
                name = interface.get("name", "Unknown")
                enabled = interface.get("enabled", "Unknown")

                print(f"Interface: {name}")
                print(f"Enabled  : {enabled}")
                print("-" * 60)

        else:
            print("RESTCONF request failed.")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the Cisco router.")

    except requests.exceptions.Timeout:
        print("ERROR: Connection timed out.")

    except requests.exceptions.RequestException as error:
        print(f"ERROR: RESTCONF request failed: {error}")


if __name__ == "__main__":
    monitor_interfaces()