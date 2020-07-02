# Codigo-TFG
Códigos en Python y R utilizados en el trabajo de fin de grado "Características sistémicas del ecosistema de herramientas web que dan soporte a la investigación en Biología Molecular"



A continuación se da un resumen de lo que desempeña cada código en el orden que deben ejecutarse

1. informacion_bioinformatics.py --> Este código esta diseñado para obtener los artículos correspondientes a softwares de la revista Bioinformatics

2. informacion_nar.py --> Este código esta diseñado para obtener los artículos correspondientes a softwares de la revista Nucleic Acids Research

2. obtencion_info_disponibilidad+muerte.py --> Obtenemos la disponibilidad de la herramienta informática en la actualidad y el intervalo de fecha en la que murio de Internet Archive

3. adicion_datos.py --> Se añaden a los datos obetenidos las citaciones y fechas en las que se publicaron los articulos de las herramientas

4. sacando_info_resultados.py --> Se obtiene el numero de articulos analizados y los que tienen softwares asociados

5. analisis_descriptivo_datos.r --> Realizacion de un analisis descriptivo de los datos obtenidos en los anteriores pasos

6. datos_analisis_KM.py --> Filtrado de los datos para adecuarlos al analisis de supervivencia con el estimador Kaplan-Meier

7. analisis_supervivencia_KM.r --> Realizacion del analisis de supervivencia con el estiadmor Kaplan-Meier de todos los datos y respecto a las revistas

8. analisis_KM_citaciones.r --> Realizacion del analisis de supervivencia con el estimador KAplan-Meier respecto a las citaciones

9. datos_analisis_turnbull.py --> Filtrado de los datos para adecuarlos al analisis de supervivencia con el estimador Turnbull 

10. analisis_supervencia_turnbull.r --> Realizacion del analisis de supervivencia con el estiadmor Turnbull de todos los datos

11. creador_ref_herr_muertas.py --> Este codigo crea el formato necesario para el siguiente paso. Para ello crea archivos para cada herramienta con el numero de referencias a las herramientas por año

12. citaciones_predictor_muerte.r --> Analiza si el patro temporal de citaciones es un predictor de muerte de las herrameinats en un tiempo proximo
