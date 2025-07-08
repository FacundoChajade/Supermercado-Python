from DAL.conexion import Conexion

def main():
    conexion = Conexion()
    conexion.conectar()
    conexion.desconectar()

if __name__ == "__main__":
    main()