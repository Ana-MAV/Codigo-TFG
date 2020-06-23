#Script destinado al análisis descriptivo de los datos
library(ggplot2)
library(tidyverse)

#Importamos los datos
datos_combinacion <- read.csv("C:/Users/anama/OneDrive/Documentos/2019-2020/Practicas/analisisR/datos_bio+nar_sin_filtrar.csv")

#Histograma de los estados de las herramientas de ambas revistas
ggplot(datos_combinacion, aes(x = Estado, fill = Revista)) +
  geom_bar(position = "dodge") +
  labs(xlab="Estado") +
  ylab("Herramientas") +
  scale_fill_manual(values=c("turquoise3","violetred3"))+
  geom_text(stat='count', aes(label=..count..), vjust=-0.5)


#Histogramas de las herramientas vivas y muertas por año
#Filtramos los datos por años
datos_bio <- filter(datos_combinacion,Revista == "Bio")
datos_bio <- select(datos_bio, URL, Volumen, Estado)
datos_nar <- filter(datos_combinacion,Revista == "NAR")
datos_nar <- select(datos_nar, URL, Volumen, Estado)
#Bioinformatics
ggplot(datos_bio, aes(x = Volumen, fill = Estado)) +
  geom_bar(position = "stack") +
  labs(title="A)", xlab = "Año") +
  scale_x_continuous(breaks = seq(1985, 2019, by = 1), limits = c(1985,2020)) +
  scale_y_continuous(breaks = seq(0, 400, by = 50), limits = c(0, 400)) +
  theme(axis.title.x=element_blank(), axis.title.y = element_blank()) +
  scale_fill_manual(values=c("chartreuse3", "red3"))
#NAR
ggplot(datos_nar, aes(x = Volumen, fill = Estado)) +
  geom_bar(position = "stack") +
  labs(title="B)", xlab = "Año") +
  scale_x_continuous(breaks = seq(1985, 2019, by = 1), limits = c(1985, 2020)) +
  scale_y_continuous(breaks = seq(0, 400, by = 50), limits = c(0, 400)) +
  theme(axis.title.x=element_blank(), axis.title.y = element_blank()) +
  scale_fill_manual(values=c("chartreuse3", "red3"))



#Importamos los datos filtrados
datos_combinacion <- read.csv("C:/Users/anama/OneDrive/Documentos/2019-2020/Practicas/analisisR/datos_bio+nar_filtrados.csv")

#Distribución de densidades de los datos filtrados
plot(density(datos$dias_max), ylim = c(0,0.0003), main = NA, xlab = "Dias", ylab = "Densidad", col = "royalblue3")
lines(density(datos$dias_min), col = "darkgoldenrod1")
legend("right", legend = c("FechasMax", "FechasMin"), lty = c(1,1), col = c("royalblue3","darkgoldenrod1"), bty = "n")

#Diagrama de cajas de los dias de supervivencia por año y revista
ggplot(datos_filtrados, aes(x=factor(Anualidad), y=dias_media, fill=Revista)) +
  geom_boxplot() +
  ylab("Dias") + 
  scale_fill_manual(values=c("turquoise3","violetred3")) +
  theme(axis.title.x=element_blank())