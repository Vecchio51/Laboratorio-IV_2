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
    df = pd.read_csv(
        archivo_csv,
        parse_dates=['timestamp'],
        index_col='timestamp'
    )
except FileNotFoundError:
    print("Error: no se encontró el archivo CSV.")

#Calcular estadísticas descriptivas con pandas y numpy
print("--- Estadísticas Descriptivas ---")
estadisticas = df.describe().loc[['mean', 'min', 'max', 'std']]
print(estadisticas)
print("\n")

#Definir criterio de alerta con arrays de numpy e indexado booleano
#Extraemos las columnas a arrays de numpy
voltaje = df['voltaje_bateria_V'].to_numpy()
rssi = df['rssi_dbm'].to_numpy()

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

#Gráfico con ejes independientes y marcadores de alerta
fig, ax1 = plt.subplots(figsize=(12, 6))

#Eje Y izquierdo: Temperatura
ax1.plot(df.index, df['temperatura_C'], color='tab:red', label='Temperatura (°C)')
ax1.set_ylabel('Temperatura (°C)', color='tab:red')

#Eje Y derecho: Voltaje
ax2 = ax1.twinx()
ax2.plot(df.index, df['voltaje_bateria_V'], color='tab:blue', label='Voltaje batería (V)')
ax2.set_ylabel('Voltaje (V)', color='tab:blue')

#Dibujar las cruces en los momentos de alerta
alertas = df[df['alerta_activa']]
ax2.scatter(alertas.index, alertas['voltaje_bateria_V'], color='black', marker='X', s=50, label='Alerta Detectada')

plt.title('Evolución temporal de telemetría')
plt.show() #Instruccion para que el gráfico se renderice en pantalla

#Resumen diario
resumen_diario = df.resample('D').agg(
    temperatura_promedio=('temperatura_C', 'mean'),
    temperatura_maxima=('temperatura_C', 'max'),
    temperatura_minima=('temperatura_C', 'min'),
    voltaje_promedio=('voltaje_bateria_V', 'mean'),
    voltaje_minimo=('voltaje_bateria_V', 'min'),
    cantidad_alertas=('alerta_activa', 'sum')
)

print("--- Resumen diario ---")
print(resumen_diario)

#Exportación a archivo Excel
resumen_diario.to_excel('resumen_telemetria.xlsx', sheet_name='Resumen diario')
print("\nArchivo Excel generado con éxito.")

