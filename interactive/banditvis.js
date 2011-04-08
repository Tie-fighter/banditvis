 <!-- This file is part of the project Banditvis and licensed under GNU LGPL. -->
 
 var map;
	function init(){
		map = new OpenLayers.Map('map');
		var osm = new OpenLayers.Layer.OSM("OpenStreetMaps");
		map.addLayer(osm);
		
		map.setCenter(
			new OpenLayers.LonLat(10.75, 49.1).transform(
				new OpenLayers.Projection("EPSG:4326"),
				map.getProjectionObject()
                ), 2
		);
		map.addControl(new OpenLayers.Control.LayerSwitcher());
				
		data_layers = load_data();
		for(i in data_layers){
			map.addLayer(data_layers[i]);
		}
			
	}
		
function load_data() {
	data_layers = new Array();
	data_layers.push(new OpenLayers.Layer.GML("Server", "server.kml", {format: OpenLayers.Format.KML}));
	data_layers.push(new OpenLayers.Layer.GML("ssh jail", "output/data.kml", {format: OpenLayers.Format.KML}));
	return data_layers;
}