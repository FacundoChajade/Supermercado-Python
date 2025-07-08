from DAL.conexion import Conexion
from DAL.pedidoDAO import PedidoDAO
from logica.pedidoVO import PedidoVO
from logica.productoVO import ProductoVO
import random

def main():
    conexion = Conexion()
    productos = []
    productos.append(ProductoVO(1,'Fideos',1.50,2))
    productos.append(ProductoVO(2, 'Arroz', 2.00, 30))
    productos.append(ProductoVO(3, 'Agua', 1.00, 30))
    productos.append(ProductoVO(4, 'Whisky', 25.00, 30))
    productos.append(ProductoVO(5, 'Aceite', 5.00, 20))
    productos.append(ProductoVO(6, 'Don Satur', 1.25, 15))
    productos.append(ProductoVO(7, 'Prime XS', 2.50, 10))
    productos.append(ProductoVO(8, 'Opera', 1.75, 30))
    
    pedido = PedidoVO(1)
    for producto in productos:
        valorPedido = random.randint(1,5)
        pedido.agregarProducto(producto,valorPedido,valorPedido)
    pedidoDAO = PedidoDAO(conexion)
    try:
        pedidoDAO.guardarPedido(pedido)
    except Exception as e:
        print("error: ",e)

if __name__ == "__main__":
    main()