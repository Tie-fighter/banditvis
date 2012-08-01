 <!-- This file is part of the project Banditvis and licensed under GNU LGPL. -->
 
 Banditvis = new Object();
 Banditvis.max_ocount = 0;
  
 /* Called via map.html onload */
 /* Does a lot... */
 /* Returns nothing */
 function init(){
	Banditvis.map = new OpenLayers.Map('map');
	var osm = new OpenLayers.Layer.OSM("OpenStreetMaps");
	osm.transitionEffect = "resize";
	Banditvis.map.addLayer(osm);
	
	Banditvis.map.setCenter(
		new OpenLayers.LonLat(10.75, 49.1).transform(
			new OpenLayers.Projection("EPSG:4326"),
			Banditvis.map.getProjectionObject()
            ), 2
	);
	Banditvis.map.addControl(new OpenLayers.Control.LayerSwitcher());
	
	Banditvis.legend = document.getElementById("legend");
	Banditvis.legend.upper = document.getElementById("legend_upper");
	Banditvis.legend.lower = document.getElementById("legend_lower");
		
	loadData();
	Banditvis.map.events.on({ 'moveend': function(evt) {
		Banditvis.min_ocount = null;
		Banditvis.max_ocount = null;
		for ( var i in Banditvis.dataLayers) {
				updateMetadata(Banditvis.dataLayers[i]);
				Banditvis.dataLayers[i].redraw();
			}
	} });
	Banditvis.map.events.on({ 'zoomend': function(evt) {
		redrawPopups();
	} });

	return;
}

/* Called by init() */
/* Loads the offences file */
/* Returns nothing */
function loadData() {
	var xmlHttpObject = false;
	if (typeof XMLHttpRequest != 'undefined') {
		xmlHttpObject = new XMLHttpRequest();
	}
	if (!xmlHttpObject) {
		try {
			xmlHttpObject = new ActiveXObject("Msxml2.XMLHTTP");
		} catch(e) {
			try {
				xmlHttpObject = new ActiveXObject("Microsoft.XMLHTTP");
			} catch(e) {
				xmlHttpObject = null;
			}
		}
	}
	
	// var wait = true;
	// var waitTime = 10;
	xmlHttpObject.open("GET", "output/offences.txt");
	xmlHttpObject.onreadystatechange = function() {
		if (xmlHttpObject.readyState == 4) {
			loadKMLs(xmlHttpObject);
		}
	}
	xmlHttpObject.send(null);
}

/* Called by loadData() */
/* Adds layers of data to the map */
/* Returns nothing */
function loadKMLs(xmlHttpObject) {
	Banditvis.dataLayers = new Array();

	Banditvis.dataLayers.push(new OpenLayers.Layer.Vector("Server", {
                protocol: new OpenLayers.Protocol.HTTP({
                    url: "server.kml",
                    format: new OpenLayers.Format.KML()
                }),
                strategies: [new OpenLayers.Strategy.Fixed()]
            }));
	
	var responseLines=xmlHttpObject.responseText.split("\n")
	for (var i in responseLines) {
		if (responseLines[i] != "") {
			Banditvis.dataLayers.push(new OpenLayers.Layer.Vector(responseLines[i], {
                protocol: new OpenLayers.Protocol.HTTP({
                    url: "output/"+responseLines[i]+".kml",
                    format: new OpenLayers.Format.KML()
                }),
                strategies: [new OpenLayers.Strategy.Fixed()]
            }));
		}
	}


	for (var i in Banditvis.dataLayers) {
		Banditvis.map.addLayer(Banditvis.dataLayers[i]);
		Banditvis.dataLayers[i].strategies = new Array();
		
		Banditvis.dataLayers[i].events.on({"loadend": function() {
			addMetadata(Banditvis.dataLayers[i]);
			updateMetadata(Banditvis.dataLayers[i]);
			Banditvis.dataLayers[i].redraw();
		} });
		
		addStyles(Banditvis.dataLayers[i]);
		addClustering(Banditvis.dataLayers[i]);
		// addReloader(Banditvis.dataLayers[i]);
		addMouseOver(Banditvis.dataLayers[i]);
		
	}
	
	return;
}


