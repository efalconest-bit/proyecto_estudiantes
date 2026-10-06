# ============================================================
# views.py  ->  CAPA DE "LÓGICA / CONTROLADOR"
# Conecta el modelo (Estudiante) con el almacenamiento (JSON).
# Aquí están las operaciones CRUD: crear, leer, actualizar, eliminar,
# más validaciones. No usa input() ni imprime: eso lo hace main.py.
# Casi todas las funciones devuelven una tupla (exito, mensaje):
#   exito   -> True/False según si la operación salió bien
#   mensaje -> texto para mostrar al usuario (o un dato si exito=True)
# ============================================================

# Importa la clase Estudiante y la tupla de campos desde models.py.
from models import Estudiante, CAMPOS_ESTUDIANTE
# Importa la clase que lee/escribe el JSON.
from shared.json_manager import GestorJSON
# Importa la función que valida el formato del email.
from shared.herramientas import es_email_valido

# Gestor para leer y guardar los datos.
# Se crea UNA sola vez aquí y todas las funciones lo reutilizan.
# La ruta es relativa: hay que ejecutar el programa desde la carpeta del proyecto.
gestor = GestorJSON("data/estudiantes.json")

# TUPLAS: campos necesarios para trabajar con estudiantes.
# CAMPOS_OBLIGATORIOS: campos que no pueden quedar vacíos al crear.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
# CAMPOS_BUSCABLES: campos donde buscar_estudiantes() busca el texto.
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

# Devuelve el conjunto de carnets ya usados (para evitar duplicados).
def carnets_registrados(excepto_id=None):
    """Obtiene los carnets que ya están registrados.
    Args:
        excepto_id: ID que se puede excluir.
    Returns:
        set: Carnets registrados.
    """
    # Es una "comprensión de conjuntos" (set comprehension), con llaves {}.
    # Recorre cada registro (r) del JSON y toma su carnet:
    #   str(...)    -> lo convierte a texto (por si fuera número)
    #   .strip()    -> quita espacios
    #   .lower()    -> pasa a minúsculas (compara sin distinguir mayúsculas)
    # 'if r["id"] != excepto_id' omite al estudiante cuyo id se indique.
    # Eso sirve al ACTUALIZAR: un estudiante puede conservar su propio carnet.
    return {str(r["carnet"]).strip().lower() for r in gestor.leer()
            if r["id"] != excepto_id}

# Igual que la anterior, pero con los emails.
def emails_registrados(excepto_id=None):
    """Obtiene los emails registrados.
    Args:
        excepto_id: ID que se puede excluir.
    Returns:
        set: Emails registrados.
    """
    # Mismo mecanismo: set de emails normalizados, excluyendo opcionalmente un id.
    return {str(r["email"]).strip().lower() for r in gestor.leer()
            if r["id"] != excepto_id}

# Calcula el id que le toca al próximo estudiante.
def siguiente_id():
    """Obtiene el siguiente ID disponible.
    Args:
        No recibe argumentos.
    Returns:
        int: Siguiente ID.
    """
    # Lista con todos los ids existentes (comprensión de listas).
    ids = [r["id"] for r in gestor.leer()]
    # Si hay ids: el mayor + 1. Si no hay ninguno: empieza en 1.
    # Usar max()+1 (y no len()+1) evita repetir ids tras eliminar estudiantes.
    return max(ids) + 1 if ids else 1

# CREATE: valida los datos y guarda un estudiante nuevo.
def crear_estudiante(datos):
    """Crea y guarda un estudiante.
    Args:
        datos: Diccionario con los datos.
    Returns:
        tuple: Resultado y mensaje.
    """
    # try/except general: cualquier error inesperado se devuelve como mensaje
    # en vez de cerrar el programa.
    try:
        # Construye un diccionario {campo: valor_limpio} para cada campo.
        # datos.get(c, "") devuelve "" si el campo no vino; str() y strip() normalizan.
        valores = {c: str(datos.get(c, "")).strip() for c in CAMPOS_ESTUDIANTE}
        # Lista de campos obligatorios cuyo valor quedó vacío ("" es falso en Python).
        faltantes = [c for c in CAMPOS_OBLIGATORIOS if not valores[c]]

        # Si hay faltantes, corta aquí y avisa cuáles son.
        # ', '.join(...) une la lista con comas: "nombre, email".
        if faltantes:
            return False, f"Faltan campos: {', '.join(faltantes)}"
        # Valida el formato del email.
        if not es_email_valido(valores["email"]):
            return False, "El email no tiene un formato válido"
        # Revisa que el email no esté repetido (comparación en minúsculas).
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        # Revisa que el carnet no esté repetido.
        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        # Crea el objeto. **valores "desempaqueta" el diccionario como
        # argumentos con nombre: nombre=..., apellido=..., email=..., carnet=...
        estudiante = Estudiante(siguiente_id(), **valores)
        # Lee todos los registros actuales del JSON.
        registros = gestor.leer()
        # Agrega el nuevo estudiante (convertido a diccionario) a la lista.
        registros.append(estudiante.a_diccionario())

        # guardar() devuelve False si falló la escritura.
        if not gestor.guardar(registros):
            return False, "No se pudo guardar el estudiante"

        # Todo salió bien: devuelve True y un mensaje con el id asignado.
        return True, f"Estudiante creado con id {estudiante.id}"
    # Captura cualquier excepción y guarda el objeto de error en 'error'.
    except Exception as error:
        return False, f"Error inesperado: {error}"

