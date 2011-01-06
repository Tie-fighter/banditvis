#!/usr/bin/env python
# This file is part of the project Banditvis and licensed under GNU LGPL.

import mapnik			# for drawing the map

# Instantiate a map object with given width, height and spatial reference system
m = mapnik.Map(2400,1158,"+proj=latlong +datum=WGS84")
# Set background colour to 'steelblue'.  
# You can use 'named' colours, #rrggbb, #rgb or rgb(r%,g%,b%) format
m.background = mapnik.Color('steelblue')

# Now lets create a style and add it to the Map.
s = mapnik.Style()
# A Style can have one or more rules. A rule consists of a filter, min/max scale 
# demoninators and 1..N Symbolizers. If you don't specify filter and scale denominators
# you get default values :
#   Filter =  'ALL' filter (meaning symbolizer(s) will be applied to all features) 
#   MinScaleDenominator = 0
#   MaxScaleDenominator = INF  
# Lets keep things simple and use default value, but to create a map we 
# we still must provide at least one Symbolizer. Here we  want to fill countries polygons with 
# greyish colour and draw outlines with a bit darker stroke.

####### POINTS
#points = mapnik.PointDatasource()
#points.add_point(0, 0, '0,0', 'lol') 
#points.add_point(10, 10, '10,10', 'lol')

shield = mapnik.ShieldSymbolizer('NAME','DejaVu Sans Bold',6,mapnik.Color('#000000'),'attacker.png', 'png', 5, 5)



r=mapnik.Rule()
r.symbols.append(mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9')))
r.symbols.append(mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),0.1))

###### POINTS SYMB
symb = mapnik.PointSymbolizer("attacker.png","png", 5,5)
#symb.opacity = .5
symb.allow_overlap = True

r.symbols.append(shield)
s.rules.append(r)

#lyr = mapnik.Layer('Places','+proj=latlon +datum=WGS84')
#lyr.datasource = points
#lyr.styles.append('places_labels')


# Here we have to add our style to the Map, giving it a name.
m.append_style('My Style',s)

# Here we instantiate our data layer, first by giving it a name and srs (proj4 projections string), and then by giving it a datasource.
lyr = mapnik.Layer('world',"+proj=latlong +datum=WGS84")
# Then provide the full filesystem path to a shapefile in WGS84 or EPSG 4326 projection without the .shp extension
# A sample shapefile can be downloaded from http://mapnik-utils.googlecode.com/svn/data/world_borders.zip
lyr.datasource = mapnik.Shapefile(file='data/shapes/TM_WORLD_BORDERS-0.3')
lyr.styles.append('My Style')

m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())

# Write the data to a png image called world.png in the base directory of your user
mapnik.render_to_file(m,'output/world.png', 'png')

# Exit the python interpreter
exit()