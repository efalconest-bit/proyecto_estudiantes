# Ejercicio 1: Eliminar duplicados de una lista y conservar el orden

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()
unicas = []
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print(unicas)


# Ejercicio 2: Contar con un diccionario

conteo = {}
for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1

print(conteo)

mas_repetida = max(conteo, key=conteo.get)
print(mas_repetida)


# Ejercicio 3: Conjuntos en acción

inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Juan"}

ambas = inscritos_matematica & inscritos_ingles
solo_mate = inscritos_matematica - inscritos_ingles
total = len(inscritos_matematica | inscritos_ingles)

print(sorted(ambas), sorted(solo_mate), total)


# Ejercicio 4: De lista de diccionarios a índice

clientes = [
    {"id": 1, "nombre": "Ana"},
    {"id": 2, "nombre": "Luis"},
    {"id": 3, "nombre": "Sol"},
]
indice = {cliente["id"]: cliente for cliente in clientes}
print(indice[2]["nombre"])


# Ejercicio 5: Tuplas como registros inmutables

ventas = [
    ("Enero", 1000),
    ("Febrero", 1500),
    ("Marzo", 1200),
]
total = sum(monto for _mes, monto in ventas)

mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])

print(f"Total: {total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")

for mes, monto in ventas:
    print(f"{mes:<10} {monto}")
