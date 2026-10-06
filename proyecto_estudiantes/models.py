# ============================================================
# models.py  ->  CAPA DE "MODELO"
# Aquí se define QUÉ es un estudiante (sus datos y su comportamiento).
# No pide datos al usuario ni guarda archivos: solo describe la clase.
# ============================================================

# TUPLA:
# Contiene los campos principales de un estudiante.
# Se utiliza una tupla porque los nombres de los campos son fijos.
# (una tupla es inmutable: nadie puede agregarle o quitarle campos por error)
# Se importa en main.py y views.py para recorrer los campos con un for.
CAMPOS_ESTUDIANTE = (
    "nombre",      # Campo 1: nombre de pila
    "apellido",    # Campo 2: apellido
    "email",       # Campo 3: correo electrónico
    "carnet"       # Campo 4: código/identificación del estudiante
)


# 'class' define una clase: un molde para crear objetos de tipo Estudiante.
class Estudiante:
    """
    Representa a un estudiante y sus datos académicos.
    """

    # __init__ es el CONSTRUCTOR: se ejecuta automáticamente cada vez que
    # escribes Estudiante(...). Recibe los datos y los guarda en el objeto.
    def __init__(
        self,                # 'self' es el objeto que se está creando (se pasa solo)
        id_estudiante,       # número único que identifica al estudiante
        nombre,              # nombre de pila
        apellido,            # apellido
        email,               # correo electrónico
        carnet,              # carnet del estudiante
        notas=None,          # parámetro opcional: diccionario de notas (por defecto None)
        materias=None        # parámetro opcional: materias inscritas (por defecto None)
    ):
        """
        Crea un objeto Estudiante.

        Args:
            id_estudiante (int): Identificador del estudiante.
            nombre (str): Nombre del estudiante.
            apellido (str): Apellido del estudiante.
            email (str): Correo electrónico.
            carnet (str): Carnet del estudiante.
            notas (dict): Materias y listas de notas.
            materias (set): Materias inscritas.

        Returns:
            None: No devuelve ningún valor.
        """

        # Guarda el id dentro del objeto como atributo (self.id).
        # Se llama distinto al parámetro porque 'id' es una función de Python.
        self.id = id_estudiante
        # Guarda el nombre en el atributo del objeto.
        self.nombre = nombre
        # Guarda el apellido.
        self.apellido = apellido
        # Guarda el correo.
        self.email = email
        # Guarda el carnet.
        self.carnet = carnet

        # DICCIONARIO:
        # Relaciona cada materia con sus notas.
        # Ejemplo: {"Matemática": [18, 20], "Inglés": [17]}
        # 'notas if notas else {}' significa: si llegaron notas úsalas;
        # si es None (o vacío) crea un diccionario nuevo vacío.
        # Se evita usar {} como valor por defecto en la firma porque ese
        # diccionario se compartiría entre TODOS los estudiantes (bug clásico).
        self.notas = notas if notas else {}

        # CONJUNTO:
        # Guarda las materias sin repetir.
        # set(materias) convierte lo que llegue (lista, set...) en conjunto.
        # Si no llegó nada, crea un conjunto vacío con set().
        self.materias = set(materias) if materias else set()

    # Método de instancia: se llama sobre un estudiante concreto.
    def obtener_nombre_completo(self):
        """
        Obtiene el nombre completo del estudiante.

        Args:
            No recibe argumentos.

        Returns:
            str: Nombre y apellido del estudiante.
        """
        # f-string: mete los valores de las variables dentro del texto.
        # Devuelve, por ejemplo, "Ana Pérez".
        return f"{self.nombre} {self.apellido}"

    # Método que agrega una materia al conjunto de materias inscritas.
    def inscribir_materia(self, materia):
        """
        Inscribe al estudiante en una materia.

        Args:
            materia (str): Nombre de la materia.

        Returns:
            None: No devuelve ningún valor.
        """

        # add() agrega la materia y evita duplicados.
        # Si la materia ya estaba en el conjunto, no pasa nada.
        self.materias.add(materia)

    # Método que registra una nota para una materia.
    def agregar_nota(self, materia, nota):
        """
        Agrega una nota a una materia.

        Args:
            materia (str): Nombre de la materia.
            nota (int o float): Nota obtenida.

        Returns:
            None: No devuelve ningún valor.
        """

        # Al agregar una nota también se registra la materia.
        # Así una materia con notas siempre aparece en self.materias.
        self.inscribir_materia(materia)

        # Si la materia no existe, crea una lista.
        # setdefault(materia, []) devuelve la lista de esa materia; si la
        # clave no existe, primero la crea con una lista vacía.
        # Luego .append(nota) añade la nota al final de esa lista.
        self.notas.setdefault(materia, []).append(nota)

    # Método que calcula el promedio general (de todas las materias juntas).
    def obtener_promedio(self):
        """
        Calcula el promedio de todas las notas.

        Args:
            No recibe argumentos.

        Returns:
            float: Promedio de las notas.
        """

        # LISTA:
        # Guarda todas las notas para calcular el promedio.
        # Empieza vacía y se llena en el for de abajo.
        todas = []

        # .values() devuelve solo las listas de notas (sin los nombres de materia).
        for lista_notas in self.notas.values():
            # extend() agrega TODOS los elementos de lista_notas a 'todas'
            # (a diferencia de append, que agregaría la lista entera como un solo elemento).
            todas.extend(lista_notas)

        # Si 'todas' está vacía no hay notas: evita dividir entre cero.
        if not todas:
            return 0

        # sum(todas) suma las notas; len(todas) las cuenta.
        # round(..., 2) redondea el resultado a 2 decimales.
        return round(sum(todas) / len(todas), 2)

    # Método que compara las materias de este estudiante con las de otro.
    def materias_en_comun(self, otro_estudiante):
        """
        Obtiene las materias que comparten dos estudiantes.

        Args:
            otro_estudiante (Estudiante): Segundo estudiante.

        Returns:
            set: Materias que ambos estudiantes comparten.
        """

        # INTERSECCIÓN:
        # Obtiene los elementos que están en ambos conjuntos.
        # El operador & entre dos sets devuelve solo lo que tienen en común.
        return self.materias & otro_estudiante.materias

    # Convierte el objeto en un diccionario para poder guardarlo en JSON.
    def a_diccionario(self):
        """
        Convierte el estudiante en un diccionario.

        Args:
            No recibe argumentos.

        Returns:
            dict: Datos del estudiante para guardar en JSON.
        """

        # Devuelve un diccionario con todos los datos del estudiante.
        return {
            "id": self.id,                # id del estudiante
            "nombre": self.nombre,        # nombre
            "apellido": self.apellido,    # apellido
            "email": self.email,          # correo
            "carnet": self.carnet,        # carnet
            "notas": self.notas,          # diccionario de notas (JSON sí lo soporta)

            # JSON no trabaja directamente con set.
            # Por eso convertimos las materias en una lista.
            # sorted() devuelve una lista ordenada alfabéticamente.
            "materias": sorted(self.materias)
        }

    # @classmethod: el método pertenece a la CLASE, no a un objeto concreto.
    # Se usa como Estudiante.desde_diccionario(datos) sin crear antes un estudiante.
    # Es el proceso inverso a a_diccionario(): diccionario -> objeto.
    @classmethod
    def desde_diccionario(cls, datos):    # 'cls' es la clase (Estudiante), como 'self' pero para la clase
        """
        Crea un estudiante a partir de un diccionario.

        Args:
            datos (dict): Datos del estudiante.

        Returns:
            Estudiante: Objeto creado desde el diccionario.
        """

        # cls(...) equivale a Estudiante(...): llama al constructor.
        return cls(
            datos["id"],          # id (si no existe la clave, lanza KeyError)
            datos["nombre"],      # nombre (obligatorio)
            datos["apellido"],    # apellido (obligatorio)
            datos["email"],       # email (obligatorio)
            datos["carnet"],      # carnet (obligatorio)
            # .get(clave, valor_por_defecto): si no hay "notas", usa {}
            notas=datos.get("notas", {}),
            # Convierte la lista guardada en JSON de vuelta a un conjunto (set)
            materias=set(datos.get("materias", []))
        )

    # Método especial: Python lo llama al hacer print(estudiante) o str(estudiante).
    def __str__(self):
        """
        Muestra una representación sencilla del estudiante.

        Args:
            No recibe argumentos.

        Returns:
            str: Texto con carnet, nombre y promedio.
        """

        # Los paréntesis permiten partir un texto largo en varias líneas;
        # Python concatena los f-strings consecutivos en uno solo.
        # Resultado ejemplo: "[EST2026001] Ana Pérez - Promedio: 18.33"
        return (
            f"[{self.carnet}] "
            f"{self.obtener_nombre_completo()} - "
            f"Promedio: {self.obtener_promedio()}"
        )


