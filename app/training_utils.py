import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://www.tdea.edu.co/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

facultades = []

## Estructurar datos extraidos del TdeA
for link_facultad in soup.find_all('a', class_='uk-position-cover'):
    if re.search('facultad', link_facultad.get('href', '')):
        facultad = {'nombre': link_facultad['href'].split('/')[-1].replace('-', ' ').title(), 'carreras': []}
        href_facultad = link_facultad['href']
        response_facultad = requests.get(href_facultad)
        soup_facultad = BeautifulSoup(response_facultad.content, 'html.parser')
        for link_carrera in soup_facultad.find_all('a', class_='elementor-post__thumbnail__link'):
            carrera = {'carrera': link_carrera['href'].split('/')[-1].replace('-', ' ').title(), 'plan de estudio': [], 'precios': ""}
            href_carrera = link_carrera['href']
            response_carrera = requests.get(href_carrera)
            soup_carrera = BeautifulSoup(response_carrera.content, 'html.parser')
            valores = soup_carrera.find_all('h2', class_='elementor-heading-title elementor-size-default')
            if len(valores) > 0:
              for valor in valores:
                value = valor and valor.text.rfind('SMMLV')
                if value != -1:
                  cadena_formateada = valor.text.strip().replace('\n', ' ')
                  cadena_formateada = cadena_formateada.replace(':', '')
                  carrera['precios'] = cadena_formateada
            semestres = []
            print(carrera)
            for semestre in soup_carrera.find_all('div', class_='elementor-price-table'):
              materias = []
              div_materias = semestre.find_all('div', class_='elementor-price-table__feature-inner')
              if div_materias is not None:
                  for materia in div_materias:
                      if materia.find('span') is not None and materia.find('span').text:
                        materias.append(materia.find('span').text.strip())
              carrera['plan de estudio'].append({'semestre': semestre.find(class_='elementor-price-table__heading').text.strip(), 'materias': materias})
            facultad['carreras'].append(carrera)

        facultades.append(facultad)

## Generar datos en csv
with open('datos_tdea.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Escribir la cabecera
    writer.writerow(['Facultad', 'Carrera', 'Precio', 'Semestre', 'Materias'])
    
    # Escribir cada fila con los datos
    for facultad in facultades:
        nombre_facultad = facultad['nombre']
        for carrera in facultad['carreras']:
            nombre_carrera = carrera['carrera']
            precio = carrera['precios']
            for semestre in carrera['plan de estudio']:
                nombre_semestre = semestre['semestre']
                materias = ';'.join(semestre['materias'])
                writer.writerow([nombre_facultad, nombre_carrera, precio, nombre_semestre, materias])
