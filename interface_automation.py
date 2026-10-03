import getpass
import requests
import urllib3
from requests.auth import HTTPBasicAuth

# ============================================================
# RESTCONF INTERFACE AUTOMATION
# Cisco IOS XE / DevNet Sandbox
# ============================================================

# Disable the warning caused by the Cisco Sandbox's lab certificate.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ============================================================
# DEVICE SETTINGS
# ============================================================

DEVICE_IP = "10.10.20.48"
RESTCONF_PORT = 443

USERNAME = "developer"

BASE_URL = (
    f"https://{DEVICE_IP}:{RESTCONF_PORT}"
    "/restconf/data/ietf-interfaces:interfaces"
)

LOOPBACK_NAME = "Loopback100"

# ------------------------------------------------------------
# IMPORTANT:
# These are the example values used by this project.
# Change them if your instructor specified different values.
# ------------------------------------------------------------

LOOPBACK_IP = "10.100.100.1"
LOOPBACK_NETMASK = "255.255.255.255"

LOOPBACK_DESCRIPTION = "Loopback100 created using RESTCONF"


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}


# ============================================================
# AUTHENTICATION
# ============================================================

PASSWORD = getpass.getpass(
    f"Enter RESTCONF password for {USERNAME}: "
)

AUTH = HTTPBasicAuth(USERNAME, PASSWORD)


# ============================================================
# JSON PAYLOAD
# ============================================================

LOOPBACK_PAYLOAD = {
    "ietf-interfaces:interface": {
        "name": LOOPBACK_NAME,
        "description": LOOPBACK_DESCRIPTION,
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": LOOPBACK_IP,
                    "netmask": LOOPBACK_NETMASK
                }
            ]
        }
    }
}


# ============================================================
# CREATE LOOPBACK100
# ============================================================

def create_loopback():
    print("\n" + "=" * 60)
    print("CREATING LOOPBACK100")
    print("=" * 60)

    print(f"Device       : {DEVICE_IP}")
    print(f"Interface    : {LOOPBACK_NAME}")
    print(f"IP Address   : {LOOPBACK_IP}")
    print(f"RESTCONF URL : {BASE_URL}")

    try:
        response = requests.post(
            BASE_URL,
            headers=HEADERS,
            auth=AUTH,
            json=LOOPBACK_PAYLOAD,
            verify=False,
            timeout=15
        )

        print(f"\nHTTP Status Code: {response.status_code}")

        # 201 = successfully created
        if response.status_code == 201:
            print("SUCCESS: Loopback100 configuration created.")
            return True

        # 409 = resource already exists
        elif response.status_code == 409:
            print("INFO: Loopback100 already exists.")
            print("Proceeding to verification...")
            return True

        else:
            print("ERROR: Configuration request failed.")

            if response.text:
                print("\nRouter response:")
                print(response.text)

            return False

    except requests.exceptions.Timeout:
        print("ERROR: RESTCONF request timed out.")
        print("Check that the VPN is connected and the router is reachable.")
        return False

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the Cisco router.")
        print("Make sure the Cisco Sandbox VPN is connected.")
        return False

    except requests.exceptions.RequestException as error:
        print(f"ERROR: RESTCONF request failed: {error}")
        return False


# ============================================================
# VERIFY LOOPBACK100
# ============================================================

def verify_loopback():
    print("\n" + "=" * 60)
    print("VERIFYING LOOPBACK100")
    print("=" * 60)

    verification_url = (
        f"{BASE_URL}/interface={LOOPBACK_NAME}"
    )

    try:
        response = requests.get(
            verification_url,
            headers=HEADERS,
            auth=AUTH,
            verify=False,
            timeout=15
        )

        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code != 200:
            print("ERROR: Could not retrieve Loopback100.")

            if response.text:
                print("\nRouter response:")
                print(response.text)

            return False

        data = response.json()

        # ----------------------------------------------------
        # RESTCONF may return the interface as either:
        #
        # {
        #   "ietf-interfaces:interface": {...}
        # }
        #
        # or:
        #
        # {
        #   "ietf-interfaces:interface": [{...}]
        # }
        # ----------------------------------------------------

        interface = data.get("ietf-interfaces:interface")

        if not interface:
            print("ERROR: Loopback100 was not found.")
            return False

        # Handle list response
        if isinstance(interface, list):
            interface = interface[0]

        # ----------------------------------------------------
        # Display interface information
        # ----------------------------------------------------

        print("\nLoopback100 Configuration")
        print("-" * 40)

        print(f"Name        : {interface.get('name')}")
        print(f"Description : {interface.get('description')}")
        print(f"Type        : {interface.get('type')}")
        print(f"Enabled     : {interface.get('enabled')}")

        # ----------------------------------------------------
        # Display IPv4 information
        # ----------------------------------------------------

        ipv4 = interface.get("ietf-ip:ipv4", {})
        addresses = ipv4.get("address", [])

        if addresses:
            address = addresses[0]

            print(f"IP Address  : {address.get('ip')}")
            print(f"Netmask     : {address.get('netmask')}")
        else:
            print("IP Address  : Not configured")

        print("\nSUCCESS: Loopback100 verification completed.")

        return True

    except requests.exceptions.Timeout:
        print("ERROR: Verification request timed out.")
        return False

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the Cisco router.")
        return False

    except requests.exceptions.RequestException as error:
        print(f"ERROR: RESTCONF verification failed: {error}")
        return False

    except ValueError:
        print("ERROR: Router returned invalid JSON.")
        print(response.text)
        return False


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("RESTCONF INTERFACE AUTOMATION")
    print("=" * 60)

    print(f"Device : {DEVICE_IP}")
    print(f"User   : {USERNAME}")
    print(f"Target : {LOOPBACK_NAME}")

    # Create the interface
    create_success = create_loopback()

    # Verify the interface
    if create_success:
        verify_loopback()
    else:
        print("\nConfiguration was not successful.")
        print("Verification was skipped.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()