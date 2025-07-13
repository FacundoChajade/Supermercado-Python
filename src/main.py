from DAL.conexion import Conexion
from DAL.pedidoDAO import PedidoDAO
from DAL.productoDAO import ProductoDAO
from logica.pedidoVO import PedidoVO
from logica.productoVO import ProductoVO
import multiprocessing as mp
import threading as th
import os

def accion_cliente(pedido, condicion,conexion):
    with condicion:
        condicion.wait()
        pedidoDAO = PedidoDAO(conexion)
        pedidoDAO.guardar_pedido(pedido)
    
def cargar_productos(evento,productos_compartidos,conexion):
    productoDAO = ProductoDAO(conexion)
    productos = productoDAO.cargar_productos()
    productos_compartidos.extend(productos)
    evento.set()
    print("terminó repositor")

def inflacion(aumento,conexion):
    productoDAO = ProductoDAO(conexion)
    with aumento:
        aumento.wait()
        productoDAO.aumentar_precios()


def registrar_pedidos(conexion):
    pedidoDAO = PedidoDAO(conexion)
    with open("registros.txt", 'w') as archivo:
        archivo.write(pedidoDAO.traer_pedidos())
        

def main():
    global productos
    conexion = Conexion()
    aumento = mp.Condition()
    while True:
        manager = mp.Manager()
        productos_compartidos = manager.list()
        productos_cargados = mp.Event()
        repositor = mp.Process(target=cargar_productos, args=(productos_cargados,productos_compartidos,conexion))
        encarecimiento = mp.Process(target=inflacion,args=(aumento,conexion))
        anotador = mp.Process(target=registrar_pedidos,args=(conexion,))
        anotador.start()
        encarecimiento.start()
        repositor.start()
        opcion = int(input("Que desea realizar: 1-Ingresar pedidos 2-Ver pedidos 3-Salir "))
        if opcion < 1 or opcion > 3:
            raise ValueError("Ingrese una opcion valida")
        
        if opcion == 1:
            condicion = th.Condition()
            clientes = []
            try:
                cant_clientes = int(input("Cuantos clientes hay? "))
                if cant_clientes <= 0:
                    raise ValueError("No se puede poner un valor menor ni igual a 0")
            except ValueError as ve:
                print("Error: ",ve)
            except Exception as e:
                print("Error: ",e)
            

            productos = list(productos_compartidos)
            
            for _ in range(cant_clientes):
                while True:
                    try:
                        dni = int(input("Ingrese su DNI: "))
                        if dni < 1:
                            raise ValueError("Ingrese una opcion valida")
                        break
                    except ValueError as ve:
                        print("Error: ",ve)
                pedido = PedidoVO(dni)
                cantidades = {}
                for producto in productos:
                    cantidades[producto] = 0
                while True: 
                    os.system("cls")
                    contador = 0
                    print("Para salir ingrese 0")
                    for producto in productos:
                        contador += 1
                        print(f"{contador}-Producto: {producto.get_nombre()}\nPrecio: {producto.get_precio()}")
                    try:
                        eleccion = int(input("Seleccione un producto: "))
                        if eleccion < 0 or eleccion > len(productos):
                            raise ValueError("Seleccione un valor dentro de los parametros")
                        if eleccion == 0:
                            break
                        cantidad = int(input("Ingrese la cantidad deseada del producto: "))
                        if cantidad < 0:
                            raise ValueError("No se puede ingresar una cantidad negativa")
                        cantidades[productos[eleccion-1]] += cantidad
                        
                    except ValueError as ve:
                        print("Error: ",ve)
                    except Exception as e:
                        print("Error: ", e)
                try:
                    for clave in cantidades:
                        if cantidades[clave] != 0:
                            pedido.agregarProducto(clave, cantidades[clave])
                        else:
                            print("No entró")
                except ValueError as ve:
                    print("Error: ",ve)
                except Exception as e:
                    print("Error: ", e)
                clientes.append(th.Thread(target=accion_cliente, args=(pedido,condicion,conexion)))
            
            
            for cliente in clientes:
                cliente.start()
            print("Presione cualquier tecla para inciar con la simulacion")
            os.system("pause")
            with condicion:
                condicion.notify_all()
            for cliente in clientes:
                cliente.join()
            with aumento:
                aumento.notify()
            
        elif opcion == 2:
            os.startfile("registros.txt")
            continue


        elif opcion == 3:
            with aumento:
                aumento.notify()
            break
        
        repositor.join()
        encarecimiento.join()
        anotador.join()

if __name__ == "__main__":
    main()