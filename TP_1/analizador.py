import statistics
import time
import os
import csv

def analizador(pipe_conn, cola_resultados, tipo):
    ventana = []  # ventana móvil de los últimos 30 datos
    nombre_archivo = f"{tipo}.csv"

    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "media", "desvio"])

    while True:
        if pipe_conn.poll(1):
            dato = pipe_conn.recv()
            if dato is None:
                print(f"Analizador {tipo} terminó correctamente.")
                break

            if tipo == 'frecuencia':
                valor = dato['frecuencia']
            elif tipo == 'presion':
                valor = dato['presion'][0]  # sistólica
            else:
                valor = dato['oxigeno']

            timestamp = dato['timestamp']
            ventana.append((timestamp, valor))

            if len(ventana) > 30:
                ventana.pop(0)

            valores = [v for _, v in ventana]
            media = statistics.mean(valores)
            desvio = statistics.stdev(valores) if len(valores) > 1 else 0.0

            resultado = {
                "tipo": tipo,
                "timestamp": timestamp,
                "media": media,
                "desv": desvio
            }

            # guardo en el archivo CSV
            with open(nombre_archivo, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, f"{media:.2f}", f"{desvio:.2f}"])

            # envio a la cola del verificador
            cola_resultados.put(resultado)
        else:
            time.sleep(0.1)
