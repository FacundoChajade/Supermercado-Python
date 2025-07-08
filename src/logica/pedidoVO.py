class PedidoVO:
    def __init__(self,cliente_id):
        self.id = None
        self.precioTotal = 0
        self.cliente_id = cliente_id
        self.listaProductos = []

    def agregarProducto(self,producto,cantidad_recibida,cantidad_pedida):
        self.listaProductos.append((producto, cantidad_recibida, cantidad_pedida))