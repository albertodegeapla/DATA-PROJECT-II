import random

def generar_id_coche():
    return random.randint(10000, 99999)

def cargar_txt(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def generar_marca():
    marca = cargar_txt('/Users/albertodegeapla/Desktop/DATA-PROJECT-II/Data_Base/personas y coches/marcas_coche.txt')
    return random.choice(marca)

def generar_matricula():
    numeros = random.randint(0000, 9999)
    letra = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f"{numeros}-{letra}"

def generar_edad_coche():
    random.randint(0, 25)

def generar_plazas():
    random.randint(1, 4)

def generar_kilometraje():
    random.randint(1000, 200000)

def generar_precio_compra():
    random.randint(10000, 80000)

def generar_precio_km(kilometraje, precio_compra):
    descuento_por_kilometraje = 0.05  # Descuento del 5% por cada 10000km
    descuento = (kilometraje // 10000) * descuento_por_kilometraje
    precio_final = precio_compra - descuento

    return max(precio_final, 0)

kilometraje = generar_kilometraje
precio_compra = generar_precio_compra


def generar_coche():
    id_coche = generar_id_coche
    marca = generar_marca
    matricula = generar_matricula
    edad_coche = generar_edad_coche
    plazas = generar_plazas
    kilometraje = generar_kilometraje
    precio_compra = generar_precio_compra
    precio_por_km = generar_precio_km

    coche = {
        'ID_coche':id_coche,
        'Marca':marca,
        'Matrícula':matricula,
        'Edad coche':edad_coche,
        'Kilometraje':kilometraje,
        'Precio de compra':precio_compra,
        'Precio por kilometro':precio_por_km
    }

    return coche

#SOLO DEVOLVERÁ UN COCHE PARA ESTE VIERNES
for _ in range(1):
    coche_generado = generar_coche()
    print(coche_generado)
