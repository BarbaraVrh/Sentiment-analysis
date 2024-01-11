import pyodbc

# This class manages the Azure SQL DB connection
class SQLConnection(object):
    __instance = None
    __connection = None

    def __new__(cls):
        if SQLConnection.__instance is None:
            SQLConnection.__instance = object.__new__(cls)        
        return SQLConnection.__instance  

    def getConnection(self):

        server = 'your_sql_server'
        database = 'your_db_name'
        username = 'your_username'
        password = 'your_password'
        driver= '{ODBC Driver 18 for SQL Server}'

        if (self.__connection == None):
            self.__connection = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        
        return self.__connection
    
    def removeConnection(self):
        self.__connection = None
