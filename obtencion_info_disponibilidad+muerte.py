#Script que junta todos los pasos necesarios desde que tenemos los datos de los volumenes
import pandas as pd
import requests
import requests.exceptions
import urllib.request
import urllib.error
import urllib.parse
import os
import sys
import re
import ssl

#Primero sacamos las urls de Bioinformatics y las separamos por ftps y https
volumenes_bioinformatics = [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 10), (15, 12), (16, 12), (17, 12), (18, 12), (19,18), (20, 18), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24), (28, 24), (29, 24), (30, 24), (31, 24), (32, 24), (33, 24), (34, 24), (35, 24)]
urls_http = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_http_url.txt", "w")
urls_ftps = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_ftp_url.txt", "w")
urls_http_cod = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_http_id.txt", "w")
urls_ftp_cod = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_ftp_id.txt", "w")
for pareja in volumenes_bioinformatics:#Recorremos por los volumenes
	volumen = pareja[0]
	issue_max = pareja[1]
	for issue in range(1, issue_max+1):#Recorremos los issues de cada volumen
		if volumen == 15 and issue == 8:
			continue
		data_bio = pd.read_csv("/home/amanhel/Documents/TFG/Bioinformatics/Vol"+str(volumen)+"Issue"+str(issue)+".csv")
		for i in range(0, len(data_bio.index)):#Recorremos las filas de los csv
			fila = data_bio.iloc[i]
			id_articulo = fila["IDArticulo"]
			url = str(fila["Herramienta"])
			if "ftp" in url:
				urls_ftps.write(url+"\n")
				urls_ftp_cod.write(str(id_articulo)+"\n")
			elif url == '-':
				continue
			elif url == "nan":
				continue
			else:
				urls_http.write(url+"\n")
				urls_http_cod.write(str(id_articulo)+"\n")
urls_http.close()
urls_ftps.close()




#Segundo sacamos las urls de NAR y las separamos por ftps y https --> hecho
vol_inicial = 32
vol_final = 47
urls_http = open("/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_http_url.txt", "w")
urls_ftp = open("/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_ftp_url.txt", "w")
urls_http_cod = open("/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_http_id.txt", "w")
urls_ftp_cod = open("/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_ftp_id.txt", "w")
for vol in range(vol_inicial, vol_final+1):#Recorremos los volumenes
	if vol < 40:
		data_nar = pd.read_csv("/home/amanhel/Documents/TFG/ArchivosNucleic/Vol"+str(vol)+"Issuesuppl_2.csv")
	else:
		data_nar = pd.read_csv("/home/amanhel/Documents/TFG/ArchivosNucleic/Vol"+str(vol)+"IssueW1.csv")
	for j in range(0, len(data_nar.index)):#Recorremos las filas de los csv
			fila = data_nar.iloc[j]
			id_articulo = fila["IDArticulo"]
			url = fila["Herramienta"]
			if "ftp" in str(url):
				urls_ftp.write(url+"\n")
				urls_ftp_cod.write(str(id_articulo)+"\n")
			elif url == '-':
				continue
			elif str(url) == "nan":
				continue
			else:
				urls_http.write(url+"\n")
				urls_http_cod.write(str(id_articulo)+"\n")
urls_http.close()
urls_ftp.close()






#Tercero hacemos el wget de los https de Bioinformatics y NAR
os.system('wget --user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" --referer="https://www.google.com" --timeout=100 --tries=4 --no-check-certificate -i "/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_http_url.txt" -o "/home/amanhel/Documents/TFG/ArchivosBioinformatics/output_wget_bio.txt" -O "/dev/null"')
os.system('wget --user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" --referer="https://www.google.com" --timeout=100 --tries=4 --no-check-certificate -i "/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_http_url.txt" -o /home/amanhel/Documents/TFG/ArchivosNucleic/"output_wget_nar.txt" -O "/dev/null"')
#Los documentos que obtenemos seran los outputs de haber intentado buscar con wget las urls





