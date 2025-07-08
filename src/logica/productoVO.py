class ProductoVO:
    def __init__(self,id,nombre,precio,cantidad):
        self.__id = id
        self.__nombre = nombre
        self.__precio = precio
        self.__cantidad = cantidad

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_precio(self):
        return self.__precio

    def set_precio(self, precio):
        self.__precio = precio

    def get_cantidad(self):
        return self.__cantidad

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad