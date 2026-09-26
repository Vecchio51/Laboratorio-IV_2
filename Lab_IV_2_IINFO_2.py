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

#Calcular estadísticas descriptivas con pandas y numpy
print("--- Estadísticas Descriptivas ---")
estadisticas = df.describe().loc[['mean', 'min', 'max', 'std']]
print(estadisticas)
print("\n")

#Definir criterio de alerta con arrays de numpy e indexado booleano
#Extraemos las columnas a arrays de numpy
voltaje = df['voltaje bateria V'].to_numpy()
rssi = df['rssi dbm'].to_numpy()

#Definimos las condiciones de alerta
alerta_bateria = voltaje < 3.5
alerta_senal = rssi < -85

#Definimos al menos una alerta (operador OR bit a bit para arrays booleanos)
alerta_general = alerta_bateria | alerta_senal

print("--- Resumen de Alertas ---")
print(f"Registros con batería baja (< 3.5V): {np.sum(alerta_bateria)}")
print(f"Registros con señal débil (< -85 dBm): {np.sum(alerta_senal)}")
print(f"Total de registros con al menos una alerta: {np.sum(alerta_general)}")
print("\n")

#Añadimos la columna de alerta general al DataFrame para usarla en el agrupamiento
df['alerta_activa'] = alerta_general




