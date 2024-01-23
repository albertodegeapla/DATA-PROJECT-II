import pandas as pd
import random
from datetime import date, datetime
import numpy as np

ROOT_CSV = 'db/csv/'
# -------------- lectura de las data bases --------------
df_woman_names = pd.read_csv('csv/woman_name.csv', 
                             dtype = {
                                 "nombre": str,
                                 "frec":int
                             })
df_woman_frec_names = df_woman_names["frec"]
df_woman_names = df_woman_names["nombre"]

df_man_names = pd.read_csv('csv/man_name.csv', 
                             dtype = {
                                 "nombre": str,
                                 "frec":int
                             })
df_man_frec_names = df_man_names["frec"]
df_man_names = df_man_names["nombre"]

df_last_names = pd.read_csv('csv/last_name.csv', 
                             dtype = {
                                 "apellido": str,
                                 "frec_pri": int,
                                 "frec_seg": int
                             })
df_frec_1_last_names = df_last_names["frec_pri"]
df_frec_2_last_names = df_last_names["frec_seg"]
df_last_names = df_last_names["apellido"]

# introducir el numero de usuarios que queremos
def user_generator(param:int):
    users = [] # lista de usuarios
    dni_check = []

    for person in range(param):
        if param >= 89999999: # numero maximo (n DNIs) 
            break

        user = [] # lista de usuario

        # Generar dni y comprobar si esta disponible, si no, se genera otro sucesivamente
        dni = str(random.randint(10000000,99999999))
        dni = dni + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        while(dni in dni_check):
            dni = str(random.randint(10000000,99999999))
            dni = dni + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        dni_check.append(dni)

        # seleccion hombre mujer y su nombre segun su frecuencia (leer readme)
        sex_probability = [0.57, 0.43]
        sex_choice = int(np.random.choice([1, 2], p=sex_probability))
        if(sex_choice == 1):
            name = random.choices(df_man_names, weights=df_man_frec_names, k=1)[0]
            sex = "HOMBRE"
        else:
            name = random.choices(df_woman_names, weights=df_woman_frec_names, k=1)[0]
            sex = "MUJER"

        # seleccion apellidos segun su frecuencia
        last_name_1 = random.choices(df_last_names, weights=df_frec_1_last_names, k=1)[0]
        last_name_2 = random.choices(df_last_names, weights=df_frec_2_last_names, k=1)[0]

        # seleccion rango de edad segun frecuencia (consultar frecuencias en el README)
        age_range_probability = [
            (18, 24, 0.27),
            (25, 29, 0.26),
            (30, 39, 0.26),
            (40, 54, 0.16),
            (55, 80, 0.05)
        ]
        age_range = random.choices(age_range_probability, weights=[probabilidad for _, _, probabilidad in age_range_probability])[0]
        age = random.randint(age_range[0], age_range[1])

        # seleccion de si tiene coche y puede ser conductor o no
        car = random.choices([True, False], weights=[0.35, 0.65])[0]

        # seleccion del estado de animo (si es muy majo tiene mas disponibilidad para cambiar la ruta que si no lo es)
        mood = random.choices(["Muy majo", "Majo", "Normal", "Borde", "Muy Borde"], weights=[0.1, 0.25, 0.3, 0.25, 0.1], k=1)[0]

        # todos lo usuarios comienzan con 10€ de prueba
        wallet = 10.0

        # beneficio en blablacar
        profit = 0.0

        user.append(dni) 
        user.append(name)
        user.append(last_name_1)
        user.append(last_name_2)
        user.append(sex)
        user.append(age)
        user.append(car)
        user.append(mood)
        user.append(wallet)
        user.append(profit)
        users.append(user)
        
    
    return users

'''for element in user_generator(10):
    print(element)'''
