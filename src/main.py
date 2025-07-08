from DAL.conexion import Conexion
from DAL.pedidoDAO import PedidoDAO
from logica.pedidoVO import PedidoVO
from logica.productoVO import ProductoVO


def main():
    conexion = Conexion()
    producto = ProductoVO(1,'Fideos',1.50,2)
    pedido = PedidoVO(1)
    
    pedido.agregarProducto(producto,3,3)
    pedidoDAO = PedidoDAO(conexion)
    try:
        pedidoDAO.guardarPedido(pedido)
    except Exception as e:
        print("error: ",e)

if __name__ == "__main__":
    main()