from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error,
    imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id,
    buscar_estudiantes, actualizar_estudiante,
    eliminar_estudiante, agregar_nota, obtener_promedio,
    materias_ofertadas, estudiantes_en_comun
)

def pausa():
    """Pausa el programa.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    input("\nPresione Enter para continuar...")

def mostrar_tabla(estudiantes):
    """Muestra estudiantes en una tabla.
    Args:
        estudiantes: Lista de estudiantes.
    Returns:
        None.
    """
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<30}{'CARNET':<15}")
    print("-" * 75)

    for e in estudiantes:
        print(f"{e.id:<5}{e.obtener_nombre_completo():<25}"
              f"{e.email:<30}{e.carnet:<15}")

    print("-" * 75)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")

def opcion_crear():
    """Solicita datos y crea un estudiante.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {campo: input(f"{campo.capitalize()}: ")
             for campo in CAMPOS_ESTUDIANTE}

    exito, mensaje = crear_estudiante(datos)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

def opcion_ver_todos():
    """Muestra todos los estudiantes.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("ESTUDIANTES")
    estudiantes = obtener_todos()

    if estudiantes:
        mostrar_tabla(estudiantes)
    else:
        imprimir_info("No hay estudiantes registrados.")

    pausa()

def opcion_buscar():
    """Busca estudiantes mediante un texto.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    estudiantes = buscar_estudiantes(termino)

    if estudiantes:
        mostrar_tabla(estudiantes)
    else:
        imprimir_info("No se encontraron estudiantes.")

    pausa()

def opcion_ver_por_id():
    """Muestra un estudiante por su ID.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("VER POR ID")

    try:
        id_estudiante = int(input("ID: "))
    except ValueError:
        imprimir_error("El ID debe ser un número.")
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
    else:
        print(f"ID: {estudiante.id}")
        print(f"Nombre: {estudiante.obtener_nombre_completo()}")
        print(f"Email: {estudiante.email}")
        print(f"Carnet: {estudiante.carnet}")
        print(f"Materias: {', '.join(sorted(estudiante.materias))}")
        print(f"Promedio: {estudiante.obtener_promedio()}")

    pausa()

def opcion_actualizar():
    """Actualiza los datos de un estudiante.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

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

    cambios = {}

    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()

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

    if confirmar(f"¿Eliminar a {estudiante.obtener_nombre_completo()}?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada.")

    pausa()

def opcion_agregar_nota():
    """Agrega una nota a un estudiante.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("AGREGAR NOTA")

    try:
        id_estudiante = int(input("ID: "))
        materia = input("Materia: ")
        nota = float(input("Nota (0 - 20): "))
    except ValueError:
        imprimir_error("Los datos no tienen un formato válido.")
        pausa()
        return

    exito, mensaje = agregar_nota(id_estudiante, materia, nota)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()

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

    exito, resultado = obtener_promedio(id_estudiante)

    if exito:
        imprimir_info(f"Promedio: {resultado}")
    else:
        imprimir_error(resultado)

    pausa()

def opcion_materias_ofertadas():
    """Muestra las materias registradas.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("MATERIAS OFERTADAS")
    materias = materias_ofertadas()

    if materias:
        for materia in sorted(materias):
            print("-", materia)
    else:
        imprimir_info("No existen materias registradas.")

    pausa()

def opcion_materias_en_comun():
    """Muestra las materias compartidas por dos estudiantes.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("MATERIAS EN COMÚN")

    try:
        id_a = int(input("ID del primer estudiante: "))
        id_b = int(input("ID del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los IDs deben ser números.")
        pausa()
        return

    exito, resultado = estudiantes_en_comun(id_a, id_b)

    if exito:
        if resultado:
            print("Materias en común:")
            for materia in sorted(resultado):
                print("-", materia)
        else:
            imprimir_info("No comparten materias.")
    else:
        imprimir_error(resultado)

    pausa()

def salir():
    """Muestra el mensaje de salida.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_info("Gracias por utilizar el Sistema de Estudiantes.")

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

def mostrar_menu():
    """Muestra el menú principal.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    imprimir_titulo("SISTEMA DE ESTUDIANTES")

    for numero, funcion in OPCIONES.items():
        print(f"{numero}. {funcion.__name__.replace('opcion_', '').replace('_', ' ').title()}")

    print("0. Salir")

def main():
    """Ejecuta el menú principal.
    Args:
        No recibe argumentos.
    Returns:
        None.
    """
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "0":
            salir()
            break

        funcion = OPCIONES.get(opcion)

        if funcion:
            funcion()
        else:
            imprimir_error("Opción no válida.")
            pausa()

if __name__ == "__main__":
    print("PRUEBA DE MAIN.PY")
    print("El menú funciona así:")
    mostrar_menu()
    print("\nCantidad de estudiantes:", len(obtener_todos()))
    print("\nIniciando el sistema...")
    main()