/* Called by loadKMLs() */
/* Adds the style to the datapoints */
/* Returns nothing */
function addStyles(layer){
	var style = new OpenLayers.Style({
		pointRadius: "${radius}",
		fillColor: "${fillColor}",
		fillOpacity: 0.8,
		strokeColor: "#000000",
		strokeWidth: "${width}",
		strokeOpacity: 0.8,
		label: "${label}"
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
            },
			fillColor: function(feature) {
			
				if (!feature.attributes || !feature.attributes.ocount) {
					return "#808080";
				}
				var ocount = parseInt(feature.attributes.ocount);
				
				var r = 0;
				var R;
				var g = 0;
				var G;
				
				var p = (ocount - Banditvis.min_ocount) / (Banditvis.max_ocount - Banditvis.min_ocount) * 100;				
				
				if (p < 0 || p > 100 || isNaN(p))
					{ p = 50; }
				
				if (p >= 50) r = 255;
				if (p < 50) r = Math.round(p/50 * 255);
				
				if (p >= 50) g = 255 - Math.round((p-50)/50 * 255);
				if (p < 50) g = 255;
				
				if (r < 16) R = "0"+r.toString(16);
				else R = r.toString(16);
				
				if (g < 16) G = "0"+g.toString(16);
				else G = g.toString(16);
				
				var color = "#"+R+G+"00";
				if (color.length != 7) {
					alert(color);
				}
				return color;
				
			},
			label: function(feature) { 
				if (feature.cluster) {
					if (feature.attributes.count <= 3) {
						return "";
					}
					return feature.attributes.count;
				} else {
					return "";
				}
			}
			
        }
    });

	layer.styleMap =  new OpenLayers.StyleMap({
		"default": style,
		"select": {
			fillColor: "#54ffff",
			strokeColor: "#000000"
		}
	});
	
	return;
}

/* Called by loadKMLs() */
/* Fills feature.data with metadata */
/* Returns nothing */
function addMetadata(layer) {
	for (var i in layer.features) {
		if ( layer.features[i].cluster) {
			for (var j in layer.features[i].cluster) {
				extractMetadata(layer.features[i].cluster[j]);
			}
		} else {
			extractMetadata(layer.features[i]);
		}
	}
	return;
}

function extractMetadata(feature) {
	var match = feature.data.description.search("offence: (.*?), count: (.*?), first_seen: (.*?), last_seen: (.*)");
		if (match != -1) {
			feature.attributes.offence = RegExp.$1;
			feature.attributes.ocount = RegExp.$2;
			feature.attributes.first_time = RegExp.$3;
			feature.attributes.last_time = RegExp.$4;
		}
	return;
}

function updateMetadata(layer) {
for (var i in layer.features) {
	if (layer.features[i].onScreen()){
		if (layer.features[i].cluster) {
			var count = 0;
			for (var j in layer.features[i].cluster) {
				if (layer.features[i].cluster[j].attributes.ocount) {
					count = count + parseInt(layer.features[i].cluster[j].attributes.ocount);
				}
			}
			layer.features[i].attributes.ocount = parseInt(count);
		}
		if (layer.features[i].attributes.ocount > Banditvis.max_ocount) {
			Banditvis.max_ocount = parseInt(layer.features[i].attributes.ocount);
		}
		if (!Banditvis.min_ocount || layer.features[i].attributes.ocount < Banditvis.min_ocount) {
			Banditvis.min_ocount = parseInt(layer.features[i].attributes.ocount);
		}
	}
}
	Banditvis.legend.upper.innerHTML = Banditvis.max_ocount;
	Banditvis.legend.lower.innerHTML = Banditvis.min_ocount;
	return;
}

/* Called by loadKMLs() */
/* Adds the clustering strategy to the dataLayer*/
/* Returns nothing */
function addClustering(layer) {
	var clustering = new OpenLayers.Strategy.Cluster({distance: 25, threshold: 2});
		clustering.setLayer(layer);
		clustering.activate();
		layer.strategies.push(clustering);
	return;
}

/* Called by loadKMLs() */
/* Adds the Hover/Select-effect */
/* Returns nothing */
function addMouseOver(layer) {
	layer.events.on({
		//'hoverfeature': function(evt) { showPopup(evt.feature) },
		//'outfeature': function(evt) { evt.feature.popup.destroy() },
		'featureselected': function(evt) {
			//alert("evt: sel: " +evt.feature.id);
			showPopup(evt.feature);
			if (evt.redraw != true) {
				if (evt.feature.cluster == null) {
					//alert("arrayAdd: "+arrayAdd(evt.feature));
				} else {
					for (var i in evt.feature.cluster) {
						arrayAdd(evt.feature.cluster[i]);
					}
				}
			}
		},
		'featureunselected': function(evt) {
			//alert("evt: usel: " +evt.feature.id);
			//console.log(evt.feature.popup);
			if (evt.feature.popup != null) {
				evt.feature.popup.destroy();
			}
 			if (evt.redraw != true) {
				if (evt.feature.cluster == null) {
					//alert("arrayRemove: "+arrayRemove(evt.feature));
				} else {
					for (var i in evt.feature.cluster) {
						arrayRemove(evt.feature.cluster[i]);
					}
				}
			}
		}
	});
	Banditvis.hover = new OpenLayers.Control.SelectFeature(Banditvis.dataLayers, {/*hover: true, */multiple: true, toggle: true});
	Banditvis.map.addControl(Banditvis.hover);
	Banditvis.hover.activate(true);
	
	Banditvis.selectedFeatures = new Array();
	
	return;
}