# READ: devuelve todos los estudiantes como objetos Estudiante.
def obtener_todos():
    """Obtiene todos los estudiantes.
    Args:
        No recibe argumentos.
    Returns:
        list: Lista de estudiantes.
    """
    # Convierte cada diccionario del JSON en un objeto Estudiante.
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]

# READ: busca un estudiante concreto por su id.
def obtener_por_id(id_estudiante):
    """Busca un estudiante por su ID.
    Args:
        id_estudiante: ID del estudiante.
    Returns:
        Estudiante o None.
    """
    # Recorre todos los estudiantes uno por uno.
    for estudiante in obtener_todos():
        # Si el id coincide, lo devuelve y termina la función.
        if estudiante.id == id_estudiante:
            return estudiante
    # Si terminó el for sin encontrarlo, devuelve None ("nada").
    return None

# READ: búsqueda por coincidencia parcial de texto.
def buscar_estudiantes(termino):
    """Busca por nombre, apellido, email o carnet.
    Args:
        termino: Texto de búsqueda.
    Returns:
        list: Estudiantes encontrados.
    """
    # Normaliza el término: a texto, sin espacios sobrantes, en minúsculas.
    termino = str(termino).strip().lower()
    # Lista donde se acumulan los estudiantes que coinciden.
    encontrados = []

    # Si el término está vacío, devuelve lista vacía (evita devolver a todos,
    # porque "" está contenido en cualquier texto).
    if not termino:
        return encontrados

    # Revisa cada registro del JSON.
    for registro in gestor.leer():
        # Revisa cada campo buscable (nombre, apellido, email, carnet).
        for campo in CAMPOS_BUSCABLES:
            # 'termino in texto' es verdadero si el texto CONTIENE al término.
            # registro.get(campo, "") evita error si falta el campo.
            if termino in str(registro.get(campo, "")).lower():
                # Coincidió: lo convierte en objeto y lo agrega.
                encontrados.append(Estudiante.desde_diccionario(registro))
                # break sale del for de campos, para no agregar al mismo
                # estudiante dos veces si coincide en varios campos.
                break
    return encontrados

