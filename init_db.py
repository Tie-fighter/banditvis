#!/usr/bin/env python

import ConfigParser		# for config parsing
import MySQLdb			# for DB interaction

# check config
config = ConfigParser.ConfigParser()
config.read('config.ini')

if config.get('mySQL', 'host') == '':
	print 'ERROR: mySQL host not set'
	exit()
else:
	db_host = config.get('mySQL', 'host')

if config.get('mySQL', 'user') == '':
	print 'ERROR: mySQL user not set'
	exit()
else:
	db_user = config.get('mySQL', 'user')

if config.get('mySQL', 'password') == '':
	print 'ERROR: mySQL password not set'
	exit()
else:
	db_password = config.get('mySQL', 'password')

if config.get('mySQL', 'database') == '':
	print 'ERROR: mySQL database not set'
	exit()
else:
	db_db = config.get('mySQL', 'database')

# connect
db = MySQLdb.connect(db_host , db_user, db_password, db_db)
cursor = db.cursor()

# insert table
cursor.execute("DROP TABLE IF EXISTS bandits")
cursor.execute("

DROP TABLE IF EXISTS `bandits`;
CREATE TABLE IF NOT EXISTS `bandits` (
  `key` varchar(36) collate utf8_unicode_ci NOT NULL,
  `ip_address` varchar(16) collate utf8_unicode_ci NOT NULL,
  `offence` varchar(21) collate utf8_unicode_ci NOT NULL,
  `count` int(11) NOT NULL,
  `status` text collate utf8_unicode_ci NOT NULL,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY  (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

")

db.close()