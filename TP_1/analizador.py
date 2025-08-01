import statistics
import time

def analizador(pipe_conn, cola_resultados, tipo):
    ventana = []  # ventana móvil de los últimos 30 datos

    while True:
        if pipe_conn.poll(1):
            dato = pipe_conn.recv()
            if dato is None:
                print(f"Analizador {tipo} terminó correctamente.")
                break

            if tipo == 'frecuencia':
                valor = dato['frecuencia']
            elif tipo == 'presion':
                valor = dato['presion'][0]  # presion sistolica
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

            # Enviar resultado al verificador
            cola_resultados.put(resultado)
        else:
            time.sleep(0.1)
