# Importo tkinter para lanzar la ventana principal
import tkinter as tk
# Importo la clase de la interfaz grafica y el sistema de registro de errores
from gui import SoftwareFJApp
from modelo.registro import guardar_error, guardar_evento


def main():
    # Punto de entrada principal que arranca Software FJ asegurando que nunca se detenga sin registro
    try:
        guardar_evento("Iniciando aplicacion principal Software FJ desde main.py")
        root = tk.Tk()
        app = SoftwareFJApp(root)
        root.mainloop()
    except Exception as err:
        # Si ocurre algun fallo inesperado al iniciar la ventana lo guardo en el log
        guardar_error(err, origen="main.py")
        print(f"Error critico controlado al iniciar la aplicacion: {err}")


if __name__ == "__main__":
    main()