#Script de prueba para relativizar las citaciones de bio+nar_nuevos.csv
import pandas as pd
import re
from datetime import datetime


def calcular_fecha_media(fecha_min,fecha_max):
    d1 = datetime.strptime(fecha_min,"%Y-%m-%d")
    d2 = datetime.strptime(fecha_max,"%Y-%m-%d")
    fecha_mid = str(d1.date() + (d2-d1)/2)
    fecha_mid = fecha_mid.split("-")
    return([fecha_mid[2],fecha_mid[1],fecha_mid[0]])


datos = pd.read_csv("datos_bio+nar_nuevos.csv")


#Vamos a crear 2 diccionarios, uno de bio y otro de nar con la ID y las citaciones
volumenes_bio = [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 10), (15, 12), (16, 12), (17, 12), (18, 12), (19,18), (20, 18), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24), (28, 24), (29, 24), (30, 24), (31, 24), (32, 24), (33, 24), (34, 24), (35, 24)]
issue_min_nar = 32
issue_max_nar = 47

dicc_bio = {}
dicc_nar = {}
for tupla in volumenes_bio:
	volumen = tupla[0]
	for i in range(1,tupla[1]+1):
		if volumen == 15 and i == 8:
			continue
		datos_volumen = pd.read_csv("/home/amanhel/documents/TFG/ArchivosBioinformatics/Vol"+str(volumen)+"Issue"+str(i)+".csv")
		for j in range(0,len(datos_volumen)):
			id_art = datos_volumen.iloc[j]["IDArticulo"]
			referencias = datos_volumen.iloc[j]["Referencias"]
			try:
				dicc_bio[id_art]
				print(str(volumen)+" bio "+str(i)+" "+id_art)
			except:
				dicc_bio[id_art] = referencias

for a in range(issue_min_nar,issue_max_nar+1):
	if a <40:
		issue="suppl_2"
	else:
		issue="W1"
	datos_volumen = pd.read_csv("/home/amanhel/documents/TFG/ArchivosNucleic/Vol"+str(a)+"Issue"+issue+".csv")
	for b in range(0,len(datos_volumen)):
		id_art = datos_volumen.iloc[b]["IDArticulo"]
		referencias = datos_volumen.iloc[j]["Referencias"]
		try:
			dicc_nar[id_art]
			print(str(a)+" nar "+id_art)
		except:
			dicc_nar[id_art] = referencias
#Ya tenemos los diccionarios
#Vamos a buscar y añadir las citaciones a cada fila segun su id y la revista
citaciones_min_col = []
citaciones_media_col = []
citaciones_max_col = []
citaciones_min_rel = []
citaciones_media_rel = []
citaciones_max_rel = []
for fila in range(0,len(datos.index)):
	row = datos.iloc[fila]
	id_art = int(row["ID"])
	dias_min = int(row["dias_min"])
	dias_med = int(row["dias_media"])
	dias_max = int(row["dias_max"])
	if row["Estado"] == "Disponible":
		citaciones_min_col.append(int(row["NumCitaciones"]))
		citaciones_media_col.append(int(row["NumCitaciones"]))
		citaciones_max_col.append(int(row["NumCitaciones"]))
		citaciones_min_rel.append(int(row["NumCitaciones"])/dias_min)
		citaciones_media_rel.append(int(row["NumCitaciones"])/dias_med)
		citaciones_max_rel.append(int(row["NumCitaciones"])/dias_max)
		continue
	else:
		#Establecemos hasta el año que vivieron
		anu_min = int(row["FechaMin"].split("/")[2])
		if row["FechaMax"] == "?":
			anu_max = 2020
			fecha_max = ["31","05","2020"]
		else:
			anu_max = int(row["FechaMax"].split("/")[2])
			fecha_max = row["FechaMax"].split("/")
		fecha = row["FechaMin"].split("/")
		fecha_min = fecha[2]+"-"+fecha[1]+"-"+fecha[0]
		fecha_max = fecha_max[2]+"-"+fecha_max[1]+"-"+fecha_max[0]
		#print(id_art)
		#print(fecha_min)
		#print(fecha_max)
		anu_med = int(calcular_fecha_media(fecha_min,fecha_max)[2])
	if row["Revista"] == "Bio":
		referencias = dicc_bio[id_art]
		if referencias == "[]":
			referencias = []
		else:
			referencias = referencias[2:-2].split("), (")
	else:
		referencias = dicc_nar[id_art]
		if referencias == "[]":
			referencias = []
		else:
			referencias = referencias[2:-2].split("), (")
	citaciones_por_anualidad = {}
	for citacion in referencias:
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
		        anualidad = int(re.search("[0-9]{4}",fecha).group())
		        if str(anualidad) not in citaciones_por_anualidad:
		            citaciones_por_anualidad[str(anualidad)] = 1
		        else:
		            citaciones_por_anualidad[str(anualidad)] = citaciones_por_anualidad[str(anualidad)]+1
		    else:
		        pass
	#Ya tenemos las citaciones por año de la herramienta
	#Ahora vamos  sacar los años hasta los que vivio en cada set y ver las referencias hasta ese momento
	cit_min = 0
	cit_med = 0
	cit_max = 0
	for anu in list(citaciones_por_anualidad.keys()):
		if int(anu) <= anu_min:
			cit_min += citaciones_por_anualidad[anu]
			cit_med += citaciones_por_anualidad[anu]
			cit_max += citaciones_por_anualidad[anu]
		if int(anu) <= anu_med and int(anu) > anu_min:
			cit_med += citaciones_por_anualidad[anu]
			cit_max += citaciones_por_anualidad[anu]
		if int(anu) > anu_med and int(anu) <= anu_max:
			cit_max += citaciones_por_anualidad[anu]
	#Ahora vamos a añadirlos a los datos
	citaciones_min_col.append(int(cit_min))
	citaciones_media_col.append(int(cit_med))
	citaciones_max_col.append(int(cit_max))
	#Vamos a relativizar
	citaciones_min_rel.append(int(cit_min)/dias_min)
	citaciones_media_rel.append(int(cit_med)/dias_med)
	citaciones_max_rel.append(int(cit_max)/dias_max)
datos["CitMin"] = citaciones_min_col
datos["CitMed"] = citaciones_media_col
datos["CitMax"] = citaciones_max_col
datos["CitMinRel"] = citaciones_min_rel
datos["CitMedRel"] = citaciones_media_rel
datos["CitMaxRel"] = citaciones_max_rel
datos.to_csv("datos_citaciones_antes_de_muerte.csv",index=False)
	
