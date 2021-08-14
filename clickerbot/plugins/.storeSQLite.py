# Plugin that stores the results in SQLite

import plugins
import sqlite3


class StoreSQLite(plugins.ClickerBotPlugin):
    def __init__(self, db_path = "../data/backend.db"):
    	self.db_path = db_path
    	self.connection = sqlite3.connect(self.db_path)

    def initDB(self):
    	cursor = self.connection.cursor()

    	cursor.execute(
    		'''
	    		CREATE TABLE IF NOT EXISTS Proxies (
	    		ProxyID INTEGER NOT NULL PRIMARY KEY, 
	    		Type TEXT NOT NULL, 
	    		IP TEXT NOT NULL, 
	    		Port TEXT NOT NULL, 
	    		Country TEXT, 
	    		Latency INT, 
	    		LastUsed TEXT, 
	    		LastChecked TEXT, 
	    		IsActive BOOLEAN NOT NULL CHECK (IsActive IN (0, 1))
	    		)
	    	'''
    		)

    	cursor.execute(
    		'''
	    		CREATE TABLE IF NOT EXISTS Clicks (
	    		ClickID INTEGER NOT NULL PRIMARY KEY, 
	    		ProxyID INTEGER NOT NULL, 
	    		ClickedDate TEXT, 
	    		StatusCode INT, 
	    		PictureBefore BLOB, 
	    		PictureAfter BLOB
	    		)
    		'''
	    	)

    	self.connection.commit()
    	self.connection.close()

    def addProxy(self, type, ip, port, country, isactive = 1):
    	cursor = self.connection.cursor()

    	cursor.execute("INSERT INTO Proxies(Type, IP, Port, IsActive) VALUES (?, ?, ?, ?)", (type, ip, port, 1))
    	self.connection.commit()
    	self.connection.close()

	#def addBeforeImage(self, image):