#Cuarto hacemos el proceso de urllib de los ftps de Bioinformatics y NAR:
def resultados_ftp(data, nombre_archivo_output, nombre_archivo_id):
	lineas = []
	file_in = open(nombre_archivo_id, "r").readlines()
	for x,URL in enumerate(data):
		row = URL.replace("\r","").replace("\n","")#Para quitar el salto de carro que estaba en todas las URLs
		id_articulo = file_in[x]
		try: #No habría error
			row = urllib.parse.urlsplit(row)
			row = list(row)
			row[2] = urllib.parse.quote(row[2])
			row = urllib.parse.urlunsplit(row)
			req = urllib.request.Request(row, headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0", "Referer":"https://www.google.com"})
			context = ssl._create_unverified_context()
			code = urllib.request.urlopen(req, context=context).getcode() #Para evitar que salgan los errores de SSL
			if "ftp://" in row and str(code).upper() == "NONE":
				code = str(200)
			lineas.append([id_articulo, row, code, "OK"])
		except urllib.error.HTTPError as e: #HTTP error
			code = e.code
			error = e.reason
			lineas.append([id_articulo, row, code, error])
		except urllib.error.URLError as u: #URL, FTP error o SSl error
			p = re.compile("\[Errno (\d+|-\d+|-\d)\]") #Para errores URL
			r = re.compile("ftp error:.*\('(\d+) .*'\)") #Para uno de los errores FTP
			r2 = re.compile('ftp error:.*\("(\d+) .*"\)') #Para otro de los errores FTP
			r3 = re.compile("ftp error:.*\((\d+).*\)") #Para otro de los errores FTP
			code = str(u.reason)
			if p.match(code):
				codigo = p.match(code).group(1)
				sentencia = str(id_articulo)+"\t"+row+"\t"+codigo+"\t"+code+"\n"
				lineas.append([id_articulo, row, codigo, code])
			elif r.match(code):
				codigo = r.match(code).group(1)
				sentencia = str(id_articulo)+"\t"+row+"\t"+codigo+"\t"+code+"\n"
				lineas.append([id_articulo, row, codigo, code])
			elif r2.match(code):
				codigo = r2.match(code).group(1)
				sentencia = str(id_articulo)+"\t"+row+"\t"+codigo+"\t"+code+"\n"
				lineas.append([id_articulo, row, codigo, code])
			elif r3.match(code):
				codigo = r3.match(code).group(1)
				sentencia = str(id_articulo)+"\t"+row+"\t"+codigo+"\t"+code+"\n"
				lineas.append([id_articulo, row, codigo, code])
			else:
				lineas.append([id_articulo, row, code, "Error sin numero"])
		except:
			lineas.append([id_articulo, row, 0, "Error desconocido"])
	tabla = pd.DataFrame(data=lineas,columns=["ID", "URL", "Codigo", "Mensaje"])
	tabla.to_csv(nombre_archivo_output,index=False)
	return
	

urls_bio = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_ftp_url.txt", "r").readlines()
urls_nar = open("/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_ftp_url.txt", "r").readlines()

resultados_ftp(urls_bio, "/home/amanhel/Documents/TFG/ArchivosBioinformatics/codigos_bio_ftp.csv", "/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_ftp_id.txt")
resultados_ftp(urls_nar, "/home/amanhel/Documents/TFG/ArchivosNucleic/codigos_nar_ftp.csv", "/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_ftp_id.txt")









#Quinto hacemos la extraccion de los codigos wget y damos los codigos de urllib de los https de Bioinformatics

file_in = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/output_wget_bio.txt", "r")
file_in_nar = open("/home/amanhel/Documents/TFG/ArchivosNucleic/output_wget_nar.txt", "r")
data_bio = file_in.readlines()
data_nar = file_in_nar.readlines()

#Separamos cada parrafo que equivaldra a los mensajes de cada url, lo guardaremos en mensajes_urls
contol = 0
for data in (data_bio, data_nar):
    control += 1
    parrafo = []
    mensajes_urls = []
    for i, line in enumerate(data):
    	if line == "\n":
    		if "0K" in data[i+1] or "0K" in data[i-1]:
    			continue
    		elif "(intento: " in data[i+1]:
    			continue
    		else:
    			mensajes_urls.append(parrafo)
    			parrafo = []
    	elif "wget: no se pudo resolver la dirección del equipo" in line and "--2020-" in data[i+1]:#No se ha dado un codigo de error pero no se pudo establecer la conexion
    		parrafo.append(line.replace("\n",""))
    		mensajes_urls.append(parrafo)
    		parrafo = []
    	elif "wget: no se pudo resolver la dirección del equipo" in line and "URL transformed to HTTPS due to an HSTS policy" in data[i+1]:
    		parrafo.append(line.replace("\n",""))
    		mensajes_urls.append(parrafo)
    		parrafo = []
    	elif "No se pudo establecer la conexión SSL." in line:
    		parrafo.append(line.replace("\n",""))
    		mensajes_urls.append(parrafo)
    		parrafo = []
    	elif "Sobrepasadas las 20 redirecciones." in line:
    		parrafo.append(line.replace("\n",""))
    		mensajes_urls.append(parrafo)
    		parrafo = []
    	elif "URL transformed to HTTPS due to an HSTS policy" in line:
    		continue
    	elif "falló: " in line and "URL transformed to HTTPS due to an HSTS policy" in data[i+1]:
    		parrafo.append(line.replace("\n",""))
    		mensajes_urls.append(parrafo)
    		parrafo = []
    	elif "falló: " in line and "--2020-" in data[i+1]:
    		parrafo.append(line.replace("\n",""))
    		mensajes_urls.append(parrafo)
    		parrafo = []
    	elif "ACABADO" in line: #Sera la ultima URL ya
    		mensajes_urls.append(parrafo)
    		break
    	else:
    		parrafo.append(line.replace("\n",""))
    if not mensajes_urls[-1]: #Caso de que el ultimo elemento este vacio, para que no estorbe
    	mensajes_urls.pop()
    
    #Cogemos los codigos y los mensajes extraidos de los URLs sacados con wget y guardamos los codigos y razones de cada una en frases
    frases = []
    for mensaje in mensajes_urls:
    	try:#Sacamos la URL de la página que estamos buscando el estado
    		url = mensaje[1].split("--  ")
    		url = url[1]
    	except:
    		url = mensaje[0].split("--  ")
    		url = url[1]
    	r = re.compile(".* ERROR (\d+): (.*)") #Tiene que matchear toda la frase, no vae con que solo encuentre una parte
    	r2 = re.compile(".*esperando respuesta... (\d+) (.*)")
    	try: #En el caso de que haya algun error que pueda reconocer (ERROR ...: ...)
    		codigo = r.match(mensaje[-1]).group(1)
    		razon = r.match(mensaje[-1]).group(2)
    	except: #Otro tipo de error o un 200
    		if "Guardando como: “/dev/null”" in mensaje: #Primero comprobamos si la URL sigue operativa, tiene que ser la expresion completa de la linea, si no, no lo toma como True
    		#"Petición HTTP enviada, esperando respuesta... 200 OK" in mensaje or "Petición HTTP enviada, esperando respuesta... 200" in mensaje --> estas son las alternativas, pero funciona mejor lo que esta en el codigo
    			codigo = 200
    			razon = "OK"
    		elif mensaje[-1] == "Abandonando.":#Se ha reintentado 4 veces y no se ha dado la conexion
    			codigo = 404
    			razon = "Maximo intentos"
    		elif mensaje[-1] == "No se pudo establecer la conexión SSL.":
    			codigo = 222
    			razon = "No se pudo establecer la conexión SSL."
    		elif "wget: no se pudo resolver la dirección del equipo" in mensaje[-1]:
    			codigo = "404"
    			razon = "No se pudo resolver la dirección del equipo"
    		elif "Sobrepasadas las 20 redirecciones." in line:
    			parrafo.append(line.replace("\n",""))
    			mensajes_urls.append(parrafo)
    			parrafo = []
    		elif r2.match(mensaje[-1]): #el error 401
    			codigo = r2.match(mensaje[-1]).group(1)
    			razon = r2.match(mensaje[-1]).group(2)
    		else: #Otro tipo de error
    			codigo = 123
    			razon = mensaje[-1]+"***"
    	#Vamos a ver si se redirecciona y cuantas veces lo hace
    	redirecciones = 0
    	for frase in mensaje:
    		red = re.compile(".*\[siguiente\]")
    		if red.match(frase):
    			redirecciones += 1
    	frases.append([url,codigo,razon,str(redirecciones)])
    
    #Ahora que tenemos los codigos y razones de lo wget, vamos a comprobar que estan bien, si no es asi, estableceremos la conexion con urllib
    frases_con_adicion = []
    for mensaje in frases:
    	codigo_wget = int(mensaje[1])
    	url = mensaje[0]
    	if codigo_wget != 200: #wget dice que no es funcional
    		#Intentamos hacer la conexion con urllib
    			row = mensaje[0]
    			try: #No habría error
    				row = urllib.parse.urlsplit(row)
    				row = list(row)
    				row[2] = urllib.parse.quote(row[2])
    				row = urllib.parse.urlunsplit(row)
    				req = urllib.request.Request(row, headers = {"user-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0", "referer":"https://www.google.com"})
    				context = ssl._create_unverified_context()
    				status_urllib = urllib.request.urlopen(req, context=context).getcode() #Para evitar que salgan los errores de SSL
    				razon_urllib = "OK"
    			except urllib.error.HTTPError as e: #HTTP error
    				status_urllib = e.code
    				razon_urllib = e.reason
    			except urllib.error.URLError as u: #URL, FTP error o SSl error
    				p = re.compile("\[Errno (\d+|-\d+|-\d)\]") #Para errores URL
    				r = re.compile("ftp error:.*\('(\d+) .*'\)") #Para errores FTP
    				razon_urllib = str(u.reason)
    				try:
    					try:
    						status_urllib = p.match(code).group(1)
    					except:
    						status_urllib = r.match(code).group(1)
    				except:
    					status_urllib = 123
    					razon_urllib = "Error sin numero"
    			except:
    				status_urllib = 345
    				razon_urllin = "Error desconocido"
    		
    		#Añadimos la busqueda de urllib
    		adicion = [status_urllib, razon_urllib]
    	else: #wget dice que esta funcional
    		adicion = ["-", "-"]
    	mensaje_ad = mensaje+adicion
    	frases_con_adicion.append(mensaje_ad)
    
    #Vamos a crear un archivo pandas con las urls y sus codigos
    file_id_bien = []
    if control == 1:#Bioinformatics
        urls_http_cod = open("/home/amanhel/Documents/TFG/ArchivosBioinformatics/urls_bio_http_id.txt", "r")
        direccion = "/home/anmanhel/Documents/ArchivosBioinformactis/codigos_urls_wget_bio.csv"
    else:#NAR
        urls_http_cod = open("/home/amanhel/Documents/TFG/ArchivosNucleic/urls_nar_http_id.txt", "r")
        direccion = "/home/anmanhel/Documents/ArchivosNucleic/codigos_urls_wget_nar.csv"
    for id_art in urls_http_cod.readlines():
    	file_id_bien.append(id_art.replace("\n",""))
    columnas = ["URL", "Codigo Wget", "Mensaje Wget", "Redirecciones Wget", "Codigo UrlLib", "Mensaje UrlLib"]
    tabla = pd.DataFrame(frases_con_adicion, columns = columnas)
    tabla.insert(0,"ID",file_id_bien)
    tabla.to_csv(direccion,index=False)


#Ahora vamos a adjuntar a los archivos csv que tenemos las fechas de su muerte (min y maxima)
def sustituir(a, b, frase):
#Función que sustituye el o los caracteres de "a" por el caracter "b" en la string "frase"
 	for char in a:
		frase = frase.replace(char, b)
 	return frase

def muerte(url, historial):
 	print("muerte")
#Función que nos da la fecha de muerte de la página leyendo en los mementos desde atras hasta encontrar un 200 o hasta el principio del historial
#Historial es un pandas donde cada uno de los mementos es una linea y las columnas que nos interesan son statuscode (codigo del memento) y timestamp (fecha)
 	i = len(historial.index)-1
 	while True:
		memento = historial.iloc[i]
		estado = memento["statuscode"]
		if estado == "200":
 			memento = historial.iloc[i]
 			fecha_min = memento["timestamp"]
 			memento = historial.iloc[i+1]
 			fecha_max = memento["timestamp"]
 			break
		elif i == 0:#Llegamos al principio del historial de los mementos sin encontrar un 200
 			fecha_min = "?"
 			fecha_max = memento["timestamp"]
 			break
		else:#Seguimos leyendo hacia arriba
 			i -= 1
 	#Ya tenemos la fecha, vamos a devolver una fecha de verdad
 	if fecha_min != "?" and fecha_max != "?":
		fecha_estetica_min = str(fecha_min[6:8]+"/"+fecha_min[4:6]+"/"+fecha_min[0:4])
		fecha_estetica_max = str(fecha_max[6:8]+"/"+fecha_max[4:6]+"/"+fecha_max[0:4])
 	elif fecha_min == "?":
		fecha_estetica_min = fecha_min
		fecha_estetica_max = str(fecha_max[6:8]+"/"+fecha_max[4:6]+"/"+fecha_max[0:4])
 	elif fecha_max == "?":
		fecha_estetica_min = str(fecha_min[6:8]+"/"+fecha_min[4:6]+"/"+fecha_min[0:4])
		fecha_estetica_max = fecha_max
 	else:
		pass
 	return (fecha_estetica_min, fecha_estetica_max)

def principal(url):
 	print("Principal")
#Funcion que devuelve el estado y el historial de la url que hemos dado
 	mementos_url = api_CDX(url)
 	if mementos_url.empty: #No esta en archive
		#print("no esta en archive")
		ult_cod = "1234"
		#Creando los datos para introducirlos a la matriz de la web
		web = url.split("://")
		web = web[1]
		web = web.split("/")
		parte_1 = web[0]
		parte_2 = web[1:]
		parte_1 = parte_1.split(".")
		final = str(parte_1[-1])
		i = len(parte_1)-2
		while i>=0:
 			final = final+","+parte_1[i]
 			i -= 1
		final = final+")"
		for parte in parte_2:
 			final = final+"/"+parte
		
		#Creando los datos para introducir a la matriz de la web		
		timestamp = str(datetime.datetime.now())
		timestamp = sustituir(["-",":"," "],"", timestamp)
		timestamp = timestamp[0:14]
		headers= ["urlkey","timestamp","original","mimetype","statuscode","digest","length"]
		mementos_url = pd.DataFrame([[final,timestamp,url,"-",ult_cod,"-","-"]],columns=headers)
		return("No esta en archive", mementos_url)
 	else: #Significa que hay algun dato en archive
		#print("hay algo en archive")	
		ult_cod = int(mementos_url.iat[-1,4])
		#print(ult_cod)
 	
 	if ult_cod == 200: #Significa que esta muerta pero en archive sale como operativa
		#print("esta en archive como operativa")
		i = len(mementos_url.index)-1
		memento = mementos_url.iloc[i]
		fecha_min = memento["timestamp"]
		fecha_estetica = str(fecha_min[6:8]+"/"+fecha_min[4:6]+"/"+fecha_min[0:4])
		return ("Fecha minima "+fecha_estetica+" - Fecha maxima ?", mementos_url)
 	elif ult_cod == 301 or ult_cod == 302 or ult_cod == 303:
		#print("hay redireccion")
		data = mementos_url
		last_line = data.iloc[-1]
		last_line = [last_line.urlkey, last_line.timestamp, last_line.original, last_line.mimetype, last_line.statuscode, last_line.digest, last_line.length]
		estado, data = redir(last_line, url, data)
		return (estado, data)
 	elif ult_cod == 403 or ult_cod == 404:
		#print("esta muerta")
		fecha_min, fecha_max = muerte(url, mementos_url)
		return (str("Fecha minima "+fecha_min+" - Fecha maxima "+fecha_max), mementos_url)
 	else:
		#print("error desconocido")
		fecha_min, fecha_max = muerte(url, mementos_url)
		return (str("Fecha minima "+fecha_min+" - Fecha maxima "+fecha_max), mementos_url)

def convertir(data):
#Funcion para convertir la string que nos da CDX a una matrix en la que cada memento es un elemento de la matriz
#El orden de cada memento es: urlkey, timestamp, original, mimetype, statuscode, digest, length
 	data_final = []
 	for memento in data:
		data_final.append(memento.split(" "))

 	#Pasamos a pandas	
 	header = ['urlkey', 'timestamp', 'original', 'mimetype', 'statuscode', 'digest', 'length']
 	data_tabla = pd.DataFrame(data_final,columns=header)	
 	return data_tabla

def api_CDX(url):
 	print("api_CDX")
#Funcion que extrae los mementos que te da la api CDX de la URL dada
 	url_1 = "http://web.archive.org/cdx/search/cdx?"
 	info = url_1 + urllib.parse.urlencode({"url":url,"filter":"!statuscode:-"})#Filtro los que no valen porque no me dan status code
 	uh = urllib.request.urlopen(info).read()
 	data = uh.decode('utf-8')
 	
 	#Comprobar si existe algun memento de la url en archive
 	if not data:
		return convertir(data)
 	else:
		data = data.split('\n')
		#Quitamos el ultimo porque va a quedarnos vacio por el formato de la pagina
		data.pop()
		return convertir(data)

def redir(memento, url, historial):
#Funcion para saber a que pagina se ha redirigido, devuelve la url a la que se redirige
	url_original = "https://web.archive.org/web/"+memento[1]+"/"+memento[2]
	r = requests.get(url_original)
	redirecciones = []
	for res in r.history:
		redirecciones.append(res.url)
	if len(redirecciones) == 2:
		url_final = redirecciones[1]
	elif len(redirecciones) > 2:
		url_final = redirecciones[2]
	else:
		url_final = r.url
	
	#Vamos a comparar las URLs para ver si se redirige a la misma o a otro dominio
	comparacion = url_final.split("/web/")
	webynum = comparacion[-1].split("/")
	num = webynum[0]
	del webynum[0]
	web = '/'.join(webynum)
	url_1 = "http://web.archive.org/cdx/search/cdx?"
	
	#Buscaremos este memento dentro de la API
	info = url_1 + urllib.parse.urlencode([("url",url),("filter","!statuscode:-"),("filter","timestamp:"+num),("filter","original:"+web)])		
	uh = urllib.request.urlopen(info).read()
	data = uh.decode('utf-8')
	if not data: #Se redirije a otra web
		estado, historial_nuevo = principal(web)
		historial_final = pandas.concat([historial,historial_nuevo],ignore_index=True)
		if estado == "Fecha de muerte desconocida":
			sentencia = "Muerta desde maximo "+muerte(url)
			return (sentencia, historial_final)
		else:
			return (estado, historial_final)
	else: #Esto significa que se redirige a si misma, por lo que esta muerta la pagina
		sentencia = "Muerta desde minimo "+muerte(url)
		return (sentencia, historial) 



#Programa
#Los historiales van a ser un archivo por cada url correspondiente a la historia con su nombre teniendo tanto los puntos como los slashs sustituidos por un barra-baja
data_bio_ftp = pd.read_csv("/home/amanhel/Documents/ArchivosBioinformatics/codigos_bio_ftp.csv")
data_bio_http = pd.read_csv("/home/amanhel/Documents/ArchivosBioinformatics/codigos_bio_ftp.csv")
data_nar_ftp = pd.read_csv("/home/amanhel/Documents/ArchivosNucleic/codigos_nar_ftp.csv")
data_nar_http = pd.read_csv("/home/amanhel/Documents/ArchivosNucleic/codigos_nar_ftp.csv")
if len(sys.argv) == 2 and sys.argv[1] == "-h": #Al ejecutar el codigo en la terminal si pones -h se da el historial
 	history = True
else:
 	history = False
control = 0
for data in (data_bio_ftp, data_bio_http, data_nar_ftp,data_nar_http):
    control += 1
    #Sacamos la url y los codigos
    muerte_min = [] #Guardaremos los valores de la columna muerte minima
    muerte_max = [] #Guardaremos los valores de la columna muerte maxima
    for i in range(0, len(data.index)):
     	row = data.iloc[i]
     	url = row["Herramienta"]
     	print(url)
     	codigo = str(row["Codigo"])
     	if codigo == "200":
    		muerte_min.append("-")
    		muerte_max.append("-")
    		if history:
     			pass
    		else:
     			continue
    
     	estado, historial = principal(url) #Si es 200 y no hay -h, no lo va a hacer
     	if history:
    		url = sustituir([".","/",":"], "_", url)
    		archivo_2 = url+".csv"
    		historial.to_csv(archivo_2, index=False)
     	
     	if estado == "No esta en archive":
    		#print("no en archive")
    		muerte_min.append("?")
    		muerte_max.append("?")
     	else:
    		#print("regex")
    		p = re.compile("Fecha minima (\?|\d+/\d+/\d+) - Fecha maxima (\?|\d+/\d+/\d+)")
    		muerte_min.append(p.match(estado).group(1))
    		muerte_max.append(p.match(estado).group(2))
    #Añadimos las columnas Fecha minima muerte y Fecha maxima muerte en el pandas data y crearemos otro archvio csv
    data["Fecha minima muerte"] = muerte_min
    data["Fecha maxima muerte"] = muerte_max
    if control == 1:
        archivo = "/home/amanhel/Documents/TFG/ArchivosBioinformatics/ftps_bio_muerte.csv"
    elif control == 2:
        archivo = "/home/amanhel/Documents/TFG/ArchivosBioinformatics/https_bio_muerte.csv"
    elif control == 3:
        archivo = "/home/amanhel/Documents/TFG/ArchivosNucleic/ftps_nar_muerte.csv"
    else:
        archivo = "/home/amanhel/Documents/TFG/ArchivosNucleic/https_nar_muerte.csv"
    data.to_csv(archivo, index = False)

#↨Hemos obtenido diferentes csvs en los que tenemos sus ids, disponibilidad y fechas de muerte
