#Scripts para sacar la informacion de los articulos de Bioinformatics

import time
import random
from bs4 import BeautifulSoup as BS
import json
import re
import pandas as pd
import os

#Funciones necesarias para el funcionamiento del programa principal
def articulos(file_issue):
#Funcion que coge un HTML de un Issue y da como output una lista con los articulos que se dan en la seccion de Application Notes
	soup = BS(file_issue, 'lxml')
	a = soup.find_all("h4", {"data-level":"1"})

	articulos = []
	for seccion in a:#Las secciones de los papers de la pagina de bioinformatics (Articles, Erratum, Application notes, etc)
		seccion_text = seccion.text.upper()
		if seccion.text == "APPLICATIONS NOTE" or seccion.text == "APPLICATIONS NOTES" or seccion.text == "APPLICATION NOTES" or seccion.text == "APPLICATION NOTE":
			bloque =seccion.parent #Este es bloque con el primer sub-bloque de las application notes
            
			for articulo in bloque.find_all("div", class_ = "al-article-items"):#Encuentra los diferentes articulos del primer sub-apartado
				referencia = articulo.find("div", class_="ww-citation-primary")
				if "Pages i" in referencia.text or "Page i" in referencia.text: #Caso de que la estructura no sea la determinada (por ejemplo Vol29Issue13)
					continue
				link = articulo.a["href"]
				articulos.append("https://academic.oup.com"+link) #Anade el primer articulo
			while True: #Loop control para que al acabar la seccion de Application Notes deje de buscar en el HTML
				try: #Este try esta porque puede ocurrir que Applications Notes sea el ultimo apartado
					bloque = bloque.next_sibling.next_sibling
					a = str(bloque.find("h4", {"data-level":"1"}))#Cada bloque tendra un data-level 2 si es un articulo y si un data-level 1 en el caso de que sea otro apartado
					if a == "None": #Significa que no hay un data-level=1
						for articulo2 in bloque.find_all("div", class_ = "al-article-items"): #Cogemos todos los articulos dentro de esa sub-seccion de applic. notes
							link = articulo2.a["href"]
							if articulo2.a.text.upper() == "ERRATUM": #Hay veces que esta un articlo llamado erratum en estas secciones
								continue
							else:
								articulos.append("https://academic.oup.com"+link)
					else:
						break

				except:
					break

		else: #Es otro tipo de papers, pero los revisamos todos porque puede haber mas de una seccion de Application Notes
			pass

	return(articulos) #Una lista de todos los articulso de apllication notes del issue


