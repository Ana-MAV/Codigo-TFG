#Script para obtener el numero de articulos que tenemos de NAR y bio, para los resultados
#Vamos a ver cuantos articulos se accedio y cuantos se sacaron
import pandas as pd

volumenes_bio = [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 10), (15, 12), (16, 12), (17, 12), (18, 12), (19,18), (20, 18), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24), (28, 24), (29, 24), (30, 24), (31, 24), (32, 24), (33, 24), (34, 24), (35, 24)]
total_articulos = 0
total_articulos_con_herramientas = 0
articulos_bio = 0
articulos_bio_herramienta = 0
articulos_nar = 0
articulos_nar_herramienta = 0

for tupla in volumenes_bio:
	volumen = tupla[0]
	#print(volumen)
	for i in range(1,tupla[1]+1):
		#print("\t"+str(i))
		#input()
		if volumen == 15 and i == 8:
			continue
		datos = pd.read_csv("/home/ana/Escritorio/ScriptsPasar/Bio/nuevos_volumenes/Vol"+str(volumen)+"Issue"+str(i)+".csv")
		total_articulos += len(datos.index)
		articulos_bio += len(datos.index)
		for herr in range(0,len(datos.index)):
			row = datos.iloc[herr]
			if str(row["Herramienta"]) != "-" and str(row["Herramienta"]) != "nan":
				#print("\t\t"+str(row["Herramienta"]))
				articulos_bio_herramienta += 1
				total_articulos_con_herramientas += 1
			else:
				pass


				
for vol in range(32,48):
	#print(vol)
	#input()
	if vol<40:
		issue = "suppl_2"
	else:
		issue = "W1"
	datos = pd.read_csv("/home/ana/Escritorio/ScriptsPasar/NAR/nuevos_volumenes/Vol"+str(vol)+"Issue"+issue+".csv")
	total_articulos += len(datos.index)
	articulos_nar += len(datos.index)
	for herram in range(0,len(datos.index)):
			row = datos.iloc[herram]
			if str(row["Herramienta"]) != "-" and str(row["Herramienta"]) != "nan":
				#print("\t\t"+row["Herramienta"])
				articulos_nar_herramienta += 1
				total_articulos_con_herramientas += 1
			else:
				pass

print("total de los articulos "+str(total_articulos))
print("articulos con herramientas "+str(total_articulos_con_herramientas))
print("articulos bio "+str(articulos_bio))
print("articulos nar "+str(articulos_nar))
print("articulos bio con herramienta "+str(articulos_bio_herramienta))
print("articulos nar con herramienta "+str(articulos_nar_herramienta))

