#!/bin/usr/env python
# This file is part of Banditvis and licensed under GNU LGPL.

import ConfigParser		# read_config, 

db_host = ''
db_user = ''
db_password = ''
db_database = ''


def read_config():

	global db_host
	global db_user
	global db_password
	global db_database

	# check config
	config = ConfigParser.ConfigParser()
	config.read('config.ini')

#TODO check if file is actually there

	if config.get('mySQL', 'host') == '':
		print 'ERROR: mySQL host not set'
		print_usage()
		exit()
	else:
		db_host = config.get('mySQL', 'host')

	if config.get('mySQL', 'user') == '':
		print 'ERROR: mySQL user not set'
		print_usage()
		exit()
	else:
		db_user = config.get('mySQL', 'user')

	if config.get('mySQL', 'password') == '':
		print 'ERROR: mySQL password not set'
		print_usage()
		exit()
	else:
		db_password = config.get('mySQL', 'password')

	if config.get('mySQL', 'database') == '':
		print 'ERROR: mySQL database not set'
		print_usage()
		exit()
	else:
		db_database = config.get('mySQL', 'database')
	return