#Vamos a sacar cuantas citaciones tienen por año las herramientas

import pandas as pd
import re
from datetime import datetime

def calcular_fecha_media(fecha_min,fecha_max):
    d1 = datetime.strptime(fecha_min,"%Y-%m-%d")
    d2 = datetime.strptime(fecha_max,"%Y-%m-%d")
    fecha_mid = str(d1.date() + (d2-d1)/2)
    fecha_mid = fecha_mid.split("-")
    return([fecha_mid[2],fecha_mid[1],fecha_mid[0]])
    
datos = pd.read_csv('id+referencias.csv')

#Vamos a sacar las publicaciones de cada herramientas
dicc_bio = {}
dicc_nar = {}
for fila in range(0,len(datos.index)):
    if datos.iloc[fila]["Referencias"] == "[]":#No tiene referencias el articulo
        if datos.iloc[fila]["Revista"] == "NAR":
            dicc_nar[str(datos.iloc[fila]["ID"])] = []
        else:
            dicc_bio[str(datos.iloc[fila]["ID"])] = []
        continue
    años_citaciones = {}
    row = datos.iloc[fila]["Referencias"]
    row = row[2:-2].split("), (")
    for citacion in row:
        citacion = citacion[1:-1].split(", [")
        citacion = citacion[1].split("', ")
        citacion = citacion[-1][1:-1].split(", ")
        #Tenemos en row una lista con los elementos de las publicaciones limpias
        #['Science', 'Volume 252', 'Issue 5013', '1 January 1991']
        r = re.compile(".*[0-9]{4}.*")
        r2 = re.compile("issue|volume|vol",re.IGNORECASE)
        r3 = re.compile(".*[a-z][0-9]{4}.*",re.IGNORECASE)
        r4 = re.compile(".*[0-9]{4}[a-z].*",re.IGNORECASE)
        for elemento in citacion:
            if r3.search(elemento) or r4.search(elemento):
                continue
            elif r.search(elemento) and not r2.match(elemento):
                fecha = r.search(elemento).group()
                año = int(re.search("[0-9]{4}",fecha).group())
                if str(año) not in años_citaciones:
                    años_citaciones[str(año)]= 1
                else:
                    años_citaciones[str(año)] = años_citaciones[str(año)]+1
            else:
                pass
        if datos.iloc[fila]["Revista"] == "NAR":
            dicc_nar[str(datos.iloc[fila]["ID"])] = años_citaciones
        else:
            dicc_bio[str(datos.iloc[fila]["ID"])] = años_citaciones
   
#Tenemos dos diccionarios con los puntos de cada año de cada articulo

datos_analisis = pd.read_csv("C:/Users/anama/OneDrive/Documentos/2019-2020/Practicas/analisisR/datos_bio+nar_nuevos.csv")
for i in range(0,len(datos_analisis.index)):
    row = datos_analisis.iloc[i]
    if row["Estado"] == "Disponible":#Solo queremos los analisis de los que estan muertos
        continue
    
    id_herramienta = row["ID"]
    print(id_herramienta)
    revista = row["Revista"]
    año_nacimiento = row["Anualidad"]
    fecha_min = row["FechaMin"]
    fecha_min = fecha_min.split("/")
    fecha_min_calculo = str(fecha_min[2]+"-"+fecha_min[1]+"-"+fecha_min[0])
    fecha_max = row["FechaMax"]
    if fecha_max == "?":
        fecha_max = "31/05/2020"
    fecha_max = fecha_max.split("/")
    fecha_max_calculo = str(fecha_max[2]+"-"+fecha_max[1]+"-"+fecha_max[0])
    fecha_med = calcular_fecha_media(fecha_min_calculo,fecha_max_calculo)
    #buscamos de que revista son
    if revista == "NAR":
        valores_citaciones = dicc_nar[str(id_herramienta)]
    else:
        valores_citaciones = dicc_bio[str(id_herramienta)]
    #Lo que obtenemos son diccionarios en valores_citaciones
    columna_año = []
    columna_citaciones = []
    for anualidad in range(int(año_nacimiento),int(fecha_max[2])+1):
        try:
            valores_citaciones[str(anualidad)]
            columna_año.append(anualidad)
            columna_citaciones.append(int(valores_citaciones[str(anualidad)]))
        except:#No existe este año en el diccionario
            columna_año.append(anualidad)
            columna_citaciones.append("0")
    tabla_final = pd.DataFrame(data=columna_año,columns=["anualidad"])
    tabla_final["citaciones"] = columna_citaciones
    #Vamos a anadir en que ano muerio de manera minima, media y maxima
    fechas_muerte = []
    for j in range(0,len(tabla_final.index)):
        an_elegido = int(tabla_final.iloc[j]["anualidad"])
        if an_elegido == int(fecha_min[2]):
            min_muerte = 1
        else:
            min_muerte = 0
        if an_elegido == int(fecha_med[2]):
            med_muerte = 1
        else:
            med_muerte = 0
        if an_elegido == int(fecha_max[2]):
            max_muerte = 1
        else:
            max_muerte = 0
        fechas_muerte.append([min_muerte,med_muerte,max_muerte])
    tabla_fechas = pd.DataFrame(fechas_muerte,columns=["muerte_min", "muerte_med", "muerte_max"])
    resultado = pd.concat([tabla_final,tabla_fechas],axis=1)
    resultado.to_csv(str("C:/Users/anama/OneDrive/Escritorio/ref_herr_muertas/"+str(id_herramienta)+"_"+str(revista)+".csv"),index=False)
                