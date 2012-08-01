#!/bin/usr/env python
# This file is part of Banditvis and licensed under GNU LGPL.

import ConfigParser		# read_config, 


class Config:

	def read_config(self):
		config = ConfigParser.ConfigParser()
		config.read('config.ini')

		if config.get('General', 'victim_dns') == '':
			print 'ERROR: victim_dns not set'
			print_usage()
			exit()
		else:
			self.victim_dns = config.get('General', 'victim_dns')

		if config.get('General', 'victim_ip') == '':
			print 'ERROR: victim_dns not set'
			print_usage()
			exit()
		else:
			self.victim_ip = config.get('General', 'victim_ip')
		

class DbConn:
	
	def read_config(self):
		
		# use the ConfigParser
		config = ConfigParser.ConfigParser()
		config.read('config.ini')

		#TODO check if file is actually there

		# try to read the variables and save them
		if config.get('Database', 'host') == '':
			print 'ERROR: Database host not set'
			print_usage()
			exit()
		else:
			self.host = config.get('Database', 'host')

		if config.get('Database', 'user') == '':
			print 'ERROR: Database user not set'
			print_usage()
			exit()
		else:
			self.user = config.get('Database', 'user')

		if config.get('Database', 'password') == '':
			print 'ERROR: Database password not set'
			print_usage()
			exit()
		else:
			self.password = config.get('Database', 'password')

		if config.get('Database', 'database') == '':
			print 'ERROR: Database database not set'
			print_usage()
			exit()
		else:
			self.database = config.get('Database', 'database')
		return

