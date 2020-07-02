library(survival)
library(ranger)
library(ggplot2)
library(dplyr)
library(ggfortify)
library(grid)
library(gridExtra)
library(survminer)
library(ggpubr)

#Vamos a hacerlo con lso dias_media y con los grupos de cuantiles y mediana --> sale que hay diferencias
datos_grupos <- read.csv("C:/Users/anama/OneDrive/Documentos/2019-2020/Practicas/analisisR/datos_bio+nar_citaciones_antesdemorir.csv")
head(datos_grupos)

surv_mediana_min<-survfit(Surv(dias_min, Censored) ~ GrupoMedianaMin, data=datos_grupos)
a <- ggsurvplot(surv_mediana_min,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "A)",
                legend.labs=c("Datos menor o igual a 10","Datos mayores a 10"))+
  labs(x="Dias",y="S(t)")
surv_mediana <- survfit(Surv(dias_media, Censored) ~ GrupoMedianaMed, data=datos_grupos)
b <- ggsurvplot(surv_mediana,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "B)",
                legend.labs=c("Datos menor o igual a 12","Datos mayores a 12"))+
  labs(x="Dias",y="S(t)")
surv_mediana_max <- survfit(Surv(dias_max, Censored) ~ GrupoMedianaMax, data=datos_grupos)
c <- ggsurvplot(surv_mediana_max,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "C)",
                legend.labs=c("Datos menor o igual a 12","Datos mayores a 12"))+
  labs(x="Dias",y="S(t)")

#Los test log-rank para saber si son diferentes las curvas de las medianas
surv_diff_mediana_min <- survdiff(Surv(dias_min, Censored) ~ GrupoMedianaMin, data = datos_grupos)
surv_diff_mediana_min

surv_diff_mediana <- survdiff(Surv(dias_media, Censored) ~ GrupoMedianaMed, data = datos_grupos)
surv_diff_mediana

surv_diff_mediana_max <- survdiff(Surv(dias_max, Censored) ~ GrupoMedianaMax, data = datos_grupos)
surv_diff_mediana_max

#Vamos a hacerlo ahora con los cuantiles
surv_cuantiles_min <- survfit(Surv(dias_min, Censored) ~ GrupoCuantilesMin, data=datos_grupos)
a1 <- ggsurvplot(surv_cuantiles_min,
                palette = "Dark2",
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "A)",
                legend.labs=c("Datos menor o igual a 3","Datos mayores a 3 y menores o iguales a 10","Datos mayores que 10 y menores o iguales a 34","Datos mayores a 34"))+
  labs(x="Dias",y="S(t)")
surv_cuantiles <- survfit(Surv(dias_media, Censored) ~ GrupoCuantilesMed, data=datos_grupos)
b1 <- ggsurvplot(surv_cuantiles,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "B)",
                 legend.labs=c("Datos menor o igual a 4","Datos mayores a 4 y menores o iguales a 12","Datos mayores que 12 y menores o iguales a 38","Datos mayores a 38"))+
  labs(x="Dias",y="S(t)")
surv_cuantiles_max <- survfit(Surv(dias_max, Censored) ~ GrupoCuantilesMax, data=datos_grupos)
c1 <- ggsurvplot(surv_cuantiles_max,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "C)",
                 legend.labs=c("Datos menor o igual a 4","Datos mayores a 4 y menores o iguales a 12","Datos mayores que 12 y menores o iguales a 40","Datos mayores a 40"))+
  labs(x="Dias",y="S(t)")

#Vamos a hacer los test log-rank
surv_diff_cuantiles_min <- survdiff(Surv(dias_min, Censored) ~ GrupoCuantilesMin, data = datos_grupos)
surv_diff_cuantiles <- survdiff(Surv(dias_media, Censored) ~ GrupoCuantilesMed, data = datos_grupos)
surv_diff_cuantiles_max <- survdiff(Surv(dias_max, Censored) ~ GrupoCuantilesMax, data = datos_grupos)
surv_diff_cuantiles_min
surv_diff_cuantiles
surv_diff_cuantiles_max






#Ahora vamos a hacer los mismo analisisi, pero con las citaciones relativizadas
surv_mediana_min_rel<-survfit(Surv(dias_min, Censored) ~ GrupoMedianaMinRel, data=datos_grupos)
a2 <- ggsurvplot(surv_mediana_min_rel,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "A)",
                legend.labs=c("Datos menor o igual a 0.0063","Datos mayores a 0.0063"))+
  labs(x="Dias",y="S(t)")
surv_mediana_rel <- survfit(Surv(dias_media, Censored) ~ GrupoMedianaMedRel, data=datos_grupos)
b2 <- ggsurvplot(surv_mediana_rel,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "B)",
                legend.labs=c("Datos menor o igual a 0.0062","Datos mayores a 0.0062"))+
  labs(x="Dias",y="S(t)")
surv_mediana_max_rel <- survfit(Surv(dias_max, Censored) ~ GrupoMedianaMaxRel, data=datos_grupos)
c2 <- ggsurvplot(surv_mediana_max_rel,
                palette = c("skyblue4","chocolate3"),
                conf.int = TRUE,
                censor =TRUE,
                legend = "right",
                legend.title = "Set de datos",
                ggtheme = theme_gray(),
                title = "C)",
                legend.labs=c("Datos menor o igual a 0.0059","Datos mayores a 0.0059"))+
  labs(x="Dias",y="S(t)")

