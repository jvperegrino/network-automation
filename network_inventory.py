# network_inventory.py

devices = [
    {
        "hostname": "R1",
        "management_ip": "192.168.1.10",
        "device_type": "Router",
        "location": "Manila",
        "status": "UP"
    },
    {
        "hostname": "R2",
        "management_ip": "192.168.1.11",
        "device_type": "Router",
        "location": "Cebu",
        "status": "DOWN"
    },
    {
        "hostname": "SW1",
        "management_ip": "192.168.1.20",
        "device_type": "Switch",
        "location": "Davao",
        "status": "UP"
    }
]


# Display all devices
print("=" * 60)
print("NETWORK DEVICE INVENTORY")
print("=" * 60)

for device in devices:
    print(f"Hostname      : {device['hostname']}")
    print(f"Management IP : {device['management_ip']}")
    print(f"Device Type   : {device['device_type']}")
    print(f"Location      : {device['location']}")
    print(f"Status        : {device['status']}")
    print("-" * 60)


# Display only devices that are UP
print("\nDEVICES CURRENTLY UP")
print("=" * 60)

for device in devices:
    if device["status"] == "UP":
        print(
            f"{device['hostname']} - "
            f"{device['management_ip']} - "
            f"{device['device_type']} - "
            f"{device['location']}"
        )


# Count operational devices
operational_count = 0

for device in devices:
    if device["status"] == "UP":
        operational_count += 1


print("\nOPERATIONAL DEVICE COUNT")
print("=" * 60)
print(f"Devices currently UP: {operational_count}")
print(f"Total devices       : {len(devices)}")