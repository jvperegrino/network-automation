# Mini Network Automation Project

## Purpose

This project is a basic Python network automation tool that reads network device information from a JSON inventory file, checks the availability of each device, displays the results, and saves the results to an output JSON file.

## Project Structure

automation_project/
├── inventory.json
├── network_check.py
├── README.md
└── output.json

network_inventory.py	Stores and displays information about the network devices.
restconf_monitor.py	Retrieves and displays interface information from the Cisco router using RESTCONF.
interface_automation.py	Creates and verifies the Loopback100 interface using RESTCONF.
inventory.json	Stores the network device inventory in JSON format.
network_check.py	Checks the status of the listed network devices.
output.json	Stores the results produced by the network check.