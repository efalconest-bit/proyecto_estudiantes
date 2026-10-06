import os


# DICCIONARIO:
# Guarda los colores disponibles para la consola.
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}


# TUPLA:
# Contiene respuestas que se consideran afirmativas.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    """
    Limpia la pantalla de la consola.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    """
    Muestra un texto utilizando un color.

    Args:
        texto (str): Texto que se desea mostrar.
        color (str): Nombre del color.

    Returns:
        None: No devuelve ningún valor.
    """
    codigo = COLORES.get(color, COLORES["BLANCO"])
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    """
    Muestra un título en la consola.

    Args:
        texto (str): Texto que se mostrará como título.

    Returns:
        None: No devuelve ningún valor.
    """
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    """
    Muestra un mensaje de éxito.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    """
    Muestra un mensaje de error.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    """
    Muestra un mensaje informativo.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    """
    Solicita una respuesta de confirmación.

    Args:
        pregunta (str): Pregunta que se mostrará.

    Returns:
        bool: True si la respuesta es afirmativa.
    """
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    """
    Comprueba si un correo tiene un formato básico válido.

    Args:
        texto (str): Correo que se desea validar.

    Returns:
        bool: True si el correo es válido.
    """
    texto = texto.strip()

    if texto.count("@") != 1:
        return False

    usuario, dominio = texto.split("@")

    return (
        len(usuario) > 0
        and "." in dominio
        and not dominio.endswith(".")
    )


# Prueba de las funciones de herramientas.py.
if __name__ == "__main__":
    print("Prueba de herramientas.py")

    print("Función imprimir_titulo(): muestra un título.")
    imprimir_titulo("PRUEBA DE HERRAMIENTAS")

    print("Función imprimir_exito(): muestra un mensaje de éxito.")
    imprimir_exito("Mensaje de éxito")

    print("Función imprimir_error(): muestra un mensaje de error.")
    imprimir_error("Mensaje de error")

    print("Función imprimir_info(): muestra información.")
    imprimir_info("Mensaje informativo")

    print("Función es_email_valido(): comprueba un correo.")
    print("Correo válido:", es_email_valido("ana@escuela.edu"))
    print("Correo inválido:", es_email_valido("ana@escuela"))

    print("Variable COLORES:", COLORES.keys())
    print("Variable RESPUESTAS_SI:", RESPUESTAS_SI)