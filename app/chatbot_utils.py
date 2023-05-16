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


# Posibles respuestas
respuestas_saludos = ["¡Hola! ¿En qué puedo ayudarte?",
                  "¡Hola! ¿En qué puedo ayudarte hoy?",
                  "Hola, ¿cómo puedo ayudarte?"]
                  
respuestas_despedidas = ["¡Fue un placer ayudarte!",
                  "¡Hasta luego!",
                  "¡Que tengas un buen día!"]

respuestas_facultad = ["Las facultades disponibles en la universidad son", 
                       "En la universidad ofrecemos las siguientes facultades",
                       "Las facultades inscritas actualmente en la universidad son",
                       "Nuestra universidad ofrece diversas facultades, entre ellas",
                       "Puedes encontrar una amplia variedad de facultades en nuestra universidad, tales como",
                       "Contamos con varias facultades que podrían interesarte, como por ejemplo",
                       "Si buscas estudiar en una de las mejores universidades del país, nuestras facultades incluyen",
                       "En nuestra universidad, las opciones de facultades disponibles para ti son",
                       "Te ofrecemos una amplia variedad de facultades para que elijas la que mejor se adapte a tus intereses, tales como",
                       "Nuestro catálogo de facultades incluye",
                       "Las facultades más populares de nuestra universidad son",
                       "Entre nuestras facultades más destacadas se encuentran",
                       "Si te interesa alguna de estas áreas de estudio, tenemos las siguientes facultades",
                       "No importa tu área de interés, en nuestra universidad seguro encontrarás una facultad que se adapte a ti, como por ejemplo"]

respuestas_carreras = ["Las carreras disponibles son", 
                          "Te puedes encontrar con las siguientes carreras",
                          "Los programas que se ofertan son"]

# Funciones de procesamiento de texto
def limpiar_texto(texto):
    tokens = nltk.word_tokenize(texto)
    tokens = [token.lower() for token in tokens if token.isalpha()]
    return tokens

  
def encontrar_dato(tokens, datos):
    # Convertir tokens a un conjunto para buscar de manera eficiente
    token_set = set(tokens)

    # Contador para contar la cantidad de apariciones de tokens en cada dato
    apariciones = {}

    for dato in datos:
        # Convertir el dato en un conjunto de palabras
        dato_set = set(dato.lower().split())

        # Calcular la cantidad de palabras en común entre los tokens y el dato
        n_coincidencias = len(token_set & dato_set)

        # Agregar las coincidencias al contador
        apariciones[dato] = n_coincidencias

    # Ordenar los datos por cantidad de coincidencias, de mayor a menor
    datos_ordenados = sorted(datos, key=lambda x: apariciones[x], reverse=True)

    # Si hay un solo dato con la máxima cantidad de coincidencias, devolverlo
    if apariciones[datos_ordenados[0]] > 0 and apariciones[datos_ordenados[0]] >= apariciones[datos_ordenados[1]]:
        return datos_ordenados[0]
    else:
        return None
  
def quitar_tildes(frase):
    return ''.join((c for c in unicodedata.normalize('NFD', frase) if unicodedata.category(c) != 'Mn'))
