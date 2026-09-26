import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Autores: Francisco Vecchione y Walter ariel Paz Estrada

#URL del repositorio público de Github
#REPOSITORIO_GITHUB = https://github.com/Vecchio51/Laboratorio-IV_2

#PRIMERO: Cargar el archivo CSV con pandas
#Se interpreta 'timestamp' como fecha/hora y se asigna como índice del DataFrame


archivo_csv = 'telemetria_nodo_iot.csv'
try:
    df = pd.read_csv(archivo_csv, parse_dates=['timestamp'], index_col='timestamp')
except FileNotFoundError:
    print("Error...")

#analis estadistico

estadisticas = df.describe().loc[['mean', 'min', 'max', 'std']]}

#realizamos una deteccion de fallos con arreglos

voltaje = df['voltaje bateria V'].to_numpy()
rssi = df['rssi dbm'].to_numpy()

alerta_bateria = voltaje < 3.5
alerta_senal = rssi < -85
alerta_general = alerta_bateria | alerta_senal

df['alerta_activa'] = alerta_general




