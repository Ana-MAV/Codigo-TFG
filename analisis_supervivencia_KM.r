#Script para el analisis de supervivencia con Kaplan-Meier
library(survival)
library(ggplot2)
library(dplyr)
library(survminer)
library(ggpubr)

#Importamos los datos
datos_filtrados <- read.csv("C:/Users/anama/OneDrive/Documentos/2019-2020/Practicas/analisisR/datos_bio+nar_filtrados.csv")

#KM con todos los datos
#Calculamos las curvas con los datos
km_fit <- survfit(Surv(dias_min, Censored) ~ 1, data=datos)
km_fit_max <- survfit(Surv(dias_max, Censored) ~ 1, data=datos)
km_fit_med <- survfit(Surv(dias_media, Censored) ~ 1, data=datos)

#Hacemos las gráficas de las curvas
fit <- list(SetFechaMinima = km_fit, SetFechaMaxima = km_fit_max, SetFechaMedia = km_fit_med)
ggsurvplot_combine(fit,
                   data=datos,
                   combine=TRUE,
                   conf.int=TRUE,
                   censor=TRUE,
                   palette="jco",
                   legend="right",
                   legend.title="Set De Datos",
                   ggtheme = theme_gray(),
                   legend.labs=c("FechasMin","FechasMax","FechasMed")) + labs(x="Dias",y="S(t)")


#Revistas
km_revista_fit <- survfit(Surv(dias_media, Censored) ~ Revista, data=datos_filtrados)
ggsurvplot(km_revista_fit,
                palette = c("turquoise3","violetred3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Revista",
                ggtheme = theme_gray(),
                title="A)",
                legend.labs=c("Bioinformatics","NAR"))+
  labs(x="Dias",y="S(t)")
km_revista_fit_min <- survfit(Surv(dias_min, Censored) ~ Revista, data=datos_filtrados)
ggsurvplot(km_revista_fit_min,
                palette = c("turquoise3","violetred3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Revista",
                title="B)",
                ggtheme = theme_gray(),
                legend.labs=c("Bioinformatics","NAR"))+
  labs(x="Dias",y="S(t)")
km_revista_fit_max <- survfit(Surv(dias_max, Censored) ~ Revista, data=datos_filtrados)
ggsurvplot(km_revista_fit_max,
                palette = c("turquoise3","violetred3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Revista",
                ggtheme = theme_gray(),
                title = "C)",
                legend.labs=c("Bioinformatics","NAR"))+
  labs(x="Dias",y="S(t)")

#Test de comparacion de hipotesis para las curvas calculadas con las revistas
surv_diff_media <- survdiff(Surv(dias_media, Censored) ~ Revista, data = datos_filtrados)
surv_diff_media #Es un test log-rank
surv_diff_min <- survdiff(Surv(dias_min, Censored) ~ Revista, data = datos_filtrados)
surv_diff_min #Es un test log-rank
surv_diff_max <- survdiff(Surv(dias_max, Censored) ~ Revista, data = datos_filtrados)
surv_diff_max #Es un test log-rank



#Citaciones
#Separando por la mediana
surv_mediana_min<-survfit(Surv(dias_min, Censored) ~ GrupoMediana, data=datos_filtrados)
ggsurvplot(surv_mediana_min,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "A)",
                legend.labs=c("Datos menor o igual a 13","Datos mayores a 13"))+
  labs(x="Dias",y="S(t)")

surv_mediana <- survfit(Surv(dias_media, Censored) ~ GrupoMediana, data=datos_filtrados)
ggsurvplot(surv_mediana,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "B)",
                legend.labs=c("Datos menor o igual a 13","Datos mayores a 13"))+
  labs(x="Dias",y="S(t)")

surv_mediana_max <- survfit(Surv(dias_max, Censored) ~ GrupoMediana, data=datos_filtrados)
ggsurvplot(surv_mediana_max,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "C)",
                legend.labs=c("Datos menor o igual a 13","Datos mayores a 13"))+
  labs(x="Dias",y="S(t)")

#Los test log-rank para saber si son diferentes las curvas de las medianas
surv_diff_mediana_min <- survdiff(Surv(dias_min, Censored) ~ GrupoMediana, data = datos_filtrados)
surv_diff_mediana_min

surv_diff_mediana <- survdiff(Surv(dias_media, Censored) ~ GrupoMediana, data = datos_filtrados)
surv_diff_mediana

surv_diff_mediana_max <- survdiff(Surv(dias_max, Censored) ~ GrupoMediana, data = datos_filtrados)
surv_diff_mediana_max

#Separando las citaciones por cuartiles
surv_cuantiles_min <- survfit(Surv(dias_min, Censored) ~ GrupoCuantiles, data=datos_filtrados)
a1 <- ggsurvplot(surv_cuantiles_min,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "A)",
                 legend.labs=c("Datos menor o igual a 4","Datos mayores a 4 y menores o iguales a 13","Datos mayores que 13 y menores o iguales a 41","Datos mayores a 41"))+
  labs(x="Dias",y="S(t)")
surv_cuantiles <- survfit(Surv(dias_media, Censored) ~ GrupoCuantiles, data=datos_filtrados)
b1 <- ggsurvplot(surv_cuantiles,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "B)",
                 legend.labs=c("Datos menor o igual a 4","Datos mayores a 4 y menores o iguales a 13","Datos mayores que 13 y menores o iguales a 41","Datos mayores a 41"))+
  labs(x="Dias",y="S(t)")
surv_cuantiles_max <- survfit(Surv(dias_max, Censored) ~ GrupoCuantiles, data=datos_filtrados)
c1 <- ggsurvplot(surv_cuantiles_max,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "C)",
                 legend.labs=c("Datos menor o igual a 4","Datos mayores a 4 y menores o iguales a 13","Datos mayores que 13 y menores o iguales a 41","Datos mayores a 41"))+
  labs(x="Dias",y="S(t)")

#Vamos a hacer los test log-rank
surv_diff_cuantiles_min <- survdiff(Surv(dias_min, Censored) ~ GrupoCuantiles, data = datos_filtrados)
surv_diff_cuantiles <- survdiff(Surv(dias_media, Censored) ~ GrupoCuantiles, data = datos_filtrados)
surv_diff_cuantiles_max <- survdiff(Surv(dias_max, Censored) ~ GrupoCuantiles, data = datos_filtrados)
surv_diff_cuantiles_min
surv_diff_cuantiles
surv_diff_cuantiles_max