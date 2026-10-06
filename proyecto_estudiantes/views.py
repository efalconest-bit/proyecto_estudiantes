from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

# Gestor para leer y guardar los datos.
gestor = GestorJSON("data/estudiantes.json")

# TUPLAS: campos necesarios para trabajar con estudiantes.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

def carnets_registrados(excepto_id=None):
    """Obtiene los carnets que ya están registrados.
    Args:
        excepto_id: ID que se puede excluir.
    Returns:
        set: Carnets registrados.
    """
    return {str(r["carnet"]).strip().lower() for r in gestor.leer()
            if r["id"] != excepto_id}

def emails_registrados(excepto_id=None):
    """Obtiene los emails registrados.
    Args:
        excepto_id: ID que se puede excluir.
    Returns:
        set: Emails registrados.
    """
    return {str(r["email"]).strip().lower() for r in gestor.leer()
            if r["id"] != excepto_id}

def siguiente_id():
    """Obtiene el siguiente ID disponible.
    Args:
        No recibe argumentos.
    Returns:
        int: Siguiente ID.
    """
    ids = [r["id"] for r in gestor.leer()]
    return max(ids) + 1 if ids else 1

def crear_estudiante(datos):
    """Crea y guarda un estudiante.
    Args:
        datos: Diccionario con los datos.
    Returns:
        tuple: Resultado y mensaje.
    """
    try:
        valores = {c: str(datos.get(c, "")).strip() for c in CAMPOS_ESTUDIANTE}
        faltantes = [c for c in CAMPOS_OBLIGATORIOS if not valores[c]]

        if faltantes:
            return False, f"Faltan campos: {', '.join(faltantes)}"
        if not es_email_valido(valores["email"]):
            return False, "El email no tiene un formato válido"
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        estudiante = Estudiante(siguiente_id(), **valores)
        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())

        if not gestor.guardar(registros):
            return False, "No se pudo guardar el estudiante"

        return True, f"Estudiante creado con id {estudiante.id}"
    except Exception as error:
        return False, f"Error inesperado: {error}"

def obtener_todos():
    """Obtiene todos los estudiantes.
    Args:
        No recibe argumentos.
    Returns:
        list: Lista de estudiantes.
    """
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]

def obtener_por_id(id_estudiante):
    """Busca un estudiante por su ID.
    Args:
        id_estudiante: ID del estudiante.
    Returns:
        Estudiante o None.
    """
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None

def buscar_estudiantes(termino):
    """Busca por nombre, apellido, email o carnet.
    Args:
        termino: Texto de búsqueda.
    Returns:
        list: Estudiantes encontrados.
    """
    termino = str(termino).strip().lower()
    encontrados = []

    if not termino:
        return encontrados

    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados

def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza los datos de un estudiante.
    Args:
        id_estudiante: ID del estudiante.
        cambios: Datos que se modificarán.
    Returns:
        tuple: Resultado y mensaje.
    """
    try:
        if not cambios:
            return False, "No se indicó ningún cambio"

        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, "Campos no válidos: " + ", ".join(desconocidos)

        if "email" in cambios:
            email = str(cambios["email"]).strip()
            if not es_email_valido(email):
                return False, "El email no tiene un formato válido"
            if email.lower() in emails_registrados(id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        if "carnet" in cambios:
            carnet = str(cambios["carnet"]).strip()
            if carnet.lower() in carnets_registrados(id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()

        for registro in registros:
            if registro["id"] == id_estudiante:
                registro.update({c: str(v).strip() for c, v in cambios.items()})
                if gestor.guardar(registros):
                    return True, "Estudiante actualizado correctamente"
                return False, "No se pudo guardar la actualización"

        return False, f"No existe un estudiante con id {id_estudiante}"
    except Exception as error:
        return False, f"Error inesperado: {error}"

def eliminar_estudiante(id_estudiante):
    """Elimina un estudiante por su ID.
    Args:
        id_estudiante: ID del estudiante.
    Returns:
        tuple: Resultado y mensaje.
    """
    registros = gestor.leer()
    nuevos = [r for r in registros if r["id"] != id_estudiante]

    if len(registros) == len(nuevos):
        return False, f"No existe un estudiante con id {id_estudiante}"

    if gestor.guardar(nuevos):
        return True, "Estudiante eliminado correctamente"
    return False, "No se pudo eliminar el estudiante"

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota a un estudiante.
    Args:
        id_estudiante: ID del estudiante.
        materia: Nombre de la materia.
        nota: Nota entre 0 y 20.
    Returns:
        tuple: Resultado y mensaje.
    """
    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"
    if not isinstance(nota, (int, float)) or isinstance(nota, bool):
        return False, "La nota debe ser un número"
    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20"
    if not str(materia).strip():
        return False, "La materia no puede estar vacía"

    estudiante.agregar_nota(str(materia).strip(), nota)
    registros = gestor.leer()

    for i, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            registros[i] = estudiante.a_diccionario()
            break

    if gestor.guardar(registros):
        return True, "Nota agregada correctamente"
    return False, "No se pudo guardar la nota"

def obtener_promedio(id_estudiante):
    """Obtiene el promedio de un estudiante.
    Args:
        id_estudiante: ID del estudiante.
    Returns:
        tuple: Resultado y promedio o mensaje.
    """
    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    return True, estudiante.obtener_promedio()

def materias_ofertadas():
    """Obtiene las materias sin repetir.
    Args:
        No recibe argumentos.
    Returns:
        set: Materias registradas.
    """
    materias = set()

    for estudiante in obtener_todos():
        materias.update(estudiante.materias)

    return materias

def estudiantes_en_comun(id_a, id_b):
    """Busca materias compartidas por dos estudiantes.
    Args:
        id_a: ID del primer estudiante.
        id_b: ID del segundo estudiante.
    Returns:
        tuple: Resultado y materias comunes.
    """
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"
    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"

    return True, estudiante_a.materias_en_comun(estudiante_b)

if __name__ == "__main__":
    print("PRUEBAS DE VIEWS.PY")
    print("Siguiente ID:", siguiente_id())
    print("Cantidad de estudiantes:", len(obtener_todos()))
    print("Materias ofertadas:", materias_ofertadas())

    estudiantes = obtener_todos()
    if estudiantes:
        estudiante = estudiantes[0]
        print("Estudiante por ID:", obtener_por_id(estudiante.id))
        print("Promedio:", obtener_promedio(estudiante.id))
        print("Búsqueda:", buscar_estudiantes(estudiante.nombre))

    print("Prueba de estudiante inexistente:")
    print(obtener_por_id(999999))