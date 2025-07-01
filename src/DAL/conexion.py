#pip install pymysql
import pymysql

class Conexion():
    def __init__(self):
        pass
    def restarProducto(self,producto,valor):
        conn = pymysql.connect(host='localhost', user='user', password='passwd', database='db')
        cursor = conn.cursor()
        try:
            cursor.execute("CALL restarProducto(&s,&s)",(producto,valor))
            cursor.commit()
        except Exception as e:
            print("Error: ",e)
            cursor.rollback()
        finally:
            cursor.close()
            