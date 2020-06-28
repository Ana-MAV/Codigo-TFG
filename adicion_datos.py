#Script va a poner la informacion adicional a los archviso obtenido de obtencion_info_disponibilidad+muerte.py
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

data_bio_ftp = pd.read_csv("/home/amanhel/Documents/ArchivosBioinformatics/ftps_bio_muerte.csv")
data_bio_http = pd.read_csv("/home/amanhel/Documents/ArchivosBioinformatics/https_bio_muerte.csv")
data_nar_ftp = pd.read_csv("/home/amanhel/Documents/ArchivosNucleic/ftps_nar_muerte.csv")
data_nar_http = pd.read_csv("/home/amanhel/Documents/ArchivosNucleic/https_nar_muerte.csv")

#Vamos a poner en el mismo formato los https con los ftps, ponerles su fecha de nacimiento, numero de citaciones
#NAR
estados = []
revistas = []
for i in range(0,len(data_nar_ftp.index)):
    if int(data_nar_ftp.iloc[i]["Codigo"]) == 200:
        estados.append("Disponible")
        revistas.append("NAR")
    else:
        estados.append("No disponible")
        revistas.append("NAR")
data_nar_ftp["Estado"] = estados
data_nar_ftp["Revista"] = revistas
data_nar_ftp.drop(columns=["Codigo","Mensaje"])

estados_http = []
revistas_http = []
for j in range(0,len(data_nar_http.index)):
    if int(data_nar_http.iloc[j]["Codigo Wget"]) == 200 or int(data_nar_http.iloc[j]["Codigo UrlLib"]):
        estados_http.append("Disponible")
        revistas_http.append("NAR")
    else:
        estados_http.append("No disponible")
        revistas_http.append("NAR")
data_nar_http["Estado"] = estados_http
data_nar_http["Revista"] = revistas_http
data_nar_http.drop(columns=["Codigo Wget","Mensaje Wget","CodigoUrlLib","Mensaje UrlLib"])


#Vamos a guardar los IDs de los volumenes en un diccionario en el que las keys seran los años
volumenes = {}
año = 2004
for i in range(32, 48): #Recorremos los volumenes
	if i<40:
		data = pd.read_csv("/home/ana/Escritorio/ScriptsPasar/NAR/nuevos_volumenes/Vol"+str(i)+"Issuesuppl_2.csv")
	else:
		data = pd.read_csv("/home/ana/Escritorio/ScriptsPasar/NAR/nuevos_volumenes/Vol"+str(i)+"IssueW1.csv")
	lista_IDs = data["IDArticulo"].to_list()
	fecha = "01/07/"+str(año)
	volumenes[fecha] = lista_IDs
	año += 1

