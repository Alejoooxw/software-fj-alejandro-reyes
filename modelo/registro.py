# Importo logging para guardar los errores y eventos en un archivo de texto
import logging
# Importo os para crear la carpeta logs automaticamente si no existe
import os


def iniciar_log():
    # Defino la carpeta y la ruta del archivo donde quedara el historial
    carpeta = "logs"
    archivo = os.path.join(carpeta, "sistema.log")

    try:
        # Intento crear la carpeta logs sin dar error si ya existe
        os.makedirs(carpeta, exist_ok=True)
    except OSError as err:
        # Encadeno el error del sistema operativo con RuntimeError usando 'from'
        raise RuntimeError("No se pudo crear la carpeta de logs") from err
    finally:
        # Obtengo o creo nuestro cuaderno de registros principal llamado SoftwareFJ
        logger = logging.getLogger("SoftwareFJ")

    # Configuro el nivel INFO para que guarde tanto eventos normales como errores
    logger.setLevel(logging.INFO)

    # Reviso que no tenga handlers repetidos para no duplicar lineas en el archivo
    if not logger.handlers:
        # FileHandler es el mensajero que abre logs/sistema.log y escribe ahi adentro
        handler = logging.FileHandler(archivo, mode="a", encoding="utf-8")
        # Formatter define la plantilla: fecha/hora - nivel (INFO/ERROR) - mensaje
        formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        # Le asigno esa plantilla al handler de archivo
        handler.setFormatter(formato)
        # Conecto el handler al logger principal
        logger.addHandler(handler)

    # Retorno el logger ya configurado
    return logger


# Creo la instancia global para importarla facil desde cualquier archivo
log = iniciar_log()


def guardar_evento(mensaje):
    # Escribe una linea de informacion normal (INFO) en sistema.log
    log.info(mensaje)


def guardar_error(error, origen="Sistema"):
    # Escribe el nombre de la excepcion y su detalle en sistema.log sin cerrar la app
    log.error(f"[{origen}] {type(error).__name__}: {error}")