def abstract_url(data):
#Funcion que recibe parte del contenido del HTML de un articulo y devuelve el abstract y la URL de la herramienat asociada
	#Sacamos el texto del abstract
	abstract_txt = data.find_all("p")
	abstract = str()
	url = str()
	if len(abstract_txt) == 1:
		texto = abstract_txt[0].text
		abstract = re.sub("\t|\n|\r","",texto)
	else:
		for parte in abstract_txt:
			texto = parte.text

			if "Availability:" in texto or "Contact:" in texto or "SUPPLEMENTARY INFORMATION" in texto.upper() or "Availiability:" in texto or "Availabililty:" in texto:
				if "Availability:" in texto or "Availiability:" in texto or "Availabililty:" in texto:
					for campo in parte.find_all("a"): #Asi cogemos el url del availability
						try:
							url = campo["href"]
							if "@" in url and "://" not in url: #Caso de que sea un email y no una URL
								url = str()
								continue
							elif "#supplementary-data" in url:
								url = str()
								continue
							elif url == "http://" or url == "https://":
								url = campo.text
								break
							else:
								break
						except:
							continue
			else:
				abstract = abstract+texto+" "
				abstract = re.sub("\t|\n|\r","",abstract)
                
	#Sacamos la URL de la herramienta en el caso de que no hubiera una seccion de Availability o de que en ella no hubiera enlaces. En este caso se cogera el primer URL del Abstract
	if not url:#No se establecio un aURL anteriormente
		for campo in data.find_all("a"):
			try:
				url = campo["href"]
				if "@" in url and "://" not in url:#Caso de que sea un email y no una URL
					url = "-"
					continue
				elif url == "http://" or url == "https://":#En la etiqueta solo se hallaba el protocolo
					url = campo.text
					url = url.replace(" ","").replace("\n","").replace("\t","").replace("\r","").replace("(","").replace(")","")
					url = re.sub("\t|\n|\r|(|)","",url)
					break
				elif "r-project" in url or "python.org" in url or "#supplementary-data" in url: #Esto es en el caso de que me den la URL de un lenguaje R o python
					url = "-"
					continue
				else: #Es una URL valida
					url = url.replace(" ","").replace("\n","").replace("\t","").replace("\r","").replace("(","").replace(")","")
					url = re.sub("\t|\n|\r|(|)","",url)
					break
			except: #No hay URL asociada
				url = "-"
				continue #En el caso de que haya un tag "a" que no tenga href
    
    #Vamos a comprobar que la url no es material suplementario
		if "Supplementary_Data" in url and "bioinformatics" in url:
			url = '-'
		elif "supplementary_material" in url and "bioinformatics" in url:
			url = "-"
		elif "supplementary_thesis" in url and "bioinformatics" in url:
			url = "-"
		elif "supplementaryinformation" in url and "bioinformatics" in url:
			url = "-"
		elif "supplementary_information" in url and "bioinformatics" in url:
			url = "-"
		elif "/Journal/bioinformatics/" in url:
			url = "-"
            
	else: #Si se establecio una URL
		url = url.replace(" ","").replace("\n","").replace("\t","").replace("\r","").replace("(","").replace(")","")
		url = re.sub("\t|\n|\r|(|)","",url)
	r = re.compile(".*oup\.silver.*/Journal/bioinformatics/.*")
	p = re.compile("http://http.*")
	if r.match(url):
		url = "-"
	if p.match(url):
		url = url.replace("http://http//","http://").replace("http://http:w","http://w").replace("http://http:/","http://")
	if "mailto:" in url: #Esto es para una especifica del volumen 21 issue 14
		url = url.replace("mailto:","http://")
	return (abstract, url)


def info_json(data):
#Funcion que recibe parte del contenido del HTML de un articulo y devuelve el titulo, doi, los autores y el numero de id de bioinformatics
	dic = json.loads(data.string)
	#Obtenemos la informacion de este articulo
	titulo = dic["name"]
	doi = dic["url"]
	numero = dic["sameAs"].split("/")
	numero_id = numero[-1]
	dic_autores = dic["author"]
	autores = []

	for autor in dic_autores:#Los autores estan en otro diccionario dentro del json
		if autor["name"] == ", ":
			continue
		autores.append(autor["name"])
	for i, autor in enumerate(autores):
		autor = re.sub("\t|\n|\r","",autor)
		autores[i] = autor.replace("\t","").replace("\n","").replace("\r","")
	return (numero_id, titulo, autores, doi)


