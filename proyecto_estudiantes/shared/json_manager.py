# ============================================================
# shared/json_manager.py  ->  CAPA DE "PERSISTENCIA"
# Se encarga solo de leer y escribir un archivo JSON.
# Así el resto del programa no necesita saber cómo se guardan los datos.
# ============================================================

# Módulo estándar para convertir entre objetos Python y texto JSON.
import json
# Módulo estándar para trabajar con rutas, carpetas y archivos del sistema.
import os


class GestorJSON:
    """
    Permite leer y guardar datos en un archivo JSON.
    """

    # Constructor: recibe la ruta del archivo que se va a administrar.
    def __init__(self, ruta):
        """
        Crea el gestor del archivo JSON.

        Args:
            ruta (str): Ruta del archivo JSON.

        Returns:
            None: No devuelve ningún valor.
        """
        # Guarda la ruta en el objeto para usarla en leer() y guardar().
        self.ruta = ruta

        # Obtiene la carpeta donde estará el archivo.
        # Ej: "data/estudiantes.json" -> "data"
        carpeta = os.path.dirname(ruta)

        # Si la carpeta no existe, la crea.
        # 'carpeta and ...' evita error cuando la ruta no tiene carpeta
        # (dirname devuelve "" en ese caso, que se considera falso).
        if carpeta and not os.path.exists(carpeta):
            # makedirs crea la carpeta (y las intermedias si hicieran falta).
            os.makedirs(carpeta)

    # Lee el archivo y devuelve su contenido como lista de diccionarios.
    def leer(self):
        """
        Lee los datos almacenados en JSON.

        Args:
            No recibe argumentos.

        Returns:
            list: Lista de diccionarios.
        """
        # Si el archivo todavía no existe, no hay datos: devuelve lista vacía.
        if not os.path.exists(self.ruta):
            return []

        # try/except: si algo falla al leer, el programa no se cae.
        try:
            # 'with' abre el archivo y garantiza que se cierre al terminar.
            # "r" = modo lectura; utf-8 permite tildes y ñ.
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                # json.load convierte el texto JSON en objetos Python.
                datos = json.load(archivo)

            # Validación: el programa espera una LISTA de registros.
            if isinstance(datos, list):
                return datos

            # Si el JSON es válido pero no es una lista (ej. un dict), se ignora.
            return []

        # JSONDecodeError: el archivo está dañado/mal formado.
        # OSError: problemas de permisos, disco, etc.
        except (json.JSONDecodeError, OSError):
            return []

    # Escribe la lista completa en el archivo (reemplaza el contenido anterior).
    def guardar(self, datos):
        """
        Guarda una lista de datos en JSON.

        Args:
            datos (list): Lista de diccionarios que se guardará.

        Returns:
            bool: True si se guardó correctamente.
        """
        try:
            # "w" = modo escritura: borra el contenido anterior y escribe de nuevo.
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                # json.dump convierte los objetos Python a texto JSON y lo escribe.
                json.dump(
                    datos,              # lo que se va a guardar
                    archivo,            # dónde se escribe
                    ensure_ascii=False, # conserva tildes y ñ (no las convierte a \u00e9)
                    indent=2            # sangría de 2 espacios para que sea legible
                )

            # Llegó hasta aquí sin errores: se guardó bien.
            return True

        # TypeError: algún dato no se puede convertir a JSON (ej. un set).
        # OSError: no se pudo escribir en el archivo.
        except (TypeError, OSError):
            return False


# Prueba de los métodos del gestor JSON.
# Solo se ejecuta con "python json_manager.py".
if __name__ == "__main__":
    print("Prueba de json_manager.py")

    # Ruta de un archivo temporal, para no tocar estudiantes.json.
    ruta_prueba = "data/prueba_manager.json"

    print("Método __init__(): crea el gestor.")
    gestor_prueba = GestorJSON(ruta_prueba)

    # Datos de ejemplo: una lista con un diccionario.
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

    # Limpieza: borra el archivo temporal de prueba.
    if os.path.exists(ruta_prueba):
        os.remove(ruta_prueba)
