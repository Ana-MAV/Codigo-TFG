#Script para obtener los datos para el analisis de si las citaciones por año son un predictor de muerte
library(ggplot2)

filenames <- list.files(path="C:/Users/anama/OneDrive/Escritorio/ref_herr_muertas", pattern="*.csv", full.names=TRUE)
pendientes_50_min <- c()
pendientes_50_med <- c()
pendientes_50_max <- c()
pendientes_75_max <- c()
pendientes_75_min <- c()
pendientes_75_med <- c()
for(herramienta in filenames){
  datos <- read.csv(herramienta)
  #Eliminamos los articulos que tienen citaciones 0 en todos los años
  muerte_min <- datos[datos$muerte_min==1,"anualidad"]
  muerte_med <- datos[datos$muerte_med==1,"anualidad"]
  muerte_max <- datos[datos$muerte_max==1,"anualidad"]
  if (all(datos$citaciones == 0)){
    next
  }
  else{
    vida_media_min <- as.integer(datos[1,"anualidad"]+((muerte_min-datos[1,"anualidad"])/2))
    vida_media_med <- as.integer(datos[1,"anualidad"]+((muerte_med-datos[1,"anualidad"])/2))
    vida_media_max <- as.integer(datos[1,"anualidad"]+((muerte_max-datos[1,"anualidad"])/2))
    vida_75_min <- as.integer(datos[1,"anualidad"]+(0.75*(muerte_min-datos[1,"anualidad"])))
    vida_75_med <- as.integer(datos[1,"anualidad"]+(0.75*(muerte_med-datos[1,"anualidad"])))
    vida_75_max <- as.integer(datos[1,"anualidad"]+(0.75*(muerte_max-datos[1,"anualidad"])))
  }
  #Ya tenemos el valor de la vidas medias de la herramienta
  #Vamos a sacar las pendiendes entre los datos de 50% y 75% de vida y el año muerte
  citacion_vida_media_min <- datos[datos$anualidad==vida_media_min,"citaciones"]
  citacion_vida_media_med <- datos[datos$anualidad==vida_media_med,"citaciones"]
  citacion_vida_media_max <- datos[datos$anualidad==vida_media_max,"citaciones"]
  citacion_75_min <- datos[datos$anualidad==vida_75_min,"citaciones"]
  citacion_75_med <- datos[datos$anualidad==vida_75_med,"citaciones"]
  citacion_75_max <- datos[datos$anualidad==vida_75_max,"citaciones"]
  citacion_muerte_min <- datos[datos$anualidad==muerte_min,"citaciones"]
  citacion_muerte_med <- datos[datos$anualidad==muerte_med,"citaciones"]
  citacion_muerte_max <- datos[datos$anualidad==muerte_max,"citaciones"]
  

  #Miramos si son ceros las pendientes de los min
  if (citacion_muerte_min - citacion_vida_media_min == 0){
    pendiente_50_min <- 0
  }
  else{
    pendiente_50_min <- (citacion_muerte_min - citacion_vida_media_min)/(muerte_min-vida_media_min)
  }
  if (citacion_muerte_min - citacion_75_min == 0){
    pendiente_75_min <- 0
  }
  else{
    pendiente_75_min <- (citacion_muerte_min - citacion_75_min)/(muerte_min-vida_75_min)
  }
  
  #Miramos si son ceros las pendientes de los med
  if (citacion_muerte_med - citacion_vida_media_med == 0){
    pendiente_50_med <- 0
  }
  else{
    pendiente_50_med <- (citacion_muerte_med - citacion_vida_media_med)/(muerte_med-vida_media_med)
  }
  if (citacion_muerte_med - citacion_75_med == 0){
    pendiente_75_med <- 0
  }
  else{
    pendiente_75_med <- (citacion_muerte_med - citacion_75_med)/(muerte_med-vida_75_med)
  }
  
  #Miramos si son ceros las pendients de los max
  if (citacion_muerte_max - citacion_vida_media_max == 0){
    pendiente_50_max <- 0
  }
  else{
    pendiente_50_max <- (citacion_muerte_max - citacion_vida_media_max)/(muerte_max-vida_media_max)
  }
  if (citacion_muerte_max - citacion_75_max == 0){
    pendiente_75_max <- 0
  }
  else{
    pendiente_75_max <- (citacion_muerte_max - citacion_75_max)/(muerte_med-vida_75_max)
  }
  #Añadimos los valores de las pendientes que hemos obtenido
  pendientes_50_min <- append(pendiente_50_min,pendientes_50_min)
  pendientes_50_med <- append(pendiente_50_med,pendientes_50_med)
  pendientes_50_max <- append(pendiente_50_max,pendientes_50_max)
  pendientes_75_min <- append(pendiente_75_min,pendientes_75_min)
  pendientes_75_med <- append(pendiente_75_med,pendientes_75_med)
  pendientes_75_max <- append(pendiente_75_max,pendientes_75_max)
}
#Ya tenemos los valores de las pendientes desde la vida media y desde el 75% de los 3 set de datos


#Resultados muerte_maxima, los unicos que tenemos por ahora
plot(density(pendientes_50_min),
     main="",
     xlim=c(-5,5),
     col="gray30",
     xlab = "Pendiente",
     ylab = "Densidad")
xtick <- seq(-5,5,by=1)
axis(side=1,at=xtick)
lines(density(pendientes_75_min),col="red2")#Para añadir la de las pendientes_75
legend(x="right",
       legend=c("Vida Media","75% de la vida"),
       fill=c("gray30","red2"),
       box.lty=0)
lines(c(0,0),c(5,-5),lty=2)


plot(density(pendientes_50_med),
     main="",
     xlim=c(-5,5),
     col="gray30",
     xlab = "Pendiente",
     ylab = "Densidad")
xtick <- seq(-5,5,by=1)
axis(side=1,at=xtick)
lines(density(pendientes_75_med),col="red2")#Para añadir la de las pendientes_75
legend(x="right",
       legend=c("Vida Media","75% de la vida"),
       fill=c("gray30","red2"),
       box.lty=0)
lines(c(0,0),c(5,-5),lty=2)

plot(density(pendientes_50_max),
     main="",
     xlim=c(-5,5),
     col="gray30",
     xlab = "Pendiente",
     ylab = "Densidad")
xtick <- seq(-5,5,by=1)
axis(side=1,at=xtick)
lines(density(pendientes_75_max),col="red2")#Para añadir la de las pendientes_75
legend(x="right",
       legend=c("Vida Media","75% de la vida"),
       fill=c("gray30","red2"),
       box.lty=0)
lines(c(0,0),c(5,-5),lty=2)
