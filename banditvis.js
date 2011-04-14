 <!-- This file is part of the project Banditvis and licensed under GNU LGPL. -->
 
 var map, dataLayers, debug;
			
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
	
	debug = document.getElementById("debug");
	
	loadData();
	
	dataLayers[1].events.on({
		'featureselected': function(evt) { showPopup(evt.feature) },
		'featureunselected': function(evt) { evt.feature.popup.destroy() }
	});
	
	hover = new OpenLayers.Control.SelectFeature(dataLayers, {multiple: true, toggle: true});
	map.addControl(hover);
	hover.activate(true);
	
}

function loadData() {
	dataLayers = new Array();
	dataLayers.push(new OpenLayers.Layer.GML("Server", "server.kml", {format: OpenLayers.Format.KML}));
	dataLayers.push(new OpenLayers.Layer.GML("ssh", "output/ssh.kml", {format: OpenLayers.Format.KML}));
	<!-- more data here -->
	
	for(i in dataLayers){
		map.addLayer(dataLayers[i]);
	}
	return;
}

function showPopup(feature) {
	console.log(feature);
	feature.popup = new OpenLayers.Popup(null, feature.geometry.getBounds().getCenterLonLat(), new OpenLayers.Size(50, 20), providePopupContent(feature), false, null);
	feature.popup.autoSize = true;
	feature.popup.displayClass = "Popup";
	feature.popup.contentDisplayClass = "PopupContent";
	feature.popup.setBorder("1px solid black");
	feature.popup.setOpacity(0.7);
	map.addPopup(feature.popup);
	feature.popup.show();
	return;
}

function providePopupContent(feature) {

	match = feature.data.description.search("offence: (.*?), count: (.*?), last_seen: (.*)");
	if (match == -1) {
		console.log("Regex failed");
		content = "<h3>" + feature.data.name + "</h3><p>" + feature.data.description + "</p>";	
	} else {
		content = "<h3>" + feature.data.name + "</h3><p>Offence: " + RegExp.$1 + "<br/>Count: " + RegExp.$2 + "<br/>Last time seen: " + RegExp.$3 + "</p>";
		console.log(feature.data.description);
		console.log(content);
	}

	return content;
}
