#!/usr/bin/env python
# This file is part of Banditvis and licensed under GNU LGPL.


import urllib
import re
import os
import time

def download_database():
	print 'Downloading...'
	urllib.urlretrieve ("http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz", "data/GeoIP/GeoLiteCity.dat.gz")
	os.system("gunzip -f data/GeoIP/GeoLiteCity.dat.gz")
	exit()

filename = "data/GeoIP/GeoLiteCity.dat"
if os.path.isfile(filename) == False:
	download_database()
else:
	statbuf = os.stat(filename)

url = urllib.urlopen("http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz")

#print 'Now:  ' + time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
#print 'URL:  ' + str(url.headers.get('Last-Modified'))
#print 'File: ' + str(time.ctime(statbuf.st_mtime))

url_date = time.strptime(str(url.headers.get('Date')), "%a, %d %b %Y %H:%M:%S %Z")
file_date = time.localtime(statbuf.st_mtime)

#print url_date
#print file_date

if url_date > file_date:
	print 'New file available.'
	download_database()
else:
	print 'No new file available.'
	exit()

