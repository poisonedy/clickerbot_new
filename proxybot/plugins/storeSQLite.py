# Plugin that stores the results in SQLite

import plugins
import sqlite3


class StoreSQLite(plugins.ProxyBotPlugin):
    def __init__(self, db_path = "../data/proxies.sql"):
        self.db_path = db_path
        

    def connect (self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.commit()
        self.connection.close()


    def initDB(self):
        self.connect()
        

        self.cursor.execute(
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

        self.cursor.execute(
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
        self.disconnect()
        
    def addProxy(self, type, ip, port, country, isactive = 1):

        self.connect()


        self.cursor.execute("INSERT INTO Proxies(Type, IP, Port, Country, IsActive) VALUES (?, ?, ?, ?, ?)", (type, ip, port, country, 1))
        self.disconnect()


    def removeProxy(self, type, ip, port):
        self.connect()
        self.cursor.execute("DELETE FROM Proxies WHERE Type=? AND IP=? AND Port=?", (type, ip, port))
        self.disconnect()

    def allProxy(self):
        self.connect()
        query = self.cursor.execute("SELECT * FROM Proxies")
        rows = self.cursor.fetchall()
        self.disconnect()
        return rows
        
