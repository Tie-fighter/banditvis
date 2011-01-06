#!/usr/bin/env python
# This file is part of Banditvis and licensed under GNU LGPL.

import sys				# for argument passing
import re				# for ip_address checking
import MySQLdb			# for DB interaction
import time				# for getting the time

from functions import *		# import our own functions

def print_usage():
	print 'USAGE: add_bandit.py ip_address [OFFENCE]'
	print 'additional configuration: config.ini'

read_config()

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
db = MySQLdb.connect(db_host , db_user, db_password, db_database)
cursor = db.cursor()

# increase count
now = time.strftime('%Y-%m-%d %H:%M:%S')
cursor.execute("INSERT INTO `bandits` (`key`, `ip_address`, `offence`, `count`, `status`, `last_seen`) VALUES ( '"+ip_address+'_'+offence+"', '"+ip_address+"', '"+offence+"', '1', '"+status+"', '"+now+"') ON DUPLICATE KEY UPDATE `count` = `count` + 1;")

db.close()