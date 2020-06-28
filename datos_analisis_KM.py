#Vamos a crear los datos usados en el analisis KM

import pandas as pd
from datetime import datetime

#Funciones necesarias para que el programa principal funcione
def diasHastaFecha(day1, month1, year1, day2, month2, year2):
#Funcion que nos da los dias entre 2 fechas
    # Función para calcular si un año es bisiesto o no
    
    def esBisiesto(year):
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0
    
    # Caso de años diferentes
    
    if (year1<year2):
        
        # Días restante primer año
        
        if esBisiesto(year1) == False:
            diasMes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            diasMes = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
     
        restoMes = diasMes[month1] - day1
    
        restoYear = 0
        i = month1 + 1
    
        while i <= 12:
            restoYear = restoYear + diasMes[i]
            i = i + 1
    
        primerYear = restoMes + restoYear
    
        # Suma de días de los años que hay en medio
    
        sumYear = year1 + 1
        totalDias = 0
    
        while (sumYear<year2):
            if esBisiesto(sumYear) == False:
                totalDias = totalDias + 365
                sumYear = sumYear + 1
            else:
                totalDias = totalDias + 366
                sumYear = sumYear + 1
    
        # Dias año actual
    
        if esBisiesto(year2) == False:
            diasMes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            diasMes = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
        llevaYear = 0
        lastYear = 0
        i = 1
    
        while i < month2:
            llevaYear = llevaYear + diasMes[i]
            i = i + 1
    
        lastYear = day2 + llevaYear
    
        return totalDias + primerYear + lastYear
    
    # Si estamos en el mismo año
    
    else:
        
        if esBisiesto(year1) == False:
            diasMes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            diasMes = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
        llevaYear = 0
        total = 0
        i = month1
        
        if i < month2:
            while i < month2:
                llevaYear = llevaYear + diasMes[i]
                i = i + 1
            total = day2 + llevaYear - 1
            return total 
        else:
            total = day2 - day1
            return total



#Programa principal
datos = pd.read_csv("/home/amanhel/Documents/TFG/datos_bio+nar_sin_filtrar.csv")

dias = []
df = datos.drop(datos[datos.FechaMin=="?"].index)#Quitamos los left censored y los que no tenemos nada
df.reset_index(drop=True,inplace=True)
#Vamos a comprobar que ninguna de las fechas que quedan son menores de la fecha de publicacion
datos_eliminar = []
for numero in range(0,len(df.index)):
	row = df.iloc[numero]
	if row["Estado"] == "Disponible": #No es necesario cambiar nada
		continue
	else: #Hay que comprobar que la fechamin no sea menor que la de publicacion(tanto de las que solo tienen esa como de las que tienen los intervalos)
		fecha = row["Volumen"].split("/")
		fecha_muerte = row["FechaMin"].split("/")
		if int(fecha[2])<int(fecha_muerte[2]):
			continue
		elif int(fecha[2])==int(fecha_muerte[2]):#Miramos el mes
			if int(fecha[1])<int(fecha_muerte[1]):
				continue
			elif int(fecha[1])==int(fecha_muerte[1]): #Miramos el dia
				if int(fecha[0])<int(fecha_muerte[0]):
					continue
				else:#El dia es el mismo o menor
					datos_eliminar.append(numero)
			else:
				datos_eliminar.append(numero)
		else:#El año de fecha muerte es menor que el de publicacion
			datos_eliminar.append(numero)
#Eliminamos lso que tienen una fecha menor
df.drop(datos_eliminar, inplace=True)#Se eliminan 65
columna_min=[]
columna_max=[]
columna_media=[]
anualidades = []
for i in range(0,len(df.index)):
	row = df.iloc[i]
	if row["Estado"] == "Disponible":
		fecha = row["Volumen"].split("/")
		total = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), 31, 5, 2020) #El primer analisis lo hicimos el 31 de mayo
		anualidades.append(fecha[2])
		columna_min.append(total)
		columna_max.append(total)
		columna_media.append(total)
	elif row["FechaMax"] == "?":
		fecha = row["Volumen"].split("/")
		print(fecha)
		fecha_muerte = row["FechaMin"].split("/")
		print(fecha_muerte)
		a = datetime(int(fecha_muerte[2]), int(fecha_muerte[1]), int(fecha_muerte[0]))
		b = datetime(2020, 5 ,31)
		d = str(a + (b - a)/2)
		fecha_mitad = str(d).split(" ")[0]
		fecha_mitad = fecha_mitad.split("-") #Año,mes,dia se queda, ya que da la americana
		total_min = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_muerte[0]),int(fecha_muerte[1]),int(fecha_muerte[2]))
		total_max = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), 31, 5, 2020)
		total_media = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_mitad[2]), int(fecha_mitad[1]), int(fecha_mitad[0]))
		anualidades.append(fecha[2])
		columna_min.append(total_min)
		columna_max.append(total_max)
		columna_media.append(total_media)
	else:
		fecha = row["Volumen"].split("/")
		fecha_min = row["FechaMin"].split("/")
		fecha_max = row["FechaMax"].split("/")
		a = datetime(int(fecha_min[2]), int(fecha_min[1]), int(fecha_min[0]))
		b = datetime(int(fecha_max[2]), int(fecha_max[1]), int(fecha_max[0]))
		d = str(a + (b - a)/2)
		fecha_mitad = str(d).split(" ")[0]
		fecha_mitad = fecha_mitad.split("-")
		total_min = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_min[0]),int(fecha_min[1]),int(fecha_min[2]))
		total_max = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_max[0]),int(fecha_max[1]),int(fecha_max[2]))
		total_media = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_mitad[2]), int(fecha_mitad[1]), int(fecha_mitad[0]))
		anualidades.append(fecha[2])
		columna_min.append(total_min)
		columna_max.append(total_max)
		columna_media.append(total_media)

df["dias_min"] = columna_min
df["dias_media"] = columna_media
df["dias_max"] = columna_max
df["Anualidad"] = anualidades

df.to_csv("datos_bio+nar_filtrados.csv", index=False)