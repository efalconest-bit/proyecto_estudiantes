# TUPLA:
# Contiene los campos principales de un estudiante.
# Se utiliza una tupla porque los nombres de los campos son fijos.
CAMPOS_ESTUDIANTE = (
    "nombre",
    "apellido",
    "email",
    "carnet"
)


class Estudiante:
    """
    Representa a un estudiante y sus datos académicos.
    """

    def __init__(
        self,
        id_estudiante,
        nombre,
        apellido,
        email,
        carnet,
        notas=None,
        materias=None
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

        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        # DICCIONARIO:
        # Relaciona cada materia con sus notas.
        self.notas = notas if notas else {}

        # CONJUNTO:
        # Guarda las materias sin repetir.
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        """
        Obtiene el nombre completo del estudiante.

        Args:
            No recibe argumentos.

        Returns:
            str: Nombre y apellido del estudiante.
        """
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        """
        Inscribe al estudiante en una materia.

        Args:
            materia (str): Nombre de la materia.

        Returns:
            None: No devuelve ningún valor.
        """

        # add() agrega la materia y evita duplicados.
        self.materias.add(materia)

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
        self.inscribir_materia(materia)

        # Si la materia no existe, crea una lista.
        self.notas.setdefault(materia, []).append(nota)

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
        todas = []

        for lista_notas in self.notas.values():
            todas.extend(lista_notas)

        if not todas:
            return 0

        return round(sum(todas) / len(todas), 2)

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
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        """
        Convierte el estudiante en un diccionario.

        Args:
            No recibe argumentos.

        Returns:
            dict: Datos del estudiante para guardar en JSON.
        """

        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,

            # JSON no trabaja directamente con set.
            # Por eso convertimos las materias en una lista.
            "materias": sorted(self.materias)
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """
        Crea un estudiante a partir de un diccionario.

        Args:
            datos (dict): Datos del estudiante.

        Returns:
            Estudiante: Objeto creado desde el diccionario.
        """

        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", []))
        )

    def __str__(self):
        """
        Muestra una representación sencilla del estudiante.

        Args:
            No recibe argumentos.

        Returns:
            str: Texto con carnet, nombre y promedio.
        """

        return (
            f"[{self.carnet}] "
            f"{self.obtener_nombre_completo()} - "
            f"Promedio: {self.obtener_promedio()}"
        )


# Prueba de los métodos de models.py.
if __name__ == "__main__":
    print("Prueba de models.py")

    estudiante_a = Estudiante(
        1,
        "Ana",
        "Pérez",
        "ana@escuela.edu",
        "EST2026001"
    )

    estudiante_b = Estudiante(
        2,
        "Luis",
        "Gómez",
        "luis@escuela.edu",
        "EST2026002"
    )

    print("Método agregar_nota(): agrega una nota y registra la materia.")

    estudiante_a.agregar_nota("Matemática", 18)
    estudiante_a.agregar_nota("Matemática", 20)
    estudiante_a.agregar_nota("Inglés", 17)

    estudiante_b.agregar_nota("Matemática", 16)
    estudiante_b.agregar_nota("Inglés", 19)
    estudiante_b.agregar_nota("Historia", 18)

    print("Método __str__(): muestra los datos principales.")
    print(estudiante_a)
    print(estudiante_b)

    print("Método obtener_nombre_completo(): une nombre y apellido.")
    print(estudiante_a.obtener_nombre_completo())

    print("Método inscribir_materia(): agrega una materia.")
    estudiante_a.inscribir_materia("Programación")
    print(estudiante_a.materias)

    print("Método obtener_promedio(): calcula el promedio.")
    print(estudiante_a.obtener_promedio())

    print("Método materias_en_comun(): busca materias compartidas.")
    print(estudiante_a.materias_en_comun(estudiante_b))

    print("Método a_diccionario(): convierte el objeto en diccionario.")
    datos = estudiante_a.a_diccionario()
    print(datos)

    print("Método desde_diccionario(): crea un objeto desde un diccionario.")
    estudiante_c = Estudiante.desde_diccionario(datos)
    print(estudiante_c)