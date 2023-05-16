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

## Procesar datos claves iniciales
def quitar_tildes(frase):
    return ''.join((c for c in unicodedata.normalize('NFD', frase) if unicodedata.category(c) != 'Mn'))

def procesar_datos_claves(num):
    return [quitar_tildes(palabra.strip().lower()) for palabra in lineas[num].split(',')]

# Leer los arrays desde el archivo de texto
with open('datos_claves.txt', 'r') as archivo:
    lineas = archivo.readlines()
    palabras_clave_saludos = procesar_datos_claves(0)
    palabras_clave_facultades = procesar_datos_claves(1)
    palabras_clave_carreras = procesar_datos_claves(2)
    palabras_clave_precios = procesar_datos_claves(3)
    palabras_clave_semestre = procesar_datos_claves(4)
    palabras_clave_materias = procesar_datos_claves(5)
    palabras_clave_ayuda = procesar_datos_claves(6)
    palabras_clave_despedidas = procesar_datos_claves(7)
    palabras_clave_unidades = procesar_datos_claves(8)


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

# Generar respuesta aleatoria
def generar_respuesta(palabrasRandom, listaDatos = None):
  if listaDatos is not None:
    return random.choice(palabrasRandom) + ": " + "; ".join(listaDatos)
  return random.choice(palabrasRandom)

# Funciones de respuesta del chatbot
def responder_saludo():
    return generar_respuesta(respuestas_saludos)

def responder_facultades(unidades = False):
    respuesta = generar_respuesta(respuestas_facultad, facultades)
    if unidades:
      respuesta = "En total son " + str(len(facultades)) + " facultades. " + respuesta
    return respuesta

def responder_carreras(facultad, unidades = False):
    respuesta = ""
    carreras_facultad = data[data["Facultad"].str.lower() == facultad]["Carrera"].unique()
    if len(carreras_facultad) > 0:
      if unidades:
        respuesta = "En total son " + str(len(carreras_facultad)) + " carerras. " + generar_respuesta(respuestas_carreras, carreras_facultad)
      else:
        respuesta = generar_respuesta(respuestas_carreras, carreras_facultad)
    else:
        respuesta = "Lo siento. No se encontraron carreras para la " + facultad
    return respuesta

def responder_todas_carreras(unidades = False):
    respuesta = generar_respuesta(respuestas_carreras, carreras)
    if unidades:
      respuesta = "En total son " + str(len(carreras)) + " carerras. " + respuesta
    return respuesta

def responder_precios(carrera):
    precio_carrera = data[data["Carrera"].str.lower() == carrera]["Precio"].values[0]
    respuesta = "Los precios de " + carrera + " son " + str(precio_carrera)
    return respuesta

def responder_semestres(carrera):
    semestre_carrera = data[data["Carrera"].str.lower() == carrera]["Semestre"]
    respuesta = "La duración de " + carrera + " es de " + str(len(semestre_carrera)) + " semestres."
    return respuesta

def responder_materias(carrera, texto):
    materias_carrera = data[data["Carrera"].str.lower() == carrera]["Materias"]
    if len(materias_carrera) == 0:
        respuesta = "No encontré ninguna materia que coincida con tu consulta."
    else:
        respuesta = "Las materias que encontré son: " + ", ".join(materias_carrera) + ". Si quieres mas información acercate al TdeA"
    return respuesta

def responder_ayuda():
    respuesta = "Puedo ayudarte con información sobre las facultades, carreras, precios, semestres y materias de la universidad. Solo pregúntame lo que necesites."
    return respuesta

def responder_despedida():
    return generar_respuesta(respuestas_despedidas)

# def corregir_texto(texto):
#     # Creamos una instancia de LanguageTool para el idioma español
#     tool = language_tool_python.LanguageTool('es')

#     # Verificamos la gramática y ortografía del texto
#     correcciones = tool.correct(texto)

#     # Retornamos el texto corregido
#     return correcciones

# Función principal del chatbot
def chatbot_cognitivo(texto):
    respuesta = "Discúlpame, pero no entendí a que te refieres."
    # texto_correc = corregir_texto(texto)
    texto = quitar_tildes(texto).lower()
    tokens = limpiar_texto(texto)
    # Saludos
    if any(palabra in tokens for palabra in palabras_clave_saludos):
        respuesta = responder_saludo()
    
    # Facultades
    elif any(palabra in tokens for palabra in palabras_clave_facultades):
      if any(palabra in tokens for palabra in palabras_clave_unidades):
        respuesta = responder_facultades(True)
      else:
        respuesta = responder_facultades()
    
    # Carreras
    elif any(palabra in tokens for palabra in palabras_clave_carreras):
        facultad = encontrar_dato(tokens, facultades)
        if facultad:
          if any(palabra in tokens for palabra in palabras_clave_unidades):
            respuesta = responder_carreras(facultad, True)
          else:
            respuesta = responder_carreras(facultad)
        else:
          if any(palabra in tokens for palabra in palabras_clave_unidades):
            respuesta = responder_todas_carreras(True)
          else:
            respuesta = responder_todas_carreras()

    # Precios
    elif any(palabra in tokens for palabra in palabras_clave_precios):
        carrera = encontrar_dato(tokens, carreras)

        if carrera:
            respuesta = responder_precios(carrera)
        else:
            respuesta = "No entendí a qué carrera te refieres. ¿Podrías ser más específico?"
    
    # Semestre
    elif any(palabra in tokens for palabra in palabras_clave_semestre):
        carrera = encontrar_dato(tokens, carreras)

        if carrera:
            respuesta = responder_semestres(carrera)
        else:
            respuesta = "No entendí a qué carrera te refieres. ¿Podrías ser más específico?"

    # Materias
    elif any(palabra in tokens for palabra in palabras_clave_materias):
        carrera = encontrar_dato(tokens, carreras)
        if carrera:
            respuesta = responder_materias(carrera, texto)
        else:
            respuesta = "No entendí a qué carrera te refieres. ¿Podrías ser más específico?"
    
    # Ayuda
    elif any(palabra in tokens for palabra in palabras_clave_ayuda):
        respuesta = responder_ayuda()
    
    # Despedidas
    elif any(palabra in tokens for palabra in palabras_clave_despedidas):
        respuesta = responder_despedida()
        
    return respuesta