def extraccion(soup):
#Funcion que devuelve todas las referencias de las paginas dicionales de citaciones
	if soup.find("div", class_="crossref-citedby__message--empty"): #Mensaje que te sale si no hay citaciones a este paper
		return ([])

	data3 = soup.find("div",class_="crossref-citedby__text")
	data = []
	for sibling in data3.next_siblings: #Tratamos a cada refrencia por separado de esta manera
		if sibling == "\n": #Cada 2 hermanos hay un salto de carro
			continue
		else:
			doi = sibling.a["href"]
			doi = re.sub("\t|\n|\r","",doi)
			doi = doi.strip()

			titulo = str(sibling.a.string)
			titulo = re.sub("\t|\n|\r","",titulo)
			titulo = titulo.strip()

			text = sibling(class_="crossref-citedby__entry-citation")[0]
			citacion = str(text.em.string)+str(text.contents[2])
			citacion = re.sub("\r|\n|\t|^\s","",citacion)

			try:
				autores = sibling.ul.text
				autores = autores.split("\n")
				lista_autores = autores[1:len(autores)-1]
				lista_autores_final = []
				for autor in lista_autores:
					autor = re.sub("\t|\n|\r","",autor)
					autor = autor.replace("\n","").replace("\t","").replace("\r","")
					autor = autor.strip()
					lista_autores_final.append(autor)
				data.append([doi,titulo,citacion,lista_autores_final])
			except:#El articulo no tiene autores
				data.append([doi,titulo,citacion,[]])
	
	citaciones = []
	for citacion in data: #Esta parte es para facilitar luego el procesamiento de esta informacion
		citacion[2] = citacion[2].strip()
		if citacion[2][-1] == ",":
			citacion[2] = citacion[2][:-1]
		citaciones.append((citacion[0], citacion[1:]))
	return citaciones


def citation(codigo):
#Funcion que coge el codigo de identificacion del articulo de bioinformatics y devuelve todos los articulos que referencian a este
	nombre_archivo = codigo+"_ref.html"
	try:
		file_cross = open("/home/ana/urbion/TFG/ArchivosBioinformatics/"+nombre_archivo, "r")
	except:
		excepts.write(str(nombre_archivo)+"\tNo se da el archivo de las referencias\n")
		return("citaciones")

	if os.stat("/home/ana/urbion/TFG/ArchivosBioinformatics/"+nombre_archivo).st_size == 0:#Esta vacio el HTML
		file_cross.close()
		vacios.write(url+"\n")
		return ("El HTML estaba vacio")
	
	
	soup3 = BS(file_cross, 'lxml')
	#Sacamos los datos de esta pagina
	citaciones = extraccion(soup3)
	file_cross.close()
	#Despues de sacar el HTML y las referencias de la primera pagina(en ocasiones unica) vamos a ver si hay mas paginas de referencias
	try:
		paginacion = soup3.find("div", class_ = "pageNumbers al-pageNumbers")
		numero_paginas = paginacion.find_all("a")
		numero = numero_paginas[-1]["data-clicked-page"]
		for i in range(2, int(numero)+1):
			nombre_archivo = codigo+"_"+str(i)+"_ref.html"
			try:
				file_cross = open("/home/ana/urbion/TFG/ArchivosBioinformatics/"+nombre_archivo, "r")
			except:
				excepts.write(str(nombre_archivo)+"\tno se ha dado la pagina de las citaciones\n")
				return("citaciones")

			soup = BS(file_cross, 'lxml')
			lista = extraccion(soup)
			for referencia in lista:
				citaciones.append(referencia)
			file_cross.close()
	except: #Significa que solo hay una pagina de referencias
		pass	
	return citaciones


def datos(url):
#Funcion que cogiendo la URL de un articulo, devuelve los siguientes datos: 1.URL, 2.Numero de id 3.titulo, 4.autores, 5.DOI, 6.abstract, 7.URL de la herramienta, 8.Papers que lo referencian
	codigo = url.split("/")
	codigo = "_".join(codigo[-4:])#Obtenemos el 
	try: #Para saber si ese HTML esta o no en la carpeta de trabajo
		file_in = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/"+codigo+".html", "r")
	except:
		os.system(wget_com+url+'" -O '+"/home/amanhel/Documents/TFG/ArchivosBioinformatics/"+codigo+".html")
		file_in = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/"+codigo+".html", "r")
		time.sleep(random.randrange(25,85))
	
	if os.stat("/home/amanhel/Documents/TFG/ArchivosBioinformatics/"+codigo+".html").st_size == 0:
		file_in.close()
		vacios.write(url+"\n")
		return ([url,"El HTML estaba vacio","-","-","-","-","-","-"])	
    
	soup2 = BS(file_in, 'lxml')
	data = soup2.find(type="application/ld+json")
	try:#ªHay ocasiones que es un escaneado del PDF y no tiene abstract
		data2 = soup2.find("h2", class_="abstract-title")
		data2 = data2.next_sibling.next_sibling
		(abstract_txt, url_herramienta) = abstract_url(data2) #Obtenemos el abstract y la URL de la herramienta
	except:
		(abstract_txt, url_herramienta) = ("-","-")
        
	(numero_id, titulo, autores, doi) = info_json(data) #Obtenemos los demas datos
	file_in.close()
	
	
	#Ahora vamos a sacar las referencias de cada articulo
	references = citation(numero_id)
	
	return([url, numero_id, titulo, autores, doi, abstract_txt, url_herramienta, references])




