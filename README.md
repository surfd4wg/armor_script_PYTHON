# armor_script_PYTHON
# Authors:
#  Craig Ellrod, Joshua Seither
#
# Python3
#
This repo contains three python scripts that can be run against V2 of the armor API.
Reference:
 https://developer.armor.com/
 https://docs.armor.com/display/KBSS/Armor+API+Guide
 
These python scripts use the Preshared Key Authentication method - PSK:
 https://docs.armor.com/display/KBSS/Pre-Shared+Key+Authentication+Method
 
Scripts:
 armor_script.py - ubuntu 20.04, simply calls the API and outputs the result unformatted
 armor_script_json.py - ubuntu 20.04, calls the API and outputs pretty json
 armor_script_json_args.py - ubuntu 20.04, calls the API using api key and secret as command line arguments
