# ============================================================
# main.py  ->  CAPA DE "INTERFAZ" (menú en consola)
# Es el punto de entrada del programa. Pide datos con input(),
# llama a las funciones de views.py y muestra resultados con print.
# No contiene lógica de negocio: solo interacción con el usuario.
# ============================================================

# Importa la tupla de campos (nombre, apellido, email, carnet).
from models import CAMPOS_ESTUDIANTE
# Importa las funciones para imprimir con color y confirmar (sí/no).
# Los paréntesis permiten escribir el import en varias líneas.
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error,
    imprimir_info, confirmar
)
# Importa las funciones de lógica desde views.py.
from views import (
    crear_estudiante, obtener_todos, obtener_por_id,
    buscar_estudiantes, actualizar_estudiante,
    eliminar_estudiante, agregar_nota, obtener_promedio,
    materias_ofertadas, materias_en_comun
)

# Detiene el programa hasta que el usuario presione Enter.
# Sin esto, la siguiente pantalla borraría el resultado antes de leerlo.
def pausa():
    """Pausa el programa.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    # input() espera Enter; lo que se escriba se descarta.
    # "\n" al inicio deja una línea en blanco antes del mensaje.
    input("\nPresione Enter para continuar...")

# Dibuja una lista de estudiantes como tabla de texto.
def mostrar_tabla(estudiantes):
    """Muestra estudiantes en una tabla.
    Args:
        estudiantes: Lista de estudiantes.
    Returns:
        None.
    """
    # Encabezado. En un f-string, ':<5' alinea el texto a la izquierda
    # reservando 5 caracteres de ancho (25 para nombre, 30 email, 15 carnet).
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<30}{'CARNET':<15}")
    # Línea separadora de 75 guiones (5+25+30+15 = 75).
    print("-" * 75)

    # Una fila por cada estudiante.
    for e in estudiantes:
        # Las dos f-strings seguidas se unen en una sola línea de salida.
        print(f"{e.id:<5}{e.obtener_nombre_completo():<25}"
              f"{e.email:<30}{e.carnet:<15}")

    # Línea de cierre de la tabla.
    print("-" * 75)
    # Muestra cuántos estudiantes hay (len = cantidad de elementos de la lista).
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")

# Opción 1 del menú: crear un estudiante.
def opcion_crear():
    """Solicita datos y crea un estudiante.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    # Limpia la pantalla y muestra el título.
    imprimir_titulo("CREAR ESTUDIANTE")
    # Comprensión de diccionario: por cada campo de la tupla pregunta al usuario.
    # Queda así: {"nombre": "Ana", "apellido": "Pérez", ...}
    # campo.capitalize() pone la primera letra en mayúscula para el prompt.
    datos = {campo: input(f"{campo.capitalize()}: ")
             for campo in CAMPOS_ESTUDIANTE}

    # views.crear_estudiante devuelve una tupla; se "desempaqueta" en dos variables.
    exito, mensaje = crear_estudiante(datos)

    # Verde si salió bien, rojo si hubo error.
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

# Opción 2 del menú: listar todos.
def opcion_ver_todos():
    """Muestra todos los estudiantes.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("ESTUDIANTES")
    # Lista de objetos Estudiante leída del JSON.
    estudiantes = obtener_todos()

    # Una lista vacía cuenta como falsa: 'if estudiantes' = "si hay alguno".
    if estudiantes:
        mostrar_tabla(estudiantes)
    else:
        imprimir_info("No hay estudiantes registrados.")

    pausa()

# Opción 3 del menú: buscar por texto.
def opcion_buscar():
    """Busca estudiantes mediante un texto.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("BUSCAR ESTUDIANTE")
    # Pide el texto a buscar.
    termino = input("Nombre, apellido, email o carnet: ")
    # Devuelve la lista de coincidencias.
    estudiantes = buscar_estudiantes(termino)

    if estudiantes:
        mostrar_tabla(estudiantes)
    else:
        imprimir_info("No se encontraron estudiantes.")

    pausa()

