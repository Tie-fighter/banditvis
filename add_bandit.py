#!/usr/bin/env python

import ConfigParser		# for config parsing
import sys				# for argument passing
import re				# for ip_address checking
import MySQLdb			# for DB interaction
import time				# for getting the time

def print_usage():
	print 'USAGE: add_bandit.py ip_address [OFFENCE]'
	print 'additional configuration: config.ini'


# check config
config = ConfigParser.ConfigParser()
config.read('config.ini')

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

# check arguments
if (len(sys.argv) < 2 or len(sys.argv) > 4):
	print_usage()
	exit()

if len(sys.argv) == 3:
	offence = sys.argv[2]
else:
	offence = '?'

############## TODO
status = 'idk'
##############

# check ip_address
ip_address_re = re.match('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$', sys.argv[1])

if ip_address_re == None:
		print 'ERROR: ip_address must be of form 0.0.0.0'
		print_usage()
		exit()

for group in ip_address_re.groups():
	if int(group) > 255:
		print 'ERROR: ip_address invalid'
		print_usage()
		exit()

# normalize ip
ip_address = str(int(ip_address_re.group(1))) + '.' + str(int(ip_address_re.group(2))) + '.' + str(int(ip_address_re.group(3))) + '.' + str(int(ip_address_re.group(4)))

# connect to the db
db = MySQLdb.connect(db_host , db_user, db_password, db_db)
cursor = db.cursor()

# increase count
now = time.strftime('%Y-%m-%d %H:%M:%S')
cursor.execute("INSERT INTO `bandits` (`key`, `ip_address`, `offence`, `count`, `status`, `last_seen`) VALUES ( '"+ip_address+'_'+offence+"', '"+ip_address+"', '"+offence+"', '1', '"+status+"', '"+now+"') ON DUPLICATE KEY UPDATE `count` = `count` + 1;")

db.close()