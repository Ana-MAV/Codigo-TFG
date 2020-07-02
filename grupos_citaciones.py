#Separamos en grupos, por una parte vamos a hacer los cuantiles y por otra vamos a hacer los cuantiles

import pandas as pd

datos = pd.read_csv("datos_citaciones_antes_de_muerte.csv")


#datos = datos.drop(columns=["GrupoCitaciones"])

#Separamos por la mediana
grupo_mediana_min = []
grupo_mediana_med = []
grupo_mediana_max = []
grupo_mediana_min_rel = []
grupo_mediana_med_rel = []
grupo_mediana_max_rel = []
grupo_mediana_min_rel_75 = []
grupo_mediana_med_rel_75 = []
grupo_mediana_max_rel_75 = []

for i in range(0,len(datos.index)): #A es menor que la mdiana y B es mayor a la mediana
	row = datos.iloc[i]
	#print(type(row["NumCitaciones"]))
	if int(row["CitMin"]) <= 10:
		grupo_mediana_min.append("A")
	else:
		grupo_mediana_min.append("B")
	if int(row["CitMed"]) <= 12:
		grupo_mediana_med.append("A")
	else:
		grupo_mediana_med.append("B")
	if int(row["CitMax"]) <= 12:
		grupo_mediana_max.append("A")
	else:
		grupo_mediana_max.append("B")

	if row["CitMinRel"] <= 0.006349206349206349:
		grupo_mediana_min_rel.append("A")
	else:
		grupo_mediana_min_rel.append("B")
	if row["CitMedRel"] <= 0.006253908692933083:
		grupo_mediana_med_rel.append("A")
	else:
		grupo_mediana_med_rel.append("B")
	if row["CitMaxRel"] <= 0.005967922417008579:
		grupo_mediana_max_rel.append("A")
	else:
		grupo_mediana_max_rel.append("B")

	if row["CitMinRel"] <= 0.015781922525107604:
		grupo_mediana_min_rel_75.append("A")
	else:
		grupo_mediana_min_rel_75.append("B")
	if row["CitMedRel"] <= 0.015734265734265736:
		grupo_mediana_med_rel_75.append("A")
	else:
		grupo_mediana_med_rel_75.append("B")
	if row["CitMaxRel"] <= 0.015219842164599776:
		grupo_mediana_max_rel_75.append("A")
	else:
		grupo_mediana_max_rel_75.append("B")
datos["GrupoMedianaMin"] = grupo_mediana_min
datos["GrupoMedianaMed"] = grupo_mediana_med
datos["GrupoMedianaMax"] = grupo_mediana_max

datos["GrupoMedianaMinRel"] = grupo_mediana_min_rel
datos["GrupoMedianaMedRel"] = grupo_mediana_med_rel
datos["GrupoMedianaMaxRel"] = grupo_mediana_max_rel

datos["GrupoMedianaMinRel75"] = grupo_mediana_min_rel_75
datos["GrupoMedianaMedRel75"] = grupo_mediana_med_rel_75
datos["GrupoMedianaMaxRel75"] = grupo_mediana_max_rel_75
#Separamos por cuantiles


grupo_cuantiles_min = []
grupo_cuantiles_med = []
grupo_cuantiles_max = []
grupo_cuantiles_min_rel = []
grupo_cuantiles_med_rel = []
grupo_cuantiles_max_rel = []
for j in range(0,len(datos.index)):
	row = datos.iloc[j]
	
	if row["CitMinRel"] <= 0.002237970906378217:
		grupo_cuantiles_min_rel.append("A")
	elif row["CitMinRel"] > 0.002237970906378217 and row["CitMinRel"] <= 0.006349206349206349:
		grupo_cuantiles_min_rel.append("B")
	elif row["CitMinRel"] > 0.006349206349206349 and row["CitMinRel"] <= 0.015781922525107604:
		grupo_cuantiles_min_rel.append("C")
	else:
		grupo_cuantiles_min_rel.append("D")

	if row["CitMedRel"] <= 0.0022449488650536295:
		grupo_cuantiles_med_rel.append("A")
	elif row["CitMedRel"] > 0.0022449488650536295 and row["CitMedRel"] <= 0.006253908692933083:
		grupo_cuantiles_med_rel.append("B")
	elif row["CitMedRel"] > 0.006253908692933083 and row["CitMedRel"] <= 0.015734265734265736:
		grupo_cuantiles_med_rel.append("C")
	else:
		grupo_cuantiles_med_rel.append("D")
	
	if row["CitMaxRel"] <= 0.002129471890971039:
		grupo_cuantiles_max_rel.append("A")
	elif row["CitMaxRel"] > 0.002129471890971039 and row["CitMaxRel"] <= 0.005967922417008579:
		grupo_cuantiles_max_rel.append("B")
	elif row["CitMaxRel"] > 0.005967922417008579 and row["CitMaxRel"] <= 0.015219842164599776:
		grupo_cuantiles_max_rel.append("C")
	else:
		grupo_cuantiles_max_rel.append("D")

	
	if int(row["CitMin"]) <= 3:
		grupo_cuantiles_min.append("A")
	elif int(row["CitMin"]) > 3 and int(row["CitMin"]) <= 10:
		grupo_cuantiles_min.append("B")
	elif int(row["CitMin"]) > 10 and int(row["CitMin"]) <= 34:
		grupo_cuantiles_min.append("C")
	else:
		grupo_cuantiles_min.append("D")

	if int(row["CitMed"]) <= 4:
		grupo_cuantiles_med.append("A")
	elif int(row["CitMed"]) > 4 and int(row["CitMed"]) <= 12:
		grupo_cuantiles_med.append("B")
	elif int(row["CitMed"]) > 12 and int(row["CitMed"]) <= 38:
		grupo_cuantiles_med.append("C")
	else:
		grupo_cuantiles_med.append("D")

	if int(row["CitMax"]) <= 4:
		grupo_cuantiles_max.append("A")
	elif int(row["CitMax"]) > 4 and int(row["CitMax"]) <= 12:
		grupo_cuantiles_max.append("B")
	elif int(row["CitMax"]) > 12 and int(row["CitMax"]) <= 40:
		grupo_cuantiles_max.append("C")
	else:
		grupo_cuantiles_max.append("D")
datos["GrupoCuantilesMin"] = grupo_cuantiles_min
datos["GrupoCuantilesMed"] = grupo_cuantiles_med
datos["GrupoCuantilesMax"] = grupo_cuantiles_max
datos["GrupoCuantilesMinRel"] = grupo_cuantiles_min_rel
datos["GrupoCuantilesMedRel"] = grupo_cuantiles_med_rel
datos["GrupoCuantilesMaxRel"] = grupo_cuantiles_max_rel
datos.to_csv("datos_bio+nar_citaciones_antesdemorir.csv",index=False)