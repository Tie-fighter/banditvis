 <!-- This file is part of the project Banditvis and licensed under GNU LGPL. -->
 
 var map, dataLayers, debug;
 
 /* Called via map.html onload */
 /* Does a lot... */
 /* Returns nothing */
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
	addStyles();
	addClustering();
	addMouseOver();

	return;
}

/* Called by init() */
/* Adds layers of data to the map */
/* Returns nothing */
function loadData() {
	dataLayers = new Array();
	dataLayers.push(new OpenLayers.Layer.GML("Server", "server.kml", {format: OpenLayers.Format.KML}));
	dataLayers.push(new OpenLayers.Layer.GML("ssh", "output/ssh.kml", {format: OpenLayers.Format.KML}));
	<!-- more data here -->
	
	map.addLayers(dataLayers);
	return;
}



function addStyles(){
	var style = new OpenLayers.Style({
		pointRadius: "${radius}",
		fillColor: "#ff5454",
		fillOpacity: 0.8,
		strokeColor: "#000000",
		strokeWidth: "${width}",
		strokeOpacity: 0.8
		}, {
		context: {
			width: function(feature) { return (feature.cluster) ? 3 : 1; },
            radius: function(feature) {
				if(feature.cluster) {
					var r = 3 + feature.attributes.count;
				} else {
					var r = 5;
				}
                return r;
            }
        }
    });

	dataLayers[1].styleMap =  new OpenLayers.StyleMap({
		"default": style,
		"select": {
			fillColor: "#54ffff",
			strokeColor: "#000000"
		}
	});
	
	return;
}

/* Called by init() */
/* Adds the clustering strategy to the dataLayer*/
/* Returns nothing */
function addClustering() {	
	var clustering = new OpenLayers.Strategy.Cluster({distance: 25, threshold: 2});
	clustering.setLayer(dataLayers[1]);
	dataLayers[1].strategies = clustering;
	dataLayers[1].strategies.activate();
	return;
}

/* Called by init() */
/* Adds the Hover/Select-effect */
/* Returns nothing */
function addMouseOver() {
	dataLayers[1].events.on({
		//'hoverfeature': function(evt) { showPopup(evt.feature) },
		//'outfeature': function(evt) { evt.feature.popup.destroy() },
		'featureselected': function(evt) { showPopup(evt.feature) },
		'featureunselected': function(evt) { evt.feature.popup.destroy() }
	});
	
	hover = new OpenLayers.Control.SelectFeature(dataLayers, {/*hover: true, */multiple: true, toggle: true});
	map.addControl(hover);
	hover.activate(true);
	return;
}

/* Called as Eventhandler */
/* Creates a Popup and shows it */
/* Returns nothing */
function showPopup(feature) {
	console.log(feature);
	feature.popup = new OpenLayers.Popup(null, feature.geometry.getBounds().getCenterLonLat(), new OpenLayers.Size(270, 85), providePopupContent(feature), false, null);
	feature.popup.autoSize = true;
	feature.popup.displayClass = "Popup";
	feature.popup.contentDisplayClass = "PopupContent";
	feature.popup.setBorder("1px solid black");
	feature.popup.setOpacity(0.8);
	//feature.popup.minSize = new OpenLayers.Size(300, 100);
	map.addPopup(feature.popup);
	feature.popup.show();
	return;
}

/* Called by showPopup(feature) */
/* Returns the features name and description as a formatted string */
function providePopupContent(feature) {
	if (feature.cluster) { 
		content = "<b>Cluster of " + feature.attributes.count + " IPs:</b>";
		for (i in feature.cluster) {
			content = content + "<br/>" + feature.cluster[i].data.name;
		}
	} else {
		match = feature.data.description.search("offence: (.*?), count: (.*?), last_seen: (.*)");
		if (match == -1) {
			console.log("Regex failed");
			content = "<b>" + feature.data.name + "</b><br/>" + feature.data.description;	
		} else {
			content = "<b>" + feature.data.name + "</b><br/>Offence: " + RegExp.$1 + "<br/>Count: " + RegExp.$2 + "<br/>Last time seen: " + RegExp.$3;
		}
	}
	return content;
}