#Programa principal

volumenes = [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 10), (15, 12), (16, 12), (17, 12), (18, 12), (19,18), (20, 18), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24), (28, 24), (29, 24), (30, 24), (31, 24), (32, 24) (33, 24), (34, 24)]

#En la variable vacios almacenaremos los URLs que necesitamos de nuevo procesar ya que por errores con el servidor dan problemas
vacios = open("/home/amanhel/prueba/Documents/TFG/ArchivosBioinformatics/URLsVacios.txt","w")
#En la variable excepts estaran lso archivos que han dado algun tipo de error y que necesitaran una revision y arreglo
excepts = open("/home/amanhel/prueba/Documents/TFG/ArchivosBioinformatics/URLsVacios.txt","w")

wget_com = 'wget --user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" --referer="https://www.google.com" --timeout=300 --tries=4 "'

for tupla in volumenes: #Recorremos los volumenes
	issue_max = tupla[1]
	vol = tupla[0]
	for issue in range(1,issue_max+1): #Recorremos las publciaciones de cada volumen
		if vol == 15 and issue == 8: #No existe
			continue
		url = "https://academic.oup.com/bioinformatics/issue/"+str(vol)+"/"+str(issue)
		archivo = "Vol"+str(vol)+"Issue"+str(issue)+".html"
        
		try:#Control para no descargar dos veces el archivo
			file_vol = open("/home/amanhel/prueba/Documents/TFG/ArchivosBioinformatics/"+archivo,"r")
		except:#Descargamos el archivo que no consta en la carpeta
			os.system(wget_com+url+'" -O '+"/home/amanhel/prueba/Documents/TFG/ArchivosBioinformatics/"+archivo)
			file_vol = open("/home/amanhel/prueba/Documents/TFG/ArchivosBioinformatics/"+archivo, "r")	

		#Cogemos los articulos de Applications Notes de cada issue
		if os.stat("/home/amanhel/prueba/Documents/TFG/ArchivosBioinformatics/"+archivo).st_size == 0: #Caso de que el HTML este vacio por errores de conexion
			file_vol.close()
			vacios.append(url,"\n")
			continue

		articulos_issue = articulos(file_vol) #Sacamos todos los articulos de una publicacion

		#Ya tenemos en la variable "articulos" los URLs de los papers que se atribuyen a este Issue de este Volume
		todos_datos = [] #Matriz que contendra todos los datos de los articulos de este Issue
		for url in articulos_issue:#Recorremos todos lso articulos de Application Notes
			time.sleep(random.randrange(20,70))#Tiempo indicado para que no bloqueen la IP
			datos_url = datos(url)
			todos_datos.append(datos_url)
            
		#Ya tenemos todos los datos de todas las URL de este Issue
		#Vamos a crear un archvio csv con los datos que tenemos
		tabla = pd.DataFrame(todos_datos, columns=["URLArticulo", "IDArticulo", "Titulo", "Autores", "DOI", "Abstract", "Herramienta", "Referencias"])
		tabla.to_csv("/home/amanhel/prueba/Documents/TFG/ArchivosBioinformatics/Vol"+str(vol)+"Issue"+str(issue)+".csv", index = False)
		file_vol.close()
		time.sleep(random.randrange(200,300))