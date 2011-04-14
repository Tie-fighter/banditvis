#!/usr/bin/env python
# This file is part of the project Banditvis and licensed under GNU LGPL.

import psycopg2					# for interaction with Postgres

from my_functions import *		# import our own functions

### Connect to the db
db = DbConn()
db.read_config()
db.conn = psycopg2.connect(host = db.host, user = db.user, password = db.password, database = db.database)
db.cursor = db.conn.cursor()

### Get different offences
db.cursor.execute("SELECT DISTINCT offence FROM bandits;")
offences = db.cursor.fetchall()

### Write .kml for every offence
for offence in offences:
	offence = offence[0]
	file = open("/var/lib/banditvis/output/"+offence+".kml", "w")
	### Print Header
	file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
	file.write('\t<Document>\n')
	
	### Get and print Data
	db.cursor.execute("SELECT ip_address, count, last_seen, ST_AsKML(location) FROM bandits WHERE offence = '"+offence+"'")
	rows = db.cursor.fetchall()
	for row in rows:
		file.write('\t\t<Placemark>\n')
		file.write('\t\t\t<name>'+row[0]+'</name>\n')
		file.write('\t\t\t<description>offence: '+offence+', count: '+str(row[1])+', last_seen: '+str(row[2])+'</description>\n')
		file.write('\t\t\t'+row[3]+'\n')
		file.write('\t\t</Placemark>\n')

	### Print Trailer
	file.write('\t</Document>\n')
	file.write('</kml>')
	file.close

### Finished
exit()