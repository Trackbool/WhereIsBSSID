#!/usr/bin/python
# -*- coding: utf-8 -*-
#Used API mylnikov.org

import sys
import requests
import json
import re

# Version 0.2.1
# Written by: Adrián Fernández --> (@adrianfa5)
# Contact email: adrifarnal@gmail.com


class console_colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    RED = "\033[91m"
    OKYELLOW = "\033[93m"
    GREEN = "\033[92m"
    LIGHTBLUE = "\033[96m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def title_ascii():
	print console_colors.GREEN+" _    _ _                  _____   ______  _____ _____ ___________"+console_colors.ENDC
	print console_colors.GREEN+"| |  | | |                |_   _|  | ___ \/  ___/  ___|_   _|  _  \ "+console_colors.ENDC
	print console_colors.GREEN+"| |  | | |__   ___ _ __ ___ | | ___| |_/ /\ `--.\ `--.  | | | | | | "+console_colors.ENDC
	print console_colors.GREEN+"| |/\| | '_ \ / _ \ '__/ _ \| |/ __| ___ \ `--. \`--. \ | | | | | | "+console_colors.ENDC
	print console_colors.GREEN+"\  /\  / | | |  __/ | |  __/| |\__ \ |_/ //\__/ /\__/ /_| |_| |/ / "+console_colors.ENDC 
	print console_colors.GREEN+" \/  \/|_| |_|\___|_|  \___\___/___|____/ \____/\____/ \___/|___/ "+console_colors.ENDC 
	print console_colors.GREEN+" ---------------------------------------------------------------"+console_colors.ENDC 
	print console_colors.LIGHTBLUE+"			Written by Adrián Fernández-(@adrianfa5)"+console_colors.ENDC 
	print ""	
	print " [i] The BSSID Geolocation is based in a database with about 34M + of records."
	print " [i] Some BSSIDs may not be on the database"

title_ascii()

if (len(sys.argv) <= 1) or ("--h" in sys.argv) or ("-h" in sys.argv) :
	print console_colors.WARNING+"    [!] Options to use:"+console_colors.ENDC
	print console_colors.WARNING+"    	  --h Show this help menu"+console_colors.ENDC
	print console_colors.WARNING+"    	  --M BSSID (The MAC Address From the Access Point)"+console_colors.ENDC
	print console_colors.WARNING+"    	  --L Show Location"+console_colors.ENDC
	print console_colors.WARNING+"    [!] Examples:"+console_colors.ENDC
	print console_colors.WARNING+"    	  # python whereisbssid.py --M 00:11:22:DD:EE:FF"+console_colors.ENDC
	print console_colors.WARNING+"    	  # python whereisbssid.py --M 00:11:22:DD:EE:FF --L"+console_colors.ENDC
else:
	location = False
	bssid = False
	regex = "a"
	try:
		regexp = "(([0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2})|(([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4})"
		if (re.match(regexp, sys.argv[2])) and (len(sys.argv[2]) == 17):
			mac = sys.argv[2]			
		else:
			print console_colors.RED+" [!] Error, you have to put the argument --M and the BSSID"+ console_colors.ENDC
			quit()	
	except:
		print console_colors.RED+" [!] Invalid Address. Put a valid BSSID next to --M"+ console_colors.ENDC
		quit()

	try:
		if ("--M" in sys.argv):
			print ""
			print console_colors.OKBLUE+" [-] BSSID --> "+ mac + console_colors.ENDC
		else:
			print ""		
			print console_colors.RED+" [!] Error, you have to put the argument --M and the BSSID"
			quit()
		if ("--L" in sys.argv):
			ver = "1.2"
			print console_colors.OKBLUE+" [-] Show Location " + console_colors.ENDC
		else:
			ver = "1.1"
		
		print console_colors.OKBLUE+" Sending request..."+ console_colors.ENDC
		#Hacer peticion a la API // Make API request
		requ = requests.get("https://api.mylnikov.org/geolocation/wifi?v="+ver+"&bssid="+mac)		
		resp = requ.content
		json_pars = json.loads(resp)
		#Comprobar si la respuesta HTTP es 200 OK // Check if the HTTP response is 200 OK
		array_request=json_pars["result"]
		request_data = json.dumps(array_request, sort_keys=True)
		if (request_data == "200"):
			if (ver == "1.2"): 
				array_location = json_pars["data"]["location"]
				location_data = json.dumps(array_location, sort_keys=True)
			array_latitude = json_pars["data"]["lat"]
			array_range = json_pars["data"]["range"]
			array_longitude = json_pars["data"]["lon"]
			array_time = json_pars["data"]["time"]

			#Datos extraidos del array // Extracted array data
			latitude_data = json.dumps(array_latitude, sort_keys=True)
			range_data = json.dumps(array_range, sort_keys=True)
			longitude_data = json.dumps(array_longitude, sort_keys=True)
			time_data = json.dumps(array_time, sort_keys=True)

			print console_colors.OKYELLOW + " [#] Extracted Data:"
			if (ver == "1.2"): 		
				print console_colors.GREEN+"   [*] Location: " + location_data + console_colors.ENDC
			print console_colors.GREEN+"   [*] Latitude: " + latitude_data + console_colors.ENDC
			print console_colors.GREEN+"   [*] Range: " + range_data + console_colors.ENDC
			print console_colors.GREEN+"   [*] Longitude: " + longitude_data + console_colors.ENDC
			print console_colors.GREEN+"   [*] Time: " + time_data + console_colors.ENDC
		else:
			print console_colors.RED+" [!] There is no data from this BSSID --> "+mac+console_colors.ENDC
			print " [i] Don't worry, I love you <3. You can try with another one"

	except:
		print console_colors.RED+" [!] The server can't reply the request. Check your internet connection or try it later" + console_colors.ENDC	