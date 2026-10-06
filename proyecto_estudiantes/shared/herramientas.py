# ============================================================
# shared/herramientas.py  ->  FUNCIONES DE UTILIDAD
# Funciones reutilizables para la consola: colores, títulos,
# confirmaciones y validación de email.
# ============================================================

# Módulo para interactuar con el sistema operativo (aquí: limpiar pantalla).
import os


# DICCIONARIO:
# Guarda los colores disponibles para la consola.
# Los valores son "códigos ANSI": secuencias especiales que la terminal
# interpreta como un cambio de color en el texto que viene después.
COLORES = {
    "ROJO": "\033[91m",       # rojo claro (se usa en errores)
    "VERDE": "\033[92m",      # verde claro (se usa en éxito)
    "AZUL": "\033[94m",       # azul claro (se usa en títulos)
    "AMARILLO": "\033[93m",   # amarillo claro (disponible, aún sin usar)
    "CYAN": "\033[96m",       # cian (se usa en mensajes informativos)
    "BLANCO": "\033[97m",     # blanco (color por defecto)
    "RESET": "\033[0m",       # vuelve al color normal de la terminal
}


# TUPLA:
# Contiene respuestas que se consideran afirmativas.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


# Limpia la consola para que cada pantalla del menú se vea "nueva".
def limpiar_pantalla():
    """
    Limpia la pantalla de la consola.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    # os.name vale "posix" en Linux/Mac y "nt" en Windows.
    # Linux/Mac usan el comando "clear"; Windows usa "cls".
    # os.system ejecuta ese comando en la terminal.
    os.system("clear" if os.name == "posix" else "cls")


# Imprime un texto con el color pedido.
def imprimir_color(texto, color):
    """
    Muestra un texto utilizando un color.

    Args:
        texto (str): Texto que se desea mostrar.
        color (str): Nombre del color.

    Returns:
        None: No devuelve ningún valor.
    """
    # COLORES.get(color, valor_por_defecto): busca el código del color;
    # si el nombre no existe, usa el blanco en vez de lanzar KeyError.
    codigo = COLORES.get(color, COLORES["BLANCO"])
    # Imprime: [código de color] + texto + [código RESET].
    # El RESET evita que el siguiente print siga con ese color.
    print(f"{codigo}{texto}{COLORES['RESET']}")


# Muestra un encabezado grande al inicio de cada pantalla.
def imprimir_titulo(texto):
    """
    Muestra un título en la consola.

    Args:
        texto (str): Texto que se mostrará como título.

    Returns:
        None: No devuelve ningún valor.
    """
    # Primero borra la pantalla anterior.
    limpiar_pantalla()
    # Línea superior: 60 signos "=" en azul ("=" * 60 repite el carácter 60 veces).
    imprimir_color("=" * 60, "AZUL")
    # .center(60) centra el texto dentro de un ancho de 60 caracteres.
    print(f"  {texto}".center(60))
    # Línea inferior igual a la superior.
    imprimir_color("=" * 60, "AZUL")
    # print() vacío = una línea en blanco de separación.
    print()


# Mensaje verde para operaciones exitosas.
def imprimir_exito(mensaje):
    """
    Muestra un mensaje de éxito.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    # Antepone un ✓ y lo muestra en verde.
    imprimir_color(f"✓ {mensaje}", "VERDE")


# Mensaje rojo para errores.
def imprimir_error(mensaje):
    """
    Muestra un mensaje de error.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    # Antepone un ✗ y lo muestra en rojo.
    imprimir_color(f"✗ {mensaje}", "ROJO")


# Mensaje cian para información neutral.
def imprimir_info(mensaje):
    """
    Muestra un mensaje informativo.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    # Antepone un ℹ y lo muestra en cian.
    imprimir_color(f"ℹ {mensaje}", "CYAN")


# Pregunta sí/no al usuario y devuelve True o False.
def confirmar(pregunta):
    """
    Solicita una respuesta de confirmación.

    Args:
        pregunta (str): Pregunta que se mostrará.

    Returns:
        bool: True si la respuesta es afirmativa.
    """
    # input() muestra la pregunta y espera lo que escriba el usuario.
    # .strip() quita espacios sobrantes; .lower() pasa a minúsculas
    # para que "SI", "Si" y "si" valgan igual.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    # 'in' comprueba si la respuesta está en la tupla RESPUESTAS_SI.
    # El resultado de esa comprobación (True/False) es lo que se devuelve.
    return respuesta in RESPUESTAS_SI


# Validación básica de formato de correo (no verifica que exista realmente).
def es_email_valido(texto):
    """
    Comprueba si un correo tiene un formato básico válido.

    Args:
        texto (str): Correo que se desea validar.

    Returns:
        bool: True si el correo es válido.
    """
    # Quita espacios al inicio y al final.
    texto = texto.strip()

    # Debe haber exactamente un "@". Si hay 0 o 2+, no es válido.
    if texto.count("@") != 1:
        return False

    # split("@") parte el texto en dos: lo que va antes y después del "@".
    # Ej: "ana@escuela.edu" -> usuario="ana", dominio="escuela.edu"
    usuario, dominio = texto.split("@")

    # Se devuelve True solo si se cumplen las TRES condiciones (and):
    return (
        len(usuario) > 0              # 1) hay algo antes del "@"
        and "." in dominio            # 2) el dominio contiene un punto
        and not dominio.endswith(".") # 3) el dominio no termina en punto
    )


# Prueba de las funciones de herramientas.py.
# Solo corre con "python herramientas.py".
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
    # Tiene @ y el dominio tiene punto -> True
    print("Correo válido:", es_email_valido("ana@escuela.edu"))
    # El dominio "escuela" no tiene punto -> False
    print("Correo inválido:", es_email_valido("ana@escuela"))

    # .keys() muestra solo los nombres de los colores.
    print("Variable COLORES:", COLORES.keys())
    print("Variable RESPUESTAS_SI:", RESPUESTAS_SI)