#Los test log-rank para saber si son diferentes las curvas de las medianas
surv_diff_mediana_min_rel <- survdiff(Surv(dias_min, Censored) ~ GrupoMedianaMinRel, data = datos_grupos)
surv_diff_mediana_min_rel

surv_diff_mediana_rel <- survdiff(Surv(dias_media, Censored) ~ GrupoMedianaMedRel, data = datos_grupos)
surv_diff_mediana_rel

surv_diff_mediana_max_rel <- survdiff(Surv(dias_max, Censored) ~ GrupoMedianaMaxRel, data = datos_grupos)
surv_diff_mediana_max_rel

#Vamos a hacerlo ahora con los cuantiles
surv_cuantiles_min_rel <- survfit(Surv(dias_min, Censored) ~ GrupoCuantilesMinRel, data=datos_grupos)
a3 <- ggsurvplot(surv_cuantiles_min_rel,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "A)",
                 legend.labs=c("Datos menor o igual a 0.002","Datos mayores a 0.002 y menores o iguales a 0.006","Datos mayores que 0.006 y menores o iguales a 0.015","Datos mayores a 0.015"))+
  labs(x="Dias",y="S(t)")
surv_cuantiles_rel <- survfit(Surv(dias_media, Censored) ~ GrupoCuantilesMedRel, data=datos_grupos)
b3 <- ggsurvplot(surv_cuantiles_rel,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "B)",
                 legend.labs=c("Datos menor o igual a 0.002","Datos mayores a 0.002 y menores o iguales a 0.006","Datos mayores que 0.006 y menores o iguales a 0.015","Datos mayores a 0.015"))+
  labs(x="Dias",y="S(t)")
surv_cuantiles_max_rel <- survfit(Surv(dias_max, Censored) ~ GrupoCuantilesMaxRel, data=datos_grupos)
c3 <- ggsurvplot(surv_cuantiles_max_rel,
                 palette = "Dark2",
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "C)",
                 legend.labs=c("Datos menor o igual a 0.002","Datos mayores a 0.002 y menores o iguales a 0.005","Datos mayores que 0.005 y menores o iguales a 0.015","Datos mayores a 0.015"))+
  labs(x="Dias",y="S(t)")

#Vamos a hacer los test log-rank
surv_diff_cuantiles_min_rel <- survdiff(Surv(dias_min, Censored) ~ GrupoCuantilesMinRel, data = datos_grupos)
surv_diff_cuantiles_rel <- survdiff(Surv(dias_media, Censored) ~ GrupoCuantilesMedRel, data = datos_grupos)
surv_diff_cuantiles_max_rel <- survdiff(Surv(dias_max, Censored) ~ GrupoCuantilesMaxRel, data = datos_grupos)
surv_diff_cuantiles_min_rel
surv_diff_cuantiles_rel
surv_diff_cuantiles_max_rel

#Vamos a haer el analisis del 75% de las citaciones relativizadas

surv_mediana_min_rel_75 <- survfit(Surv(dias_max, Censored) ~ GrupoMedianaMinRel75, data=datos_grupos)
a4 <- ggsurvplot(surv_mediana_min_rel_75,
                 palette = c("skyblue4","chocolate3"),
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "A)",
                 legend.labs=c("Datos menor o igual a 0.0157","Datos mayores a 0.0157"))+
  labs(x="Dias",y="S(t)")

surv_mediana_med_rel_75 <- survfit(Surv(dias_max, Censored) ~ GrupoMedianaMedRel75, data=datos_grupos)
b4 <- ggsurvplot(surv_mediana_med_rel_75,
                 palette = c("skyblue4","chocolate3"),
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "B)",
                 legend.labs=c("Datos menor o igual a 0.0157","Datos mayores a 0.0157"))+
  labs(x="Dias",y="S(t)")

surv_mediana_max_rel_75 <- survfit(Surv(dias_max, Censored) ~ GrupoMedianaMaxRel75, data=datos_grupos)
c4 <- ggsurvplot(surv_mediana_max_rel_75,
                 palette = c("skyblue4","chocolate3"),
                 conf.int = TRUE,
                 censor =TRUE,
                 legend = "right",
                 legend.title = "Set de datos",
                 ggtheme = theme_gray(),
                 title = "C)",
                 legend.labs=c("Datos menor o igual a 0.0152","Datos mayores a 0.0152"))+
  labs(x="Dias",y="S(t)")

#Vamos a hacer los test log-rank
surv_diff_mediana_min_rel_75 <- survdiff(Surv(dias_min, Censored) ~ GrupoMedianaMinRel75, data = datos_grupos)
surv_diff_mediana_rel_75 <- survdiff(Surv(dias_media, Censored) ~ GrupoMedianaMedRel75, data = datos_grupos)
surv_diff_mediana_max_rel_75 <- survdiff(Surv(dias_max, Censored) ~ GrupoMedianaMaxRel75, data = datos_grupos)
surv_diff_mediana_min_rel_75
surv_diff_mediana_rel_75
surv_diff_mediana_max_rel_75