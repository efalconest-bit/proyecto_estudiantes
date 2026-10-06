import json
import os


class GestorJSON:
    """
    Permite leer y guardar datos en un archivo JSON.
    """

    def __init__(self, ruta):
        """
        Crea el gestor del archivo JSON.

        Args:
            ruta (str): Ruta del archivo JSON.

        Returns:
            None: No devuelve ningún valor.
        """
        self.ruta = ruta

        # Obtiene la carpeta donde estará el archivo.
        carpeta = os.path.dirname(ruta)

        # Si la carpeta no existe, la crea.
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        """
        Lee los datos almacenados en JSON.

        Args:
            No recibe argumentos.

        Returns:
            list: Lista de diccionarios.
        """
        if not os.path.exists(self.ruta):
            return []

        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            if isinstance(datos, list):
                return datos

            return []

        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        """
        Guarda una lista de datos en JSON.

        Args:
            datos (list): Lista de diccionarios que se guardará.

        Returns:
            bool: True si se guardó correctamente.
        """
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2
                )

            return True

        except (TypeError, OSError):
            return False


# Prueba de los métodos del gestor JSON.
if __name__ == "__main__":
    print("Prueba de json_manager.py")

    ruta_prueba = "data/prueba_manager.json"

    print("Método __init__(): crea el gestor.")
    gestor_prueba = GestorJSON(ruta_prueba)

    datos_prueba = [
        {
            "id": 1,
            "nombre": "Ana"
        }
    ]

    print("Método guardar(): guarda los datos en JSON.")
    print("Guardado:", gestor_prueba.guardar(datos_prueba))

    print("Método leer(): lee los datos del archivo.")
    print("Datos leídos:", gestor_prueba.leer())

    if os.path.exists(ruta_prueba):
        os.remove(ruta_prueba)