# Opción 4 del menú: ver el detalle de un estudiante.
def opcion_ver_por_id():
    """Muestra un estudiante por su ID.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("VER POR ID")

    # input() siempre devuelve texto; int() lo convierte a número.
    # Si el usuario escribe algo como "abc", int() lanza ValueError.
    try:
        id_estudiante = int(input("ID: "))
    except ValueError:
        imprimir_error("El ID debe ser un número.")
        pausa()
        # 'return' sale de la función: no continúa con el resto.
        return

    # Devuelve el objeto Estudiante o None si no existe.
    estudiante = obtener_por_id(id_estudiante)

    # 'is None' es la forma correcta de comprobar None.
    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
    else:
        # Muestra cada dato del estudiante.
        print(f"ID: {estudiante.id}")
        print(f"Nombre: {estudiante.obtener_nombre_completo()}")
        print(f"Email: {estudiante.email}")
        print(f"Carnet: {estudiante.carnet}")
        # sorted() ordena las materias; ', '.join(...) las une en un solo texto.
        print(f"Materias: {', '.join(sorted(estudiante.materias))}")
        print(f"Promedio: {estudiante.obtener_promedio()}")

    pausa()

# Opción 5 del menú: actualizar datos.
def opcion_actualizar():
    """Actualiza los datos de un estudiante.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    # Pide el id y verifica que sea un número.
    try:
        id_estudiante = int(input("ID: "))
    except ValueError:
        imprimir_error("El ID debe ser un número.")
        pausa()
        return

    # Busca al estudiante para poder mostrar sus valores actuales.
    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
        pausa()
        return

    # Aquí se acumularán SOLO los campos que el usuario quiera cambiar.
    cambios = {}

    for campo in CAMPOS_ESTUDIANTE:
        # getattr(objeto, "nombre_atributo") obtiene un atributo usando
        # su nombre como texto. getattr(estudiante, "email") == estudiante.email
        actual = getattr(estudiante, campo)
        # Muestra el valor actual entre corchetes; si el usuario solo
        # presiona Enter, el texto queda vacío y ese campo no cambia.
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        # Una cadena vacía es falsa: solo entra si escribió algo.
        if nuevo:
            cambios[campo] = nuevo

    # Envía los cambios a views.py, que valida y guarda.
    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()

# Opción 6 del menú: eliminar con confirmación.
def opcion_eliminar():
    """Elimina un estudiante después de confirmar.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    try:
        id_estudiante = int(input("ID: "))
    except ValueError:
        imprimir_error("El ID debe ser un número.")
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
        pausa()
        return

    # confirmar() devuelve True si el usuario responde sí. Pide confirmación
    # antes de una acción destructiva que no se puede deshacer.
    if confirmar(f"¿Eliminar a {estudiante.obtener_nombre_completo()}?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        # El usuario respondió que no.
        imprimir_info("Operación cancelada.")

    pausa()

# Opción 7 del menú: registrar una nota.
def opcion_agregar_nota():
    """Agrega una nota a un estudiante.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("AGREGAR NOTA")

    # Los tres input() están en el mismo try: si cualquier conversión
    # falla (id no entero o nota no numérica), salta al except.
    try:
        id_estudiante = int(input("ID: "))        # id como entero
        materia = input("Materia: ")              # materia queda como texto
        nota = float(input("Nota (0 - 20): "))    # nota como decimal
    except ValueError:
        imprimir_error("Los datos no tienen un formato válido.")
        pausa()
        return

    # views.py valida el rango 0-20, que el estudiante exista, etc.
    exito, mensaje = agregar_nota(id_estudiante, materia, nota)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()

# Opción 8 del menú: ver el promedio.
def opcion_ver_promedio():
    """Muestra el promedio de un estudiante.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("VER PROMEDIO")

    try:
        id_estudiante = int(input("ID: "))
    except ValueError:
        imprimir_error("El ID debe ser un número.")
        pausa()
        return

    # 'resultado' es el promedio si exito=True, o un mensaje de error si False.
    exito, resultado = obtener_promedio(id_estudiante)

    if exito:
        imprimir_info(f"Promedio: {resultado}")
    else:
        imprimir_error(resultado)

    pausa()

# Opción 9 del menú: listar todas las materias.
def opcion_materias_ofertadas():
    """Muestra las materias registradas.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("MATERIAS OFERTADAS")
    # Devuelve un set con todas las materias sin repetir.
    materias = materias_ofertadas()

    if materias:
        # Los sets no tienen orden; sorted() las muestra alfabéticamente.
        for materia in sorted(materias):
            print("-", materia)
    else:
        imprimir_info("No existen materias registradas.")

    pausa()

