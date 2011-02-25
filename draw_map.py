#!/usr/bin/env python
# This file is part of the project Banditvis and licensed under GNU LGPL.

import mapnik					# for drawing the map
import psycopg2					# for interaction with Postgres
from PIL import Image			# inserting metadata in the image
import ImageFont, ImageDraw		# inserting metadata in the image
import time						# for getting the time

from my_functions import *		# import our own functions

##### Draw Map
### Instantiate a map object with given width, height and spatial reference system
mapfile = "templates/test.xml"
m = mapnik.Map(2400, 1158)
mapnik.load_map(m, mapfile)

### World Layer
layer0 = mapnik.Layer('world',"+proj=latlong +datum=WGS84")
layer0.datasource = mapnik.Shapefile(file='data/shapes/TM_WORLD_BORDERS-0.3')

### Data Layer
layer1 = mapnik.Layer('attackers',"+proj=latlong +datum=WGS84")
layer1.datasource = mapnik.PostGIS(host='localhost', user='banditvis', password='UwpQUMS5cD3YdrLr', dbname='banditvis', table='bandits')

### Add Styles
layer0.styles.append('Map Style')
layer1.styles.append('Data Style')

### Add Layers
m.layers.append(layer0)
m.layers.append(layer1)

### Zoom
#m.zoom_to_box(layer0.envelope())
m.zoom_to_box(mapnik.Envelope(-180.0,-90.0,180.0,83.623596))


### Write file
mapnik.render_to_file(m,'output/world.png', 'png')

##### Get Metadata

# connect to the db
db = DbConn()
db.read_config()
db.conn = psycopg2.connect(host = db.host, user = db.user, password = db.password, database = db.database)
db.cursor = db.conn.cursor()

db.cursor.execute("SELECT sum(count) from bandits;")
count_attacks = int(db.cursor.fetchone()[0])
db.cursor.execute("SELECT COUNT(DISTINCT ip_address) FROM bandits;")
count_ips = int(db.cursor.fetchone()[0])

##### Insert Metadata

im = Image.open('output/world.png')
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('fonts/LinLibertine_Bd-4.1.5.otf', 20)
### Time of Render
draw.rectangle((5,5, 300,50), outline = (255,255,255))
draw.text((10, 5), time.strftime("Rendered: %d.%m.%Y %H:%M:%S GMT", time.gmtime()), (255,255,255), font=font)
draw.text((10, 25), str(count_attacks) + " attacks / "+ str(count_ips) +" IPs", (255,255,255), font=font)

###
#draw.rectangle((20,250, 350,1000), outline = (0,0,0))
#draw.text((25, 250), "more metadata...", (0,0,0), font=font)

### Write file
im.save('output/world.png')
im.save('/var/lib/banditvis/output/world.png')

exit()