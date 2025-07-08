#pip install pymysql
import pymysql

class Conexion():
    def __init__(self):
        self.conn = None

    def conectar(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='', database='supermercado')
            print("Se estableció la conexión con la base de datos")
        except Exception as e:
            print("Error: ",e)

    def desconectar(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Se terminó la conexión con la base de datos")
        else:
            print("No hay conexión")
