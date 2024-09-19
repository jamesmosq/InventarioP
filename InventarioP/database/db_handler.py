import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, TABLE_NAME, COLUMNS

class DatabaseHandler:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conectado a la base de datos MySQL")
                self.create_table()
        except Error as e:
            print(f"Error al conectarse a MySQL: {e}")
            raise

    def create_table(self):
        columns = ", ".join([f"{name} {data_type}" for name, data_type in COLUMNS])
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {columns}
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table {TABLE_NAME} created successfully")
        except Error as e:
            print(f"Error al crear la tabla: {e}")
            raise

    def insert_product(self, name, brand, reference, price, quantity):
        insert_query = f"""
        INSERT INTO {TABLE_NAME} (name, brand, reference, price, quantity)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_query, (name, brand, reference, price, quantity))
            self.connection.commit()
            print("Producto insertado exitosamente")
        except Error as e:
            print(f"Error al insertar el producto: {e}")
            raise

    def get_all_products(self):
        select_query = f"SELECT * FROM {TABLE_NAME}"
        try:
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al recuperar productos: {e}")
            raise

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("La conexión MySQL está cerrada")