#Preparamos los datos enteramente para que vayan al paquete de gte
import pandas as pd
from datetime import datetime



def diasHastaFecha(day1, month1, year1, day2, month2, year2):
    
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

datos = datos.drop(columns=["Censored"])#Esto es lo que vamos a cambiar para gte

time1 = []
time2 = []
censored = []
anualidades = []
datos = datos.drop(datos[(datos["FechaMin"]=="?")&(datos["FechaMax"] =="?")].index)#Quitamos los que no tenemos nada de datos
datos.reset_index(drop=True,inplace=True)
#Vamos a quitar los datos que tienen su fecha de muerte que la de publicacion
datos_eliminar = []
for numero in range(0,len(data_bio.index)):
	row = data_bio.iloc[numero]
	if row["Estado"] == "Disponible": #No es necesario cambiar nada
		continue
	else: #Hay que comprobar que la fechamin no sea menor que la de publicacion(tanto de las que solo tienen esa como de las que tienen los intervalos)
		fecha = row["Volumen"].split("/")
		if row["FechaMin"] == "?":
			fecha_muerte = row["FechaMax"].split("/")
		else:
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
datos.drop(datos_eliminar, inplace=True)

#Ya tenemos los datos con los que vamos a trabajar (LC,RC e IC)
for i in range(0,len(datos.index)):
	row = datos.iloc[i]
	if row["Estado"] == "Disponible":#Empezamos por el tratamiento de las herramientas disponibles
		fecha = row["Volumen"].split("/")
		total = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), 31, 5, 2020) #El ultimo analisis lo hicimos el 31 de mayo
		anualidades.append(fecha[2])
		time1.append(total)
		time2.append("NA")
		censored.append(0)
	elif row["FechaMax"] == "?":#Tratamiento de los interval censored que no sabemos su fecha maxima
		fecha = row["Volumen"].split("/")
		fecha_muerte = row["FechaMin"].split("/")
		total = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_muerte[0]),int(fecha_muerte[1]),int(fecha_muerte[2]))
		total2 = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), 31, 5, 2020) #El ultimo analisis lo hicimos el 31 de mayo
		anualidades.append(fecha[2])
		time1.append(total)
		time2.append(total2)
		censored.append(3)
	elif row["FechaMin"] == "?":#Tratamiento de los LC
		fecha = row["Volumen"].split("/")
		fecha_muerte = row["FechaMax"].split("/")
		total = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_muerte[0]),int(fecha_muerte[1]),int(fecha_muerte[2]))
		anualidades.append(fecha[2])
		time1.append("NA")
		time2.append(total)
		censored.append(2)
	else:#son los que tienen intervalos
		fecha = row["Volumen"].split("/")
		fecha_muerte_1 = row["FechaMin"].split("/")
		fecha_muerte_2 = row["FechaMax"].split("/")
		total = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_muerte_1[0]),int(fecha_muerte_1[1]),int(fecha_muerte_1[2]))
		total2 = diasHastaFecha(int(fecha[0]), int(fecha[1]), int(fecha[2]), int(fecha_muerte_2[0]),int(fecha_muerte_2[1]),int(fecha_muerte_2[2]))
		time1.append(total)
		time2.append(total2)
		censored.append(3)
		anualidades.append(fecha[2])
datos["Censored"] = censored
datos["Tiempo1"] = time1
datos["Tiempo2"] = time2
datos["Anualidad"] = anualidades


#Ya tenemos los datos con sus citaciones y fechas de muerte y censored, vamos a juntarlas
datos_combinacion = pd.concat([data_bio,data_nar])
datos_combinacion.to_csv("/home/amanhel/Documents/TFG/datos_gte_bio+nar.csv",index=False)
