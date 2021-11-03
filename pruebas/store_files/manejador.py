import sqlite3


class manejador:
    def __init__(self, db_name):
        self.db_name = db_name
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        sql_create_table_query = """
        CREATE TABLE IF NOT EXISTS datos (name TEXT NOT NULL, data BLOB);
        """
        cursor.execute(sql_create_table_query)
        connection.commit()
        connection.close()

    def agregar(self, binario, nombre):
        # Establish a connection
        connection = sqlite3.connect(self.db_name)

        # Create a cursor object
        cursor = connection.cursor()

        sqlite_insert_blob_query = f"""
        INSERT INTO datos (name, data) VALUES (?, ?)
        """
        data_tuple = (nombre, binario)
        # Execute the query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        connection.commit()
        print('File inserted successfully')
        cursor.close()
        connection.close()

    def leer(self, nombre):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        sql_retrieve_file_query = f"""SELECT * FROM datos WHERE name = ?"""
        cursor.execute(sql_retrieve_file_query, (nombre,))

        data = cursor.fetchone()

        connection.commit()
        connection.close()

        return data