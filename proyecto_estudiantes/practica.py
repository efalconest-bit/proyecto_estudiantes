#Ejercicio 1: Eliminar duplicados de una lista y conservar el orden

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()      # conjunto de control: para preguntar rápido si ya apareció
unicas = []         # lista de resultado: conserva el orden
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print(unicas)   # ['Quito', 'Guayaquil', 'Cuenca']

#Ejercicio 2: Contar un diccionario

conteo = {}
for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1     # .get evita el KeyError la primera vez

print(conteo)

# El más repetido:
mas_repetida = max(conteo, key=conteo.get)
print(mas_repetida)

#Ejercicio 3 · Conjuntos en acción

inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles     = {"Luis", "Marco", "Juan"}

ambas       = inscritos_matematica & inscritos_ingles     # {'Luis','Marco'}
solo_mate   = inscritos_matematica - inscritos_ingles     # {'Ana','Sol'}
total       = len(inscritos_matematica | inscritos_ingles)  # 5

print(sorted(ambas), sorted(solo_mate), total)

# Ejercicio 4: De lista de diccionarios a índice
clientes = [
    {"id": 1, "nombre": "Ana"},
    {"id": 2, "nombre": "Luis"},
    {"id": 3, "nombre": "Sol"},
]
indice = {cliente["id"]: cliente for cliente in clientes}
print(indice[2]["nombre"])       # 'Luis'

# Diferencia de costo:
# recorrer la lista  -> revisa hasta N registros
# indice[2]          -> una sola operación, sin importar cuántos haya

#Ejercicio 5 · Tuplas como registros inmutables

ventas = [
    ("Enero", 1000),
    ("Febrero", 1500),
    ("Marzo", 1200),
]
total = sum(monto for _mes, monto in ventas)

mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])

print(f"Total: {total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")

for mes, monto in ventas:              # desempaquetado en el for
    print(f"{mes:<10} {monto}")

