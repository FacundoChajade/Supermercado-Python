class PedidoDAO():
    def __init__(self,conexion):
        self.conexion = conexion
    
    def guardarPedido(self,pedido):
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
                cursor.execute("INSERT INTO producto_has_pedido (producto_id,pedido_id,cantidad_pedida,cantidad_recibida) VALUES (%s,%s,%s,%s)",(tupla[0].get_id(),pedido.id,tupla[2],tupla[1]))
                pedido.precioTotal += tupla[0].get_precio() * tupla[1]
            cursor.execute("UPDATE pedido SET precioFinal=%s WHERE id = %s",(pedido.precioTotal,pedido.id))
            self.conexion.conn.commit()
        except Exception as e:
            print("Error: ",e)
        finally:
            self.conexion.desconectar()
