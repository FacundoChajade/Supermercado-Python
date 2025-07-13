import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.productoVO import ProductoVO
from models.pedidoVO import PedidoVO
from DAL.conexion import Conexion
from DAL.pedidoDAO import PedidoDAO 
from DAL.productoDAO import ProductoDAO
import multiprocessing as mp
import threading as th
import os
import time

# Funciones de lógica (idénticas a main.py)
def accion_cliente(pedido, condicion, conexion):
    with condicion:
        condicion.wait()
        pedidoDAO = PedidoDAO(conexion)
        pedidoDAO.guardar_pedido(pedido)

def cargar_productos(evento, productos_compartidos, conexion):
    productoDAO = ProductoDAO(conexion)
    productos = productoDAO.cargar_productos()
    productos_compartidos.extend(productos) 
    evento.set()
    print("terminó repositor")

def inflacion(aumento, conexion):
    productoDAO = ProductoDAO(conexion)
    with aumento:
        aumento.wait()
        productoDAO.aumentar_precios()

def registrar_pedidos(conexion):
    pedidoDAO = PedidoDAO(conexion)
    with open("registros.txt", 'w') as archivo:
        archivo.write(pedidoDAO.traer_pedidos())

class SupermercadoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supermercado")  # Cambia el título de la ventana principal
        self.geometry("500x400")  # Define el tamaño de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Maneja el cierre seguro de la ventana
        self.conexion = Conexion()
        self.manager = mp.Manager()
        self.productos_compartidos = self.manager.list()
        self.productos_cargados = mp.Event()
        self.aumento = mp.Condition()
        # Lanzar procesos concurrentes
        self.repositor = mp.Process(target=cargar_productos, args=(self.productos_cargados, self.productos_compartidos, self.conexion))
        self.encarecimiento = mp.Process(target=inflacion, args=(self.aumento, self.conexion))
        self.anotador = mp.Process(target=registrar_pedidos, args=(self.conexion,))
        self.anotador.start()
        self.encarecimiento.start()
        self.repositor.start()
        self.productos_cargados.wait()  # Esperar a que el repositor cargue los productos
        self.productos = list(self.productos_compartidos)
        self.pedidos = []
        self.cant_clientes = 0
        self.num_cliente = 0
        self.dnis = []
        self.frames = []
        self.show_inicio()

    def show_inicio(self):
        self.clear_frames()
        frame = tk.Frame(self)  # Crea un contenedor para agrupar widgets
        frame.pack(expand=True, fill="both")  # Hace que el frame ocupe todo el espacio disponible
        tk.Label(frame, text="Supermercado", font=("Arial", 18)).pack(pady=10)  # Muestra un texto estático
        tk.Label(frame, text="¿Qué desea realizar?").pack(pady=10)  # Muestra otro texto
        btn1 = tk.Button(frame, text="Ingresar pedidos", command=self.show_cant_clientes)  # Botón que llama a una función
        btn1.pack(pady=5)  # Coloca el botón en el frame
        btn2 = tk.Button(frame, text="Ver informes", command=self.show_informes)  # Otro botón
        btn2.pack(pady=5)     
        self.frames.append(frame)

    def show_cant_clientes(self):
        self.clear_frames()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text="Ingrese la cantidad de clientes que harán su pedido:").pack(pady=10)
        spin = tk.Spinbox(frame, from_=1, to=20, width=5)  # Caja para seleccionar un número
        spin.pack(pady=5)
        btn = tk.Button(frame, text="Siguiente", command=lambda: self.start_pedidos(int(spin.get()))) #Se usa lambda para pasar el valor del spinbox a la función start_pedidos y no se usa self.start_pedidos(int(spin.get())) porque se ejecuta inmediatamente y no se espera a que el usuario haga click en el botón
        btn.pack(pady=10)
        self.frames.append(frame)

    def start_pedidos(self, cant):
        self.cant_clientes = cant
        self.num_cliente = 0
        self.pedidos = []
        self.dnis = []
        # Recargar productos desde la base de datos (como el main)
        self.productos_compartidos = self.manager.list()
        self.productos_cargados = mp.Event()
        self.repositor = mp.Process(target=cargar_productos, args=(self.productos_cargados, self.productos_compartidos, self.conexion))
        self.repositor.start()
        self.productos_cargados.wait()
        self.productos = list(self.productos_compartidos)
        self.show_canasta()

    def show_canasta(self):
        self.clear_frames()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text="Canasta (Stock disponible)", font=("Arial", 14)).pack(pady=10)
        for prod in self.productos:
            info = f"{prod.get_nombre()} : {prod.get_cantidad()}u  {prod.get_precio()}usd"
            tk.Label(frame, text=info).pack(anchor="center")
        btn = tk.Button(frame, text="Siguiente", command=self.show_dni_cliente)
        btn.pack(pady=15)
        self.frames.append(frame)

    def show_dni_cliente(self):
        self.clear_frames()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text=f"Cliente N°{self.num_cliente+1}", font=("Arial", 14)).pack(pady=10)
        tk.Label(frame, text="Ingrese su DNI:").pack(pady=5)
        dni_var = tk.StringVar() #StringVar es una clase que permite almacenar un valor de tipo string
        entry = tk.Entry(frame, textvariable=dni_var)  # Campo de texto para ingresar datos
        entry.pack(pady=5)
        entry.focus()  # Pone el foco en el campo de texto
        def validar_y_continuar():
            try:
                dni = int(dni_var.get())
                if dni < 1:
                    raise ValueError("Ingrese un DNI válido (número mayor a 0)")
                self.dnis.append(dni)
                self.show_pedido_cliente()
            except ValueError as e:
                messagebox.showerror("Error", e)
        btn = tk.Button(frame, text="Siguiente", command=validar_y_continuar)
        btn.pack(pady=10)
        self.frames.append(frame)

    def show_pedido_cliente(self):
        self.clear_frames()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text=f"Cliente N°{self.num_cliente+1}", font=("Arial", 14)).pack(pady=10)
        tk.Label(frame, text="Canasta").pack()
        entries = []
        for prod in self.productos:
            fila = tk.Frame(frame)  # Crea una fila para cada producto
            fila.pack(pady=2)
            tk.Label(fila, text=f"{prod.get_nombre()} ({prod.get_precio()}usd)").pack(side="left")  # Etiqueta para el producto
            var = tk.IntVar(value=0)  # Variable entera para el spinbox
            spin = tk.Spinbox(fila, from_=0, to=prod.get_cantidad(), width=5, textvariable=var)  # Spinbox para cantidad
            spin.pack(side="left", padx=5)
            entries.append((prod, var))
        total_label = tk.Label(frame, text="Total: $0")  # Etiqueta para mostrar el total
        total_label.pack(pady=5)
        def update_total(*args):
            total = 0
            for prod, var in entries:
                try:
                    total += int(var.get()) * prod.get_precio()
                except:
                    pass
            total_label.config(text=f"Total: ${total}")
        for _, var in entries:
            var.trace_add('write', update_total)
        btn = tk.Button(frame, text="Enviar", command=lambda: self.guardar_pedido(entries))
        btn.pack(pady=10)
        self.frames.append(frame)

    def guardar_pedido(self, entries):
        pedido = PedidoVO(self.dnis[self.num_cliente])
        for prod, var in entries:
            cantidad = int(var.get())
            if cantidad > 0:
                pedido.agregarProducto(prod, cantidad)
        self.pedidos.append(pedido)
        self.num_cliente += 1
        if self.num_cliente < self.cant_clientes:
            self.show_dni_cliente()
        else:
            self.procesar_pedidos_concurrentes()

    def procesar_pedidos_concurrentes(self):
        condicion = th.Condition()
        clientes = []
        for pedido in self.pedidos:
            clientes.append(th.Thread(target=accion_cliente, args=(pedido, condicion, self.conexion)))
        for cliente in clientes:
            cliente.start()
        messagebox.showinfo("Simulación", "Se van a procesar los pedidos de todos los clientes.")  # Muestra un mensaje informativo
        with condicion:
            condicion.notify_all()
        for cliente in clientes:
            cliente.join()
        # Notificar inflación
        with self.aumento:
            self.aumento.notify()
        # Registrar pedidos (proceso)
        self.anotador = mp.Process(target=registrar_pedidos, args=(self.conexion,))
        self.anotador.start()
        self.anotador.join()
        self.show_informes()

    def show_informes(self):
        self.clear_frames()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text="Informes", font=("Arial", 16)).pack(pady=10)
        informe = ""
        if os.path.exists("registros.txt"):
            with open("registros.txt", "r") as f:
                informe = f.read()
        text = tk.Text(frame, height=15, width=60)  # Área de texto multilínea
        text.insert("1.0", informe)  # Inserta texto en el área de texto
        text.config(state="disabled")  # Hace el área de texto de solo lectura
        text.pack(pady=5)
        btn_volver = tk.Button(frame, text="Volver inicio", command=self.show_inicio)
        btn_volver.pack(pady=15)
        self.frames.append(frame)

    def show_detalle_pedido(self, idx):
        pass

    def clear_frames(self):
        for frame in self.frames:
            frame.destroy()
        self.frames = []

    def on_close(self):
        try:
            if self.repositor.is_alive():
                self.repositor.terminate()
            if self.encarecimiento.is_alive():
                with self.aumento:
                    self.aumento.notify()
                self.encarecimiento.terminate()
            if self.anotador.is_alive():
                self.anotador.terminate()
        except:
            pass
        self.destroy()
