library(icenReg)
library(ggplot2)
library(survival)

#Calcular la curva ejemplo de Turnbull
data(miceData)
np_fit = ic_np(cbind(l,u)~0,data=miceData)
plot(np_fit)
xlab="t"
ylab="S(t)"

#Importamos los datos de nuestro estudio
datos_filtrados_turn <- read.csv("C:/Users/anama/OneDrive/Documentos/2019-2020/Practicas/analisisR/datos_bio+nar_filtrados_turnbull.csv")
datos_km <- read.csv("C:/Users/anama/OneDrive/Documentos/2019-2020/Practicas/analisisR/datos_bio+nar_filtrados.csv")

#Creamos los objeto del análisis de supervivencia
surv_obj <- Surv(datos_0$Tiempo1,datos_0$Tiempo2,type="interval2")
fit_km <- survfit(Surv(dias_media,Censored)~1,data=datos_km)
fit_icenReg <- ic_np(cbind(Tiempo1,Tiempo2)~0,data=datos)

#Comparamos la K-M con la nueva de Turnbull
plot(fit_icenReg,
     main = "",
     col = "gray30",
     xlab="Dias")
lines(fit_km,col="green")
legend(x="topright",
       legend=c("KM con fecha muerte media","Estimador Turnbull"),
       fill=c("green","gray30"),
       box.lty=0)