# !/usr/bin/env python3

# Jeromy Oliver

# GPA_09.py

# July 14th, 2025

# GPA 9: Git and GitHub

# In line with GPA 9 instructions, this file has been modified to reflect the
# solution from GPA 8 instead of the original file content of networkFileRW.py

# Program operates in much the same way as GPA 6, but uses JSON files to gather info
# on switches and routers. This iteration will also write results to two separate files
# for updates and invalid attempts when run. The program will then also print the numbers of
# updates and invalid addresses after finalizing selections.

# try/except used to import the JSON module, or print an error to console if module fails. 

try:

    import json

except ImportError:

    print("Error: JSON module could not be imported.")

    exit()

# Constants assigned to the two JSON files with switch/router info, and two for the eventual
# output files that will be written once program runs. 

ROUTER_FILE = "equip_r.txt"

SWITCH_FILE = "equip_s.txt"

UPDATED_TXT = "updated.txt"

INV_TXT = "invalid.txt"

# Constants assigned for user input prompts

UPDATE = "\nWhich device would you like to update "

QUIT = "(enter x to quit)? "

NEW_IP = "What is the new IP address (111.111.111.111) "

SORRY = "Sorry, that is not a valid IP address\n"

# Function defined to validate user input for device selection. If invalid,
# prints an error message.

def getValidDevice(routers, switches):

    while True:

        device = input(UPDATE + QUIT).lower()

        if device in routers or device in switches or device == 'x':

            return device

        else:

            print("That device is not in the network inventory.")


# Function defined to validate IP address updates input by user. While loop
# is used to validate that octets are proper length and within range.

def getValidIP(invalidIPCount, invalidIPAddresses):

    while True:

        ipAddress = input(NEW_IP)

        octets = ipAddress.split('.')

        if len(octets) != 4:

            invalidIPCount += 1

            invalidIPAddresses.append(ipAddress)

            print(SORRY)

            continue

        try:

            if all(0 <= int(byte) <= 255 for byte in octets):

                return ipAddress, invalidIPCount

            else:

                raise ValueError

        except ValueError:

            invalidIPCount += 1

            invalidIPAddresses.append(ipAddress)

            print(SORRY)


def main():

# imports router and switch information from the two provided JSON-formatted files.

    with open(ROUTER_FILE, 'r') as rf:

        routers = json.load(rf)

    with open(SWITCH_FILE, 'r') as sf:

        switches = json.load(sf)

# empty dictionary and list to be populated with updates and invalid IPs. These will be
# written to the two output files upon program completion.

    updated = {}

    invalidIPAddresses = []

# Counters used for final summary

    devicesUpdatedCount = 0

    invalidIPCount = 0

    quitNow = False

# Displays inventory for user to select from.

    print("Network Equipment Inventory\n")

    print("\tequipment name\tIP address")

    for router, ipa in routers.items():

        print("\t" + router + "\t\t" + ipa)

    for switch, ipa in switches.items():

        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        device = getValidDevice(routers, switches)

        if device == 'x':

            quitNow = True

            break

        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

# Dictionary update

        if device in routers:

            routers[device] = ipAddress

        else:

            switches[device] = ipAddress

        devicesUpdatedCount += 1

        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

# Prints final summary for user including number of devices updated and
# attempted invalid IPs

    print("\nSummary:\n")

    print("Number of devices updated:", devicesUpdatedCount)

# updated.txt file is created and written with the updated devices.
# an alert is also printed to the console to signal the file's
# creation.

    with open(UPDATED_TXT, 'w') as uf:

        json.dump(updated, uf)

    print("Updated equipment written to file 'updated.txt'\n")

# Same as above, an invalid.txt file is created and the invalid IP
# attempts are written to it. Another alert is printed to the console.

    print("Number of invalid addresses attempted:", invalidIPCount)

    with open(INV_TXT, 'w') as ef:

        json.dump(invalidIPAddresses, ef)

    print("List of invalid addresses written to file 'invalid.txt'")

# ensures main will only run if program is executed directly

if __name__ == "__main__":

    main()

