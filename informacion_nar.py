#Scripts para sacar la informacion de los articulos de NAR

import time
import random
from bs4 import BeautifulSoup as BS
import json
import re
import pandas as pd
import os


#Funciones necesarias para el funcionamiento del programa principal

def paginacion(url, numero_paginas, vol):
#Funcion que coge el volumen y el issue que tiene mas de una pagina y crea los documentos de las demas paginas
	for i in range(2, numero_paginas+1):
		url = url+"?page="+str(i)
		if vol<40:
			archivo = "Vol"+str(vol)+"Issuesuppl_2_"+str(i)
		else:
			archivo = "Vol"+str(vol)+"IssueW1_"+str(i)
		try:
			open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html", "r")
			if os.stat("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html").st_size == 0:
				vacios.write("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html\n")
		except:
			os.system(wget_com+url+'" -O '+"/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html")
	return


def articulos(file_issue):
#Funcion que devuelve todos las direcciones de todos los articulos de una publicacion
	articulos_totales=[]
	soup = BS(file_issue, 'lxml')
	a = soup.find_all("h4", {"data-level":"1"})
	for section in a:
		seccion_text = section.text.upper()
		if "EDITORIAL" in seccion_text or seccion_text == "FRONT-MATTER/BACK-MATTER" or seccion_text == "CORRIGENDUM": #Editorial a veces tiene mas cosas en el texto que sólo editorial
			continue
		else:
			bloque = section.parent
			for articulo in bloque.find_all("div", class_ = "al-article-items"):#Encuentra los diferentes articulos del primer sub-apartado
				link = articulo.a["href"]
				titulo = articulo.find("a").text.upper()
				if "/i/" in link or "/ii/" in link or "/iii/" in link or "BIOINFORMATICS LINKS DIRECTORY" in titulo: #Serian los que se dan al principio y el del update de directories de Bioinformatics
					continue
				articulos_totales.append("https://academic.oup.com"+link)
	return (articulos_totales)


def abstract_url(data):
#Funcion que recibe parte del contenido del HTML de un articulo y devuelve el abstract y la URL de la herramienat asociada, en el caso de que esten
	for link in data:
		if link.get("class")[0] == "abstract":#Para coger la parte que corresponde al texto completo del abstract
			parte_abstract = link
			break
	#Sacamos el texto del abstract
	abstract = parte_abstract.text
	abstract = re.sub("\t|\n|\r","",abstract)

	#Sacamos la URL de la herramienta
	url = str()
	for campo in parte_abstract.find_all("a"):
		try:
			url = campo["href"]
			if "@" in url and not "://" in url:#Caso de que sea un email y no una URL
				url = "-"
				continue
			elif "python.org" in url or "r-project.org" in url:
				url = "-"
				continue

			elif url == "http://" or url == "https://":
				url = campo.text
				break
			else: #Un URL valido
				break
		except: #No hay URL asociada
			url = "-"
			continue
	url = url.replace(" ","").replace("\n","").replace("\t","").replace("\r","").replace("(","").replace(")","")
	url = re.sub("\t|\n|\r|(|)","",url)
	return (abstract, url)


def info_json(data):
#Funcion que recibe parte del contenido del HTML de un articulo y devuelve el titulo, doi, los autores y el numero de id de bioinformatics
	dic = json.loads(data.string)
	#Obtenemos la información de este artículo
	titulo = dic["name"]
	doi = dic["url"]
	numero = dic["sameAs"].split("/")
	numero_id = numero[-1]
	dic_autores = dic["author"]
	autores = []

	for autor in dic_autores:#Los autores estan en otro diccionario dentro del grande
		autores.append(autor["name"])

	return (numero_id, titulo, autores, doi)


def datos(url):
#Funcion que cogiendo la URL de un artículo, devuelve los siguientes datos: 1.URL, 2.titulo, 3.autores, 4.DOI, 5.abstract, 6.URL de la herramienta, 7.Papers que lo referencian
	codigo = url.split("/")
	codigo = "_".join(codigo[-4:])
	try: #Para saber si ese HTML esta o no en la carpeta de trabajo
		#print("he entrado en el try")
		file_in = open("/home/ana/urbion/TFG/ArchivosNucleic/"+codigo+".html", "r")
	except:
		os.system(wget_com+url+'" -O '+"/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html")
     file_in = open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+codigo+".html", "r")
     
	if os.stat("/home/ana/urbion/TFG/ArchivosNucleic/"+codigo+".html").st_size == 0:
		file_in.close()
		vacios.write(url+"\n")
		return ([url,"El HTML estaba vacio","-","-","-","-","-","-"])	
    
	soup2 = BS(file_in, 'lxml')
	data = soup2.find(type="application/ld+json")
	try:
		soup2.find("h2", class_="abstract-title")
		data2 = soup2.find_all("section")
		(abstract_txt, url_herramienta) = abstract_url(data2)
	except:
		(abstract_txt, url_herramienta) = ("-","-")
	(numero_id, titulo, autores, doi) = info_json(data)
	file_in.close()
	
	#Ahora vamos a sacar las referencias de cada artículo
	references = citation(numero_id)
	r = re.compile("http://http.*")
	if r.match(url_herramienta):
		url_herramienta = url_herramienta.replace("http://http:/","http://")
	todas.write(url_herramienta+"\n")
	return([url, numero_id, titulo, autores, doi, abstract_txt, url_herramienta, references])


