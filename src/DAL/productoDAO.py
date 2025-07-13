from logica.productoVO import ProductoVO
class ProductoDAO:
    def __init__(self,conexion):
        self.conexion = conexion
    
    def cargar_productos(self):
        productos = []
        self.conexion.conectar()
        try:
            cursor = self.conexion.conn.cursor()
            cursor.execute("SELECT id,nombre,cantidad,precio FROM producto")
            resultados = cursor.fetchall()
            for fila in resultados:
                productos.append(ProductoVO(fila[0],fila[1],fila[3],fila[2]))
            return productos
        except Exception as e:
            print("Error: ",e)
        finally:
            self.conexion.desconectar()
    
    def aumentar_precios(self):
        self.conexion.conectar()
        try:
            cursor = self.conexion.conn.cursor()
            cursor.execute("UPDATE producto SET precio = precio * 1.05")
            self.conexion.conn.commit()
        except Exception as e:
            print("Error: ",e)
        finally:
            self.conexion.desconectar()