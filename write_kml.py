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
file1 = open("/var/lib/banditvis/output/offences.txt", "w")
for offence in offences:
	offence = offence[0]
	file2 = open("/var/lib/banditvis/output/"+offence+".kml", "w")

	### Print Prefix
	file2.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	file2.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
	file2.write('\t<Document>\n')
	
	### Get and print Data
	db.cursor.execute("SELECT ip_address, count, first_seen, last_seen, ST_AsKML(location) FROM bandits WHERE offence = '"+offence+"' ORDER BY last_seen ASC;")
	rows = db.cursor.fetchall()
	i = 0
	for row in rows:
		i = i+1
		file2.write('\t\t<Placemark id="'+str(i)+'">\n')
		file2.write('\t\t\t<name>'+row[0]+'</name>\n')
		file2.write('\t\t\t<description>offence: '+offence+', count: '+str(row[1])+', first_seen: '+str(row[2])+', last_seen: '+str(row[3])+'</description>\n')
		file2.write('\t\t\t'+row[4]+'\n')
		file2.write('\t\t</Placemark>\n')

	### Print Suffix
	file2.write('\t</Document>\n')
	file2.write('</kml>')
	file2.close
	file1.write(offence+'\n')

file1.close 

### Finished
exit()