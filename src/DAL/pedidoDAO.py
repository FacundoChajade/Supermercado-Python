class PedidoDAO():
    def __init__(self,conexion):
        self.conexion = conexion
    
    def guardar_pedido(self,pedido):
        if len(pedido.listaProductos) != 0:
            self.conexion.conectar()
            cursor = self.conexion.conn.cursor()
            cursor.execute("INSERT INTO pedido (cliente) VALUES (%s)",(pedido.cliente_id))
            try:
                pedido.id = cursor.lastrowid
                if pedido.id:
                    print("id:",pedido.id)
                else:
                    print("No se consiguió la id del pedido")
                for tupla in pedido.listaProductos:
                    cursor.execute("INSERT INTO producto_de_pedido (producto_id,pedido_id,cantidad_pedida) VALUES (%s,%s,%s)",(tupla[0].get_id(),pedido.id,tupla[1]))
                    pedido.precioTotal += tupla[0].get_precio() * tupla[1]
                cursor.execute("CALL calcular_precio_total(%s)",(pedido.id))
                self.conexion.conn.commit()
            except Exception as e:
                print("Error: ",e)
            finally:
                self.conexion.desconectar()
        else:
            print("Salida sin productos")

    def traer_pedidos(self):
        self.conexion.conectar()
        texto = ""
        cursor = self.conexion.conn.cursor()
        try:
            cursor.execute("SELECT * FROM pedido")
            resultados = cursor.fetchall()
            for fila in resultados:
                texto += f"ID: {fila[0]}, DNI del cliente: {fila[1]}, precio: {fila[2]}\n"
            return texto
        except Exception as e:
            print("Error: ",e)
        finally:
            self.conexion.desconectar()
            