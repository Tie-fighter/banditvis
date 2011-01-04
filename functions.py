#!/bin/usr/env python

import ConfigParser		# read_config, 



def read_config():

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
		db_db = config.get('mySQL', 'database')
	return