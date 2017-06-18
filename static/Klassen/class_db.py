import mysql.connector as connector


class DbClass:
    def __init__(self):
        pass

    @staticmethod
    def connection():
        config = {
            "host": "localhost",
            "user": "user_local",
            "passwd": "user_local",
            "db": "SerreMatic_db"
        }
        try:
            c = connector.connect(**config)
            return c
        except:
            print("connection error")
            exit(1)

    @staticmethod
    def getDataFromDatabase(database):
        connection = DbClass.connection()
        cursor = connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT * FROM %s ORDER BY ID DESC LIMIT 5" % database

        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    @staticmethod
    def getDetailsFromDatabase(database):
        connection = DbClass.connection()
        cursor = connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT * FROM %s ORDER BY ID DESC LIMIT 10" % database

        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    @staticmethod
    def getOneSingleRowData(database):
        connection = DbClass.connection()
        cursor = connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT * FROM %s ORDER BY ID DESC LIMIT 1" % database

        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    @staticmethod
    def TempToDatabase(Tempbinnen, Tempbuiten):
        connection = DbClass.connection()
        cursor = connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO Temperature (TempBuiten, TempBinnen, DatumTijd) VALUES ('%.2f', '%.2f', CURRENT_TIMESTAMP )" % (Tempbuiten, Tempbinnen)
        cursor.execute(sqlQuery)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def HumidityToDatabase(vocht1, vocht2):
        connection = DbClass.connection()
        cursor = connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO Humidity (Vocht1, Vocht2, DatumTijd) VALUES ('%.2f', '%.2f', CURRENT_TIMESTAMP )" % (vocht1, vocht2)
        cursor.execute(sqlQuery)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def SettingsToDatabase(temp, humidity):
        connection = DbClass.connection()
        cursor = connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO Settings (GewensteTemp, GewensteHumidity) VALUES ('%.2f', '%.2f')" % (temp, humidity)
        cursor.execute(sqlQuery)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def truncate_table(table_name):  # delete all data from table
        connection = DbClass.connection()
        cursor = connection.cursor()  # connect with database

        sqlQuery = "TRUNCATE TABLE %s" % table_name  # query
        cursor.execute(sqlQuery)  # execute query
        connection.commit()  # save changes in database
        cursor.close()  # close database connection
        connection.close()


