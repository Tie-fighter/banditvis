#!/usr/bin/env python
# This file is part of Banditvis and licensed under GNU LGPL.

import sys					# for argument passing
import os					# for exit code
import re					# for ip_address checking
import GeoIP				# for coord lookup
import psycopg2				# for interaction with Postgres
import time					# for getting the time

from my_functions import *		# import our own functions

def print_usage():
	print 'USAGE: add_bandit.py ip_address [OFFENCE]'
	print 'additional configuration: config.ini'

db = DbConn()
db.read_config()

# check arguments
if (len(sys.argv) < 2 or len(sys.argv) > 4):
	print_usage()
	exit()

if len(sys.argv) == 3:
	offence = sys.argv[2]
else:
	offence = 'unknown'

############## TODO
status = 'unknown'
##############

# check ip_address
ip_address_re = re.match('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$', sys.argv[1])

if ip_address_re == None:
		print 'ERROR: ip_address must be of form 0.0.0.0'
		print_usage()
		exit()

for group in ip_address_re.groups():
	if int(group) > 255:
		print 'ERROR: ip_address invalid'
		print_usage()
		exit()

# normalize ip
ip_address = str(int(ip_address_re.group(1))) + '.' + str(int(ip_address_re.group(2))) + '.' + str(int(ip_address_re.group(3))) + '.' + str(int(ip_address_re.group(4)))

# lookup bandit
gi = GeoIP.open("data/GeoIP/GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)

record =  gi.record_by_addr(ip_address)
if record != None:
	lon = record['longitude']
	lat = record['latitude']
else:
	lon = 0
	lat = 0

# connect to the db
db.conn = psycopg2.connect(host = db.host, user = db.user, password = db.password, database = db.database)
db.cursor = db.conn.cursor()

# increase count
now = time.strftime('%Y-%m-%d %H:%M:%S')

db.cursor.execute("SELECT add_bandit('"+ip_address+"_"+offence+"', '"+ip_address+"', '"+offence+"', '"+status+"', '"+now+"', '"+str(lon)+" "+str(lat)+"'); COMMIT;")

# finished
db.conn.close()