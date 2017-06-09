import mysql.connector as connector


class DbClass:
    def __init__(self):
        self.__dsn = {
            "host": "localhost",
            "user": "user_local",
            "passwd": "user_local",
            "db": "SerreMatic_db"
        }

    def getDataFromDatabase(self, database):
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT * FROM %s ORDER BY ID DESC LIMIT 5" % database

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDetailsFromDatabase(self, database):
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT * FROM %s ORDER BY ID DESC LIMIT 10" % database

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getOneSingleRowData(self, database):
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT * FROM %s ORDER BY ID DESC LIMIT 1" % database

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def TempToDatabase(self, Tempbinnen, Tempbuiten):
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO Temperature (TempBuiten, TempBinnen, DatumTijd) VALUES ('%.2f', '%.2f', CURRENT_TIMESTAMP )" % (Tempbuiten, Tempbinnen)
        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()

    def HumidityToDatabase(self, vocht1, vocht2):
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO Humidity (Vocht1, Vocht2, DatumTijd) VALUES ('%.2f', '%.2f', CURRENT_TIMESTAMP )" % (vocht1, vocht2)
        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()

    def truncate_table(self, table_name):  # delete all data from table
        self.__connection = connector.connect(**self.__dsn)  # define connection
        self.__cursor = self.__connection.cursor()  # connect with database

        sqlQuery = "TRUNCATE TABLE %s" % table_name  # query
        self.__cursor.execute(sqlQuery)  # execute query
        self.__connection.commit()  # save changes in database
        self.__cursor.close()  # close database connection
