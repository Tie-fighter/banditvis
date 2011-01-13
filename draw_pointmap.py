#!/usr/bin/env python
# This file is part of the project Banditvis and licensed under GNU LGPL.

import mapnik			# for drawing the map

# Instantiate a map object with given width, height and spatial reference system
m = mapnik.Map(2400, 1158, "+proj=latlong +datum=WGS84")

# Set background colour to 'steelblue'.  
# You can use 'named' colours, #rrggbb, #rgb or rgb(r%,g%,b%) format
m.background = mapnik.Color('steelblue')

### Map Style
style0 = mapnik.Style()
rule0 = mapnik.Rule()
rule0.symbols.append(mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9')))
rule0.symbols.append(mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),0.1))
#rule0.symbols.append(mapnik.ShieldSymbolizer('NAME','DejaVu Sans Bold', 6, mapnik.Color('#000000'),'', '', 0, 0))
style0.rules.append(rule0)

### Data Style
style1 = mapnik.Style()
rule1 = mapnik.Rule()
points = mapnik.PointSymbolizer('attacker.png', 'png', 5, 5)
points.allow_overlap = True
rule1.symbols.append(points)
#rule1.symbols.append(mapnik.ShieldSymbolizer('ip_address','DejaVu Sans Bold', 10, mapnik.Color('#000000'),'attacker.png', 'png', 5, 5))
style1.rules.append(rule1)

### Add styles
m.append_style('Map Style', style0)
m.append_style('Data Style', style1)


### World Layer
layer0 = mapnik.Layer('world',"+proj=latlong +datum=WGS84")
layer0.datasource = mapnik.Shapefile(file='data/shapes/TM_WORLD_BORDERS-0.3')
layer0.styles.append('Map Style')

### Data Layer
layer1 = mapnik.Layer('attackers',"+proj=latlong +datum=WGS84")
layer1.datasource = mapnik.PostGIS(host='localhost', user='banditvis', password='UwpQUMS5cD3YdrLr', dbname='banditvis', table='bandits')
layer1.styles.append('Data Style')

### Add Layers
m.layers.append(layer0)
m.layers.append(layer1)

### Zoom
m.zoom_to_box(layer0.envelope())

### Write file
mapnik.render_to_file(m,'output/world.png', 'png')

exit()