# UPDATE: modifica datos de un estudiante existente.
def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza los datos de un estudiante.
    Args:
        id_estudiante: ID del estudiante.
        cambios: Datos que se modificarán.
    Returns:
        tuple: Resultado y mensaje.
    """
    try:
        # Si el diccionario de cambios está vacío, no hay nada que hacer.
        if not cambios:
            return False, "No se indicó ningún cambio"

        # Resta de conjuntos: claves recibidas MENOS campos permitidos.
        # Lo que sobra son campos que no existen en un estudiante.
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, "Campos no válidos: " + ", ".join(desconocidos)

        # Si se quiere cambiar el email, se valida.
        if "email" in cambios:
            email = str(cambios["email"]).strip()
            # Formato correcto
            if not es_email_valido(email):
                return False, "El email no tiene un formato válido"
            # No repetido en OTROS estudiantes (se excluye el propio id).
            if email.lower() in emails_registrados(id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        # Si se quiere cambiar el carnet, se valida que no esté repetido.
        if "carnet" in cambios:
            carnet = str(cambios["carnet"]).strip()
            if carnet.lower() in carnets_registrados(id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        # Lee todos los registros para modificar uno y volver a guardarlos todos.
        registros = gestor.leer()

        # Busca el registro cuyo id coincida.
        for registro in registros:
            if registro["id"] == id_estudiante:
                # dict.update() sobrescribe solo los campos indicados.
                # La comprensión limpia cada valor (str + strip).
                registro.update({c: str(v).strip() for c, v in cambios.items()})
                # Guarda la lista completa ya modificada.
                if gestor.guardar(registros):
                    return True, "Estudiante actualizado correctamente"
                return False, "No se pudo guardar la actualización"

        # Si el for terminó sin encontrar el id, ese estudiante no existe.
        return False, f"No existe un estudiante con id {id_estudiante}"
    except Exception as error:
        return False, f"Error inesperado: {error}"

# DELETE: elimina un estudiante por id.
def eliminar_estudiante(id_estudiante):
    """Elimina un estudiante por su ID.
    Args:
        id_estudiante: ID del estudiante.
    Returns:
        tuple: Resultado y mensaje.
    """
    # Lee la lista actual.
    registros = gestor.leer()
    # Crea una lista nueva con todos MENOS el que tiene ese id (filtrado).
    nuevos = [r for r in registros if r["id"] != id_estudiante]

    # Si ambas listas miden lo mismo, no se quitó nada: el id no existía.
    if len(registros) == len(nuevos):
        return False, f"No existe un estudiante con id {id_estudiante}"

    # Guarda la lista sin el estudiante eliminado.
    if gestor.guardar(nuevos):
        return True, "Estudiante eliminado correctamente"
    return False, "No se pudo eliminar el estudiante"

# Agrega una nota a un estudiante y la guarda.
def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota a un estudiante.
    Args:
        id_estudiante: ID del estudiante.
        materia: Nombre de la materia.
        nota: Nota entre 0 y 20.
    Returns:
        tuple: Resultado y mensaje.
    """
    # Busca el estudiante (devuelve objeto o None).
    estudiante = obtener_por_id(id_estudiante)

    # Si no existe, no se puede agregar la nota.
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"
    # La nota debe ser int o float. En Python True/False también cuentan como
    # int, por eso se excluye explícitamente el tipo bool.
    if not isinstance(nota, (int, float)) or isinstance(nota, bool):
        return False, "La nota debe ser un número"
    # Rango permitido: 0 a 20.
    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20"
    # La materia no puede ser texto vacío o solo espacios.
    if not str(materia).strip():
        return False, "La materia no puede estar vacía"

    # Usa el método del modelo: agrega la nota e inscribe la materia.
    estudiante.agregar_nota(str(materia).strip(), nota)
    # Lee los registros del JSON.
    registros = gestor.leer()

    # enumerate() da el índice (i) y el registro a la vez.
    for i, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            # Reemplaza el registro viejo por el estudiante actualizado.
            registros[i] = estudiante.a_diccionario()
            # Ya encontrado: no hace falta seguir recorriendo.
            break

    # Guarda todo en el archivo.
    if gestor.guardar(registros):
        return True, "Nota agregada correctamente"
    return False, "No se pudo guardar la nota"

# Devuelve el promedio general de un estudiante.
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

    # Si existe, devuelve True y el promedio (usa el método del modelo).
    return True, estudiante.obtener_promedio()

# Reúne todas las materias que existen entre todos los estudiantes.
def materias_ofertadas():
    """Obtiene las materias sin repetir.
    Args:
        No recibe argumentos.
    Returns:
        set: Materias registradas.
    """
    # Conjunto vacío donde se irán juntando las materias.
    materias = set()

    for estudiante in obtener_todos():
        # update() agrega al conjunto todas las materias del estudiante.
        # Al ser un set, las repetidas se descartan solas.
        materias.update(estudiante.materias)

    return materias

# Devuelve las materias que comparten dos estudiantes.
def materias_en_comun(id_a, id_b):
    """Busca materias compartidas por dos estudiantes.
    Args:
        id_a: ID del primer estudiante.
        id_b: ID del segundo estudiante.
    Returns:
        tuple: Resultado y materias comunes.
    """
    # Busca a ambos estudiantes.
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    # Verifica que los dos existan, indicando cuál falta.
    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"
    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"

    # Usa la intersección de conjuntos del modelo.
    return True, estudiante_a.materias_en_comun(estudiante_b)

# Bloque de prueba: solo se ejecuta con "python views.py".
if __name__ == "__main__":
    print("PRUEBAS DE VIEWS.PY")
    print("Siguiente ID:", siguiente_id())
    print("Cantidad de estudiantes:", len(obtener_todos()))
    print("Materias ofertadas:", materias_ofertadas())

    estudiantes = obtener_todos()
    # Solo prueba con datos reales si hay al menos un estudiante.
    if estudiantes:
        estudiante = estudiantes[0]   # toma el primero de la lista
        print("Estudiante por ID:", obtener_por_id(estudiante.id))
        print("Promedio:", obtener_promedio(estudiante.id))
        print("Búsqueda:", buscar_estudiantes(estudiante.nombre))

    # Un id que no existe debe devolver None.
    print("Prueba de estudiante inexistente:")
    print(obtener_por_id(999999))
