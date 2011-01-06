#!/usr/bin/env python
# This file is part of Banditvis and licensed under GNU LGPL.

import MySQLdb			# for DB interaction
import GeoIP			# for Location Lookup
import Image			# for image manipulation

## connect to the db
db = MySQLdb.connect("engineroom.thomas-steinbrenner.net", "banditvis", "UwpQUMS5cD3YdrLr", "banditvis")
cursor = db.cursor()

# Select All
cursor.execute("SELECT * FROM `bandits`")
results = cursor.fetchall()
db.close()


## load bandits
# ip, count, lon, lat
bandits = []

i = 0
for row in results:
	i = i + 1
	bandits.append([row[1], row[2], 0, 0])

## lookup bandits

import GeoIP
gi = GeoIP.open("GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)

for bandit in bandits:
	record =  gi.record_by_addr(bandit[0])
	if record == None:
		continue
	bandit[2] = record['longitude']
	bandit[3] = record['latitude']



# osm bbox (W, S, O, N)
bbox = (-180, -60, 180, 84)
# offset in degrees
offset_x = (-180 - bbox[0])
offset_y = (90 - bbox[3])

print offset_x, offset_y


# load the map
plain_map = Image.open("input/map.png")
if map == None:
	print "ERROR: loading of inpug/map.png failed!"
	exit()

print plain_map.format, plain_map.size, plain_map.mode, plain_map.info

size = plain_map.size

# _grid == how many pixels are 1 degree ?
x_dist = round((plain_map.size[0] / float((abs(bbox[0]) + abs(bbox[2])))), 1)
y_dist = round((plain_map.size[1] / float((abs(bbox[1]) + abs(bbox[3])))), 1)

print (abs(bbox[0]) + abs(bbox[2])), (abs(bbox[1]) + abs(bbox[3]))
print x_dist, y_dist

dot_map = plain_map.copy()

#for y in range(1, size[1]):
#	for x in range(1, size[0]):
#		if (x % ((10 * x_dist) + ) == 0) or (y % ((10 * y_dist) + (offset_y * y_dist)) == 0):
#			dot_map.putpixel((int(x + (offset_x * x_dist)),int(y)), (15, 200, 199, 150))


for bandit in bandits:
	print bandit
	# coordinates in degrees from upper left corner
	x_d = 180 + bandit[2]
	y_d = -(-90 + bandit[3])
	print x_d, y_d
	# coordinates in degress from upper left corner + bbox offset
	x_o = x_d - offset_x
	y_o = y_d - offset_y
	print x_o, y_o
	# coordinates in pixles
	x_p = round((x_o * x_dist), 0)
	y_p = round((y_o * y_dist), 0)
	print x_p, y_p
	dot_map.putpixel((int(x_p), int(y_p)), (200, 15, 15, 255))


dot_map.save("output/dot_map.png")