# Prueba de los métodos de models.py.
# Este bloque SOLO corre si ejecutas "python models.py" directamente;
# si otro archivo hace "from models import ...", este bloque se ignora.
if __name__ == "__main__":
    print("Prueba de models.py")

    # Crea el primer estudiante de prueba (id=1). No pasa notas ni materias.
    estudiante_a = Estudiante(
        1,
        "Ana",
        "Pérez",
        "ana@escuela.edu",
        "EST2026001"
    )

    # Crea el segundo estudiante de prueba (id=2).
    estudiante_b = Estudiante(
        2,
        "Luis",
        "Gómez",
        "luis@escuela.edu",
        "EST2026002"
    )

    print("Método agregar_nota(): agrega una nota y registra la materia.")

    # Ana: dos notas en Matemática y una en Inglés.
    estudiante_a.agregar_nota("Matemática", 18)
    estudiante_a.agregar_nota("Matemática", 20)
    estudiante_a.agregar_nota("Inglés", 17)

    # Luis: una nota en Matemática, Inglés e Historia.
    estudiante_b.agregar_nota("Matemática", 16)
    estudiante_b.agregar_nota("Inglés", 19)
    estudiante_b.agregar_nota("Historia", 18)

    print("Método __str__(): muestra los datos principales.")
    # print llama internamente a __str__()
    print(estudiante_a)
    print(estudiante_b)

    print("Método obtener_nombre_completo(): une nombre y apellido.")
    print(estudiante_a.obtener_nombre_completo())

    print("Método inscribir_materia(): agrega una materia.")
    # Inscribe a Ana en una materia sin ponerle notas todavía.
    estudiante_a.inscribir_materia("Programación")
    print(estudiante_a.materias)

    print("Método obtener_promedio(): calcula el promedio.")
    # (18 + 20 + 17) / 3 = 18.33
    print(estudiante_a.obtener_promedio())

    print("Método materias_en_comun(): busca materias compartidas.")
    # Ana y Luis comparten Matemática e Inglés.
    print(estudiante_a.materias_en_comun(estudiante_b))

    print("Método a_diccionario(): convierte el objeto en diccionario.")
    datos = estudiante_a.a_diccionario()
    print(datos)

    print("Método desde_diccionario(): crea un objeto desde un diccionario.")
    # Reconstruye un estudiante a partir del diccionario anterior.
    estudiante_c = Estudiante.desde_diccionario(datos)
    print(estudiante_c)