#Vamos a ponerle la informacion a las tablas que ya tenemos
tabla_final = []
for c in range(0, len(data_nar_http.index)):
	row = data_nar_http.iloc[c]
	id_url = row["ID"]
	años = list(volumenes.keys())
	for entrada in años: #Recorremos el diccionario
		if id_url in volumenes[entrada]:
			#Vamos a convertir los datos en los adecuados
			if row["Estado"] == "Disponible":
				tabla_final.append([row["ID"],row["URL"],"Disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"NAR",entrada,0])#El 0 es para señalar que esta censurado por la derecha
			else:
				tabla_final.append([row["ID"],row["URL"],"No disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"NAR", entrada,1])
			break
		else:
			continue


for d in range(0, len(data_nar_ftps.index)):
	row = data_ftps.iloc[d]
	id_url = row["ID"]
	años = list(volumenes.keys())
	for entrada in años: #Recorremos el diccionario
		if id_url in volumenes[entrada]:
			#Vamos a convertir los datos en los adecuados
			if row["Estado"] == "Disponible":
				tabla_final.append([row["ID"],row["URL"],"Disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"NAR",entrada,0])
			else:
				tabla_final.append([row["ID"],row["URL"],"No disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"NAR",entrada,1])
			break
		else:
			continue
        
#Creamos la tabla con los datos que tenemos
datos_finales_nar = pd.DataFrame(data=tabla_final,columns=["ID","URL","Estado","FechaMin","FechaMax","Revista","Volumen","Censored"])

#Vamos a poner los numeros de citaciones de cada herramienta
citaciones = []
for e in range(0,len(datos_finales_nar.index)):
	row = datos_finales_nar.iloc[e]
	id_articulo = int(row["ID"])
	año = int(row["Volumen"].split("/")[2])
	volumen_id = 32+(año-2004)
	if volumen_id<40:
		add = "suppl_2"
	else:
		add = "W1"
	data = pd.read_csv("/home/amanhel/Documents/TFG/ArchivosNucleic/Vol"+str(volumen_id)+"Issue"+add+".csv")
	for numero in range(0,len(data.index)):
		fila = data.iloc[numero]
		id_data = int(fila["IDArticulo"])
		if id_articulo == id_data:
			#Sacamos las citaciones
			if fila["Referencias"] == "[]" or fila["Referencias"] == "-":
				citaciones.append(0)
			else:
				citaciones.append(len(fila["Referencias"].split("), (")))
		else:
			continue
datos_finales_nar["NumCitaciones"] = citaciones
#Ya tenemos en datos_finales_nar el volumen y el numero de citaciones que tiene cada herramienta

#BIO
estados_bio = []
revistas_bio = []
for a in range(0,len(data_bio_ftp.index)):
    if int(data_bio_ftp.iloc[a]["Codigo"]) == 200:
        estados_bio.append("Disponible")
        revistas_bio.append("Bio")
    else:
        estados_bio.append("No disponible")
        revistas_bio.append("Bio")
data_bio_ftp["Estado"] = estados
data_bio_ftp["Revista"] = revistas
data_bio_ftp.drop(columns=["Codigo","Mensaje"])

estados_http_bio = []
revistas_http_bio = []
for b in range(0,len(data_bio_http.index)):
    if int(data_bio_http.iloc[b]["Codigo Wget"]) == 200 or int(data_bio_http.iloc[b]["Codigo UrlLib"]):
        estados_http_bio.append("Disponible")
        revistas_http_bio.append("Bio")
    else:
        estados_http_bio.append("No disponible")
        revistas_http_bio.append("Bio")
data_bio_http["Estado"] = estados_http_bio
data_bio_http["Revista"] = revistas_http_bio
data_bio_http.drop(columns=["Codigo Wget","Mensaje Wget","CodigoUrlLib","Mensaje UrlLib"])

#Vamos a guardar los IDs de los volumenes en un diccionario en el que las keys seran los años
volumenes_bioinformatics = [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 10), (15, 12), (16, 12), (17, 12), (18, 12), (19,18), (20, 18), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24), (28, 24), (29, 24), (30, 24), (31, 24), (32, 24), (33, 24), (34, 24), (35, 24)]

diccionario = {"A":["01/01/","01/06/","01/09/", "01/12/"], "B":["01/04/","01/06/","01/09/","01/12/"], "C":["01/03/", "01/06/", "01/09/", "01/11/"], "D":["01/03/","01/04/","01/08/", "01/11/"], "E":["01/02/","01/04/","01/07/","01/10/"], "F":["01/01/","01/04/","01/07/","01/10/"], "G":["01/02/","01/04/","01/06/","01/08/","01/10/","01/12/"], "H":["01/02/","01/04/","01/06/","01/07/","01/09/","01/12/"], "I":["01/02/","01/04/","01/06/","01/08/","01/10/","01/12/"], "J":["01/02/","01/03/","01/04/","01/05/", "01/06/","01/07/","01/08/","01/09/","01/10/","01/11/"], "K":["01/01/","01/02/","01/03/","01/04/","01/05/", "01/06/","01/07/","-", "01/09/","01/10/","01/11/","01/12/"], "L":["01/01/","01/02/","01/03/","01/04/","01/05/", "01/06/","01/07/","01/08/","01/09/","01/10/","01/11/","01/12/"], "M":["01/01/","22/01/","12/02/","01/03/","22/03/","12/04/","01/05/","22/05/", "12/06/","01/07/","22/07/","12/08/","01/09/","22/09/","12/10/","01/11/","22/11/","12/12/"], "N":["01/01/","15/01/","01/02/","15/02/","01/03/","15/03/","01/04/","15/04/","01/05/","15/05/", "01/06/","15/06/","01/07/","15/07/","01/08/","15/08/","01/09/","15/09/","01/10/","15/10/","01/11/","15/11/","01/12/","15/12/"]}

volumenes = {}
año = 1985
for tupla in volumenes_bioinformatics: #Recorremos los volumenes
	volumen = tupla[0]
	lista_final = []
	if volumen == 1:
		fechas = diccionario["A"]
	elif volumen == 2:
		fechas = diccionario["B"]
	elif volumen == 3:
		fechas = diccionario["C"]
	elif volumen == 4:
		fechas = diccionario["D"]
	elif volumen == 5:
		fechas = diccionario["E"]
	elif volumen == 6 or volumen == 7:
		fechas = diccionario["F"]
	elif volumen == 8 or volumen == 9:
		fechas = diccionario["G"]
	elif volumen == 10:
		fechas = diccionario["H"]
	elif volumen == 11 or volumen == 12 or volumen == 13:
		fechas = diccionario["I"]
	elif volumen == 14:
		fechas = diccionario["J"]
	elif volumen == 15:
		fechas = diccionario["K"]
	elif volumen ==16 or volumen == 17 or volumen == 18:
		fechas = diccionario["L"]
	elif volumen == 19 or volumen == 20:
		fechas = diccionario["M"]
	else:
		fechas = diccionario["N"]
	for i in range(1, tupla[1]+1):
		if volumen == 15 and i == 8:
			continue
		data = pd.read_csv("/home/ana/Escritorio/ScriptsPasar/Bio/Vol"+str(volumen)+"Issue"+str(i)+".csv")
		lista_IDs = data["IDArticulo"].to_list()
		volumenes[fechas[i-1]+str(año)] = lista_IDs
	año += 1

#Ponemos la fecha de nacimiento de las herramientas
tabla_final = []
for x in range(0, len(data_bio_http.index)):
	row = data_bio_http.iloc[x]
	id_url = row["ID"]
	años = list(volumenes.keys())
	for entrada in años: #Recorremos el diccionario
		if id_url in volumenes[entrada]:
			#Vamos a convertir los datos en los adecuados
			if row["Estado"] == "Disponible":
				tabla_final.append([row["ID"],row["URL"],"Disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"Bio",entrada,0])
			else:
				tabla_final.append([row["ID"],row["URL"],"No disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"Bio", entrada,1])
			break
		else:
			continue


for y in range(0, len(data_bio_ftp.index)):
	row = data_bio_ftp.iloc[y]
	id_url = row["ID"]
	años = list(volumenes.keys())
	for entrada in años: #Recorremos el diccionario
		if id_url in volumenes[entrada]:
			#Vamos a convertir los datos en los adecuados
			if row["Estado"] == "Disponible":
				tabla_final.append([row["ID"],row["Herramienta"],"Disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"Bio",entrada,0])
			else:
				tabla_final.append([row["ID"],row["Herramienta"],"No disponible",row["Fecha minima muerte"],row["Fecha maxima muerte"],"Bio",entrada,1])
			break
		else:
			continue

datos_finales_bio = pd.DataFrame(data=tabla_final,columns=["ID","URL","Estado","FechaMin","FechaMax","Revista","Volumen","Censored"])

#Vamos a poner las citaciones
citaciones = []
for b in range(0,len(datos_finales_bio.index)):
	row = datos_finales_bio.iloc[b]
	id_articulo = int(row["ID"])
	año = int(row["Volumen"].split("/")[2])
	diaymes = row["Volumen"][:-4]
	volumen_id = int(año-1984)
	#Ya hemos averiguado el volumen, ahora hay que averiguar el issue:
	if volumen_id == 1:
		fechas = diccionario["A"]
	elif volumen_id == 2:
		fechas = diccionario["B"]
	elif volumen_id == 3:
		fechas = diccionario["C"]
	elif volumen_id == 4:
		fechas = diccionario["D"]
	elif volumen_id == 5:
		fechas = diccionario["E"]
	elif volumen_id == 6 or volumen_id == 7:
		fechas = diccionario["F"]
	elif volumen_id == 8 or volumen_id == 9:
		fechas = diccionario["G"]
	elif volumen_id == 10:
		fechas = diccionario["H"]
	elif volumen_id == 11 or volumen_id == 12 or volumen_id == 13:
		fechas = diccionario["I"]
	elif volumen_id == 14:
		fechas = diccionario["J"]
	elif volumen_id == 15:
		fechas = diccionario["K"]
	elif volumen_id ==16 or volumen_id == 17 or volumen_id == 18:
		fechas = diccionario["L"]
	elif volumen_id == 19 or volumen_id == 20:
		fechas = diccionario["M"]
	else:
		fechas = diccionario["N"]
	for bla, dia_mes in enumerate(fechas):
		if dia_mes == diaymes:
			add = str(bla+1)
			break
		else:
			continue
	data_1 = pd.read_csv("/home/amnhel/Documents/TFG/ArchivosBioinformatics/Vol"+str(volumen_id)+"Issue"+add+".csv")
	for numero in range(0,len(data_1.index)):
		fila = data_1.iloc[numero]
		id_data = int(fila["IDArticulo"])
		if id_articulo == id_data:
			#Sacamos las citaciones
			if fila["Referencias"] == "[]" or fila["Referencias"] == "-":
				citaciones.append(0)
			else:
				citaciones.append(len(fila["Referencias"].split("), (")))
		else:
			continue


datos_finales_bio["NumCitaciones"] = citaciones

#Ya tenemos todos los datos de bio en datos_finales_bio
#Vamos a unir a los dos
datos_finales = pd.concat([datos_finales_bio,datos_finales_nar])

#Vamos a pasar a un csv los datos obtenidos para su posterior filtro y analisis
datos_finales.to_csv("/home/amanhel/Documents/TFG/datos_bio+nar_sin_filtrar.csv",index=False)