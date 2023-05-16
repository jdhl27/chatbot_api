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

# Leer los arrays desde el archivo de texto
with open('datos_claves.txt', 'r') as archivo:
    lineas = archivo.readlines()
    palabras_clave_saludos = lineas[0].strip().split(',')
    palabras_clave_facultades = lineas[1].strip().split(',')
    palabras_clave_carreras = lineas[2].strip().split(',')
    palabras_clave_precios = lineas[3].strip().split(',')
    palabras_clave_semestre = lineas[4].strip().split(',')
    palabras_clave_materias = lineas[5].strip().split(',')
    palabras_clave_ayuda = lineas[6].strip().split(',')
    palabras_clave_despedidas = lineas[7].strip().split(',')
    palabras_clave_unidades = lineas[8].strip().split(',')