/* Called by loadKMLs() */
/* Adds a reloading strategy */
/* Returns nothing */
function addReloader(layer) {
	var reloader = new OpenLayers.Strategy.Refresh({interval: 1000, force: true});
	reloader.setLayer(layer);
	reloader.activate();
	layer.strategies.push(reloader);	
	return;
}

/* Called as Eventhandler */
/* Creates a Popup and shows it */
/* Returns nothing */
function showPopup(feature) {
	feature.popup = new OpenLayers.Popup(null, feature.geometry.getBounds().getCenterLonLat(), new OpenLayers.Size(270, 85), providePopupContent(feature), false, null);
	feature.popup.autoSize = true;
	feature.popup.displayClass = "Popup";
	feature.popup.contentDisplayClass = "PopupContent";
	feature.popup.setBorder("1px solid black");
	feature.popup.setOpacity(0.8);
	Banditvis.map.addPopup(feature.popup);
	feature.popup.show();
	return;
}

/* Called by showPopup(feature) */
/* Returns the features name and description as a formatted string */
function providePopupContent(feature) {
	if (feature.cluster) { 
		content = "<b>Cluster of " + feature.attributes.count + " IPs<br/>Count: " + feature.attributes.ocount + "</b>";
		for (var i  in feature.cluster) {
			content = content + "<br/>" + feature.cluster[i].attributes.name;
		}
	} else {
		if (feature.attributes.name && feature.attributes.offence && feature.attributes.ocount && feature.attributes.last_time) {
			if (feature.attributes.first_time != feature.attributes.last_time) {
				content = "<b>" + feature.attributes.name + 
				"<br/>Count: " + feature.attributes.ocount + 
				"<br/>First time: " + feature.attributes.first_time + 
				"<br/>Last time: " + feature.attributes.last_time;
			} else {
				content = "<b>" + feature.attributes.name + 
				"<br/>Count: " + feature.attributes.ocount + 
				"<br/>Time: " + feature.attributes.last_time;
			}
		} else {
			content = "<b>" + feature.data.name + "</b><br/>" + feature.data.description;
		}
	}
	return content;
}

function redrawPopups() {

	//alert("Destroying all popups");
	for (var i in Banditvis.map.popups) {
		Banditvis.map.popups[i].destroy();
	}

	var evt = { redraw: true, feature: null }
	for (var i in Banditvis.selectedFeatures) {
		for (var j in Banditvis.dataLayers) {
			for (var k in Banditvis.dataLayers[j].features) {
			
				if (Banditvis.dataLayers[j].features[k].id == Banditvis.selectedFeatures[i].id){
					evt.feature = Banditvis.dataLayers[j].features[k];
					//alert("usel: " +evt.feature.id);
					Banditvis.dataLayers[j].events.triggerEvent('featureunselected', evt);
					//alert("sel: " +evt.feature.id);
					Banditvis.dataLayers[j].events.triggerEvent('featureselected', evt);

				} else if (Banditvis.dataLayers[j].features[k].cluster != null) {
					for (var l in Banditvis.dataLayers[j].features[k].cluster[l]) {
						if(Banditvis.dataLayers[j].features[k].cluster[l].id == Banditvis.selectedFeatures[i].id) {
						
							evt.feature = Banditvis.dataLayers[j].features[k].cluster[l];
							Banditvis.dataLayers[j].events.triggerEvent('featureunselected', evt);
							Banditvis.dataLayers[j].events.triggerEvent('featureselected', evt);				
						}
					}
				}
			}
		}
	}
	
	return;
}

function arrayAdd(feature) {
	for (var i in Banditvis.selectedFeatures) {
		if (Banditvis.selectedFeatures[i].id == feature.id) {
			Banditvis.selectedFeatures.splice(i);
			return false;
		}
	}
	Banditvis.selectedFeatures.push(feature);
	return true;
}

function arrayRemove(feature) {
	for (var i in Banditvis.selectedFeatures) {
		if (Banditvis.selectedFeatures[i].id == feature.id) {
			Banditvis.selectedFeatures.splice(i);
			return true;
		}
	}
	return false;
}






