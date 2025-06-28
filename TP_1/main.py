import time
from datetime import datetime
from multiprocessing import Process, Pipe, Queue
from TP_1.analizador import analizador
from TP_1.verificador import verificador
from random import randint

def generar_dato():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "frecuencia": randint(60, 180),
        "presion": [randint(110, 180), randint(70, 110)],
        "oxigeno": randint(90, 100)
    }

def main():
    # Crear pipes para enviar datos completos a analizadores
    parent_a, child_a = Pipe()
    parent_b, child_b = Pipe()
    parent_c, child_c = Pipe()

    # Crear colas para recibir resultados de analizadores
    queue_a = Queue()
    queue_b = Queue()
    queue_c = Queue()

    # Crear procesos analizador
    p_a = Process(target=analizador, args=(child_a, queue_a, 'frecuencia'))
    p_b = Process(target=analizador, args=(child_b, queue_b, 'presion'))
    p_c = Process(target=analizador, args=(child_c, queue_c, 'oxigeno'))

    # Crear proceso verificador (solo muestra resultados)
    p_ver = Process(target=verificador, args=(queue_a, queue_b, queue_c))

    # Iniciar procesos
    p_a.start()
    p_b.start()
    p_c.start()
    p_ver.start()

    # Enviar 60 datos, 1 por segundo
    for _ in range(60):
        dato = generar_dato()
        parent_a.send(dato)
        parent_b.send(dato)
        parent_c.send(dato)
        time.sleep(1)

    # Enviar señal de fin
    parent_a.send(None)
    parent_b.send(None)
    parent_c.send(None)

    # Esperar que terminen analizadores
    p_a.join()
    p_b.join()
    p_c.join()

    print("Analizadores finalizados.")
    # Enviar señal de fin a verificador
    queue_a.put(None)
    queue_b.put(None)
    queue_c.put(None)

    # Esperar que termine verificador
    p_ver.join()

    print("Proceso verificador finalizado.")
    print("Programa principal terminó.")

if __name__ == "__main__":
    main()