def citation(codigo):
#Funcion que coge el codigo de identificacion del articulo de NAR y devuelve todos los articulos que referencian a este
	nombre_archivo = codigo+"_ref.html"
	try:
		file_cross = open("/home/ana/urbion/TFG/ArchivosNucleic/"+nombre_archivo, "r")
	except:
     url = "https://academic.oup.com/nar/crossref-citedby/"+str(codigo)
		os.system(wget_com+url+'" -O '+"/home/amanhel/Documents/TFG/ArchivosNucleic/"+nombre_archivo+".html")
     file_cross = open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+nombre_archivo, "r")
	try:
		if os.stat("/home/amanhel/Documents/TFG/ArchivosNucleic/"+nombre_archivo).st_size == 0 or os.stat("/home/amanhel/Documents/TFG/ArchivosNucleic/"+nombre_archivo).st_size == 0:#Esta vacio el HTML
			file_cross.close()
			vacios.write(url+"\n")
			return ("El HTML estaba vacio")
	except:
		pass
	
	soup3 = BS(file_cross, 'lxml')
	#Sacamos los datos de esta pagina
	citaciones = extraccion(soup3)
	file_cross.close()
	#Despues de sacar el HTML y las referencias de la primera pagina (en ocasiones unica) vamos a ver si hay mas paginas de referencias
    
	try:
		paginacion = soup3.find("div", class_ = "pageNumbers al-pageNumbers")
		numero_paginas = paginacion.find_all("a")
		numero = int(numero_paginas[-1]["data-clicked-page"]) #El ultimo que sale en esa pagina
		numero_inicial = 2
		control = True
		while control == True:
			for i in range(numero_inicial, numero+1):
				nombre_archivo = codigo+"_"+str(i)+"_ref.html"
				try:
					file_cross = open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+nombre_archivo, "r")
				except:
					faltantes.write(nombre_archivo+"\n")
					return([])

				soup = BS(file_cross, 'lxml')
				lista = extraccion(soup)
				for referencia in lista:
					citaciones.append(referencia)
				#Hay veces que hay mas paginas de las que paracen al principio 
				paginacion = soup.find("div", class_ = "pageNumbers al-pageNumbers")
				numero_paginas = paginacion.find_all("a")
				numero_nuevo = int(numero_paginas[-1]["data-clicked-page"])
				#print(str(numero)+"\t"+str(numero_nuevo)+"\t"+str(i))
				if numero == numero_nuevo:
					if i == numero:#Hemos llegado al final de las paginas de citaciones
						file_cross.close()
						control = False
						break
					else:
						file_cross.close()
						continue
				elif numero != numero_nuevo:
					if numero_nuevo < numero and i == numero:
						#print("he llegado al final de las citaciones")
						file_cross.close()
						control = False
					else:
						numero_inicial = i+1 #Comenzamos desde la siguiente pagina de las referencias
						numero = numero_nuevo
						file_cross.close()
						break
	except: #Significa que solo hay una pagina de referencias
		pass
	return citaciones



#Programa principal
wget_com = 'wget --user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" --referer="https://www.google.com" --timeout=300 --tries=4 "'
vol_1 = 32 #El primer volumen con una edicion de softwares
vol_final = 47 #El utlimo de los volumenes que vamos a contar, el del 2019
#Excepts y vacios son variables que serviran para controlar si algun HTML no esta o si esta vacio
excepts = open("archivos_except_nar.txt", "w")
vacios = open("archivos_vacios_nar.txt", "w")

for volumen in range(vol_1, vol_final+1): #Recorremos todos los volumenes
	if volumen < 40: #Se llaman diferente dependiendo del año, pero son equivalentes suppl_2 y W1
		url = "https://academic.oup.com/nar/issue/"+str(volumen)+"/suppl_2"
		archivo = "Vol"+str(volumen)+"Issuesuppl_2"
	else:
		url = "https://academic.oup.com/nar/issue/"+str(volumen)+"/W1"
		archivo = "Vol"+str(volumen)+"IssueW1"
	archivo_original = archivo #Esta variable es para poner el issue bien cuando se escriba el csv

	try:#Sirve para no descargar el mismo HTML 2 veces
		file_vol = open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html","r")
	except:
		os.system(wget_com+url+'" -O '+"/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html")
		file_vol = open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html", "r")
		time.sleep(random.randrange(25,85))
		continue

	articulos_issue = articulos(file_vol)
	file_vol.close() #Necesito hacer esto porque si no el soup no contiene nada
	file_vol = open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html", "r")
	if os.stat("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html").st_size == 0:
		vacios.write("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo+".html\n")
        
	soup = BS(file_vol, 'lxml')
	if soup.find("div", class_ = "issue-pagination-text"):
		texto = soup.find("div", class_="issue-pagination-text")
		texto = texto.text.replace(" ","").replace("\n","")
		numero_paginas = int(texto[-1])
		paginacion(url, numero_paginas, volumen)
		for i in range(2,numero_paginas+1):
			archivo = archivo+"_"+str(i)+".html"
			file_vol = open("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo, "r")
			articulos_pag = articulos(file_vol)
			for articulo in articulos_pag:
				articulos_issue.append(articulo)	
	else: #Puramente estructural este else
		pass
    
	#Ya tenemos los articulos en la lista articulos_issue, ahora tenemos que sacar los datos de ese issue
	datos_issue = []
	for articulo in articulos_issue:
		datos_issue.append(datos(articulo))
	#Ya tengo los datos de los articulos, lo pasamos ahora a un csv para ver si lo da bien
	tabla = pd.DataFrame(datos_issue, columns=["URLArticulo", "IDArticulo", "Titulo", "Autores", "DOI", "Abstract", "Herramienta", "Referencias"])
	tabla.to_csv("/home/amanhel/Documents/TFG/ArchivosNucleic/"+archivo_original+".csv", index = False)
	file_vol.close()
