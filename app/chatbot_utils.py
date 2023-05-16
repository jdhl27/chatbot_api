import nltk
import pandas as pd
import random
import unicodedata

# import language_tool_python

# Datos para tokenizar
nltk.download('punkt')

# Carga del archivo CSV
data = pd.read_csv("datos_tdea.csv")

# Minuscula en todos los datos para el proceso exitoso
def procesar_datos_iniciales(string, value = False):
  if value:  
    return [elemento.lower() for elemento in list(set(";".join(data[string]).split(";")))]

  return [elemento.lower() for elemento in list(set(data[string]))]
  

# Preprocesamiento de los datos
facultades = procesar_datos_iniciales("Facultad")
carreras = procesar_datos_iniciales("Carrera")
precios = procesar_datos_iniciales("Precio")
semestres = procesar_datos_iniciales("Semestre")
materias = procesar_datos_iniciales("Materias", True)
