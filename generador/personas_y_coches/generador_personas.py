import random

def generar_id_persona():
    return random.randint(10000, 99999)

def cargar_txt(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def generar_nombres():
    nombre = cargar_txt('Data_Base/personas_y_coches/nombre.txt')
    return random.choice(nombre)

def generar_primer_apellido():
    primer_apellido = cargar_txt('Data_Base/personas_y_coches/apellido.txt')
    return random.choice(primer_apellido)

def generar_segundo_apellido():
    segundo_apellido = cargar_txt('Data_Base/personas_y_coches/apellido.txt')
    return random.choice(segundo_apellido)

def generar_dni():
    numeros = random.randint(10000000, 99999999)
    letra = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f"{numeros}-{letra}"

def generar_edad():
    return random.randint(18, 75)

def generar_cartera():
    return round(random.uniform(100, 10000), 2)

def generar_persona():
    id_persona = generar_id_persona()
    nombre = generar_nombres()
    primer_apellido = generar_primer_apellido()
    segundo_apellido = generar_segundo_apellido()
    dni = generar_dni()
    edad = generar_edad()
    cartera = generar_cartera()

    persona = {
        'ID_persona':id_persona,
        'Nombre':nombre,
        'Primer apellido':primer_apellido,
        'Segundo apellido':segundo_apellido,
        'DNI':dni,
        'Edad':edad,
        'Cartera':cartera
    }

    return persona




#SOLO DEVOLVERÁ UNA PERSONA PARA ESTE VIERNES
for _ in range(1):
    persona_generada = generar_persona()
    print(persona_generada)