# Opción 10 del menú: materias compartidas entre dos estudiantes.
def opcion_materias_en_comun():
    """Muestra las materias compartidas por dos estudiantes.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("MATERIAS EN COMÚN")

    # Pide los dos ids dentro del mismo try.
    try:
        id_a = int(input("ID del primer estudiante: "))
        id_b = int(input("ID del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los IDs deben ser números.")
        pausa()
        return

    # Si exito=True, 'resultado' es un set de materias; si no, un mensaje.
    exito, resultado = materias_en_comun(id_a, id_b)

    if exito:
        if resultado:
            print("Materias en común:")
            for materia in sorted(resultado):
                print("-", materia)
        else:
            # El set quedó vacío: no tienen materias compartidas.
            imprimir_info("No comparten materias.")
    else:
        imprimir_error(resultado)

    pausa()

# Opción 0 del menú: despedida.
def salir():
    """Muestra el mensaje de salida.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_info("Gracias por utilizar el Sistema de Estudiantes.")

# DICCIONARIO DE FUNCIONES:
# Asocia el número del menú (texto) con la función que se ejecuta.
# Las funciones se guardan SIN paréntesis: se guarda la función misma,
# no su resultado. Se ejecutarán después, con funcion().
# Esto evita una cadena larga de if/elif: para agregar una opción
# basta con añadir una línea aquí.
OPCIONES = {
    "1": opcion_crear,
    "2": opcion_ver_todos,
    "3": opcion_buscar,
    "4": opcion_ver_por_id,
    "5": opcion_actualizar,
    "6": opcion_eliminar,
    "7": opcion_agregar_nota,
    "8": opcion_ver_promedio,
    "9": opcion_materias_ofertadas,
    "10": opcion_materias_en_comun
}

# Dibuja el menú principal.
def mostrar_menu():
    """Muestra el menú principal.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("SISTEMA DE ESTUDIANTES")

    # .items() da pares (clave, valor): el número y la función.
    for numero, funcion in OPCIONES.items():
        # El texto de cada opción se genera a partir del NOMBRE de la función:
        #   funcion.__name__            -> "opcion_ver_todos"
        #   .replace('opcion_', '')     -> "ver_todos"
        #   .replace('_', ' ')          -> "ver todos"
        #   .title()                    -> "Ver Todos"
        print(f"{numero}. {funcion.__name__.replace('opcion_', '').replace('_', ' ').title()}")

    # La opción 0 no está en OPCIONES porque main() la maneja aparte.
    print("0. Salir")

# Bucle principal: mantiene el programa funcionando hasta que se elija salir.
def main():
    """Ejecuta el menú principal.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    # Bucle infinito; se corta con 'break'.
    while True:
        # Dibuja el menú.
        mostrar_menu()
        # Lee la opción elegida y le quita espacios.
        opcion = input("\nSeleccione una opción: ").strip()

        # Opción 0: despedirse y terminar el bucle.
        if opcion == "0":
            salir()
            break

        # OPCIONES.get(opcion) devuelve la función o None si la clave no existe
        # (con OPCIONES[opcion] se lanzaría KeyError).
        funcion = OPCIONES.get(opcion)

        if funcion:
            # Ejecuta la función elegida (los paréntesis la "llaman").
            funcion()
        else:
            imprimir_error("Opción no válida.")
            pausa()

# Este bloque solo corre al ejecutar "python main.py" directamente.
if __name__ == "__main__":
    # Mensajes de prueba/diagnóstico antes de arrancar.
    print("PRUEBA DE MAIN.PY")
    print("El menú funciona así:")
    mostrar_menu()
    print("\nCantidad de estudiantes:", len(obtener_todos()))
    print("\nIniciando el sistema...")
    # Arranca el programa de verdad.
    main()
