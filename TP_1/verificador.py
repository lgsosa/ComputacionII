import json
import hashlib
import csv

def calcular_hash(prev_hash, datos, timestamp):
    texto = prev_hash + json.dumps(datos, sort_keys=True) + timestamp
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

def verificador(queue_a, queue_b, queue_c):
    fin = set()
    colas = {
        'frecuencia': queue_a,
        'presion': queue_b,
        'oxigeno': queue_c
    }

    resultados_pendientes = {}
    blockchain = []
    archivo_blockchain = "blockchain.json"

    csv_files = {}
    csv_writers = {}
    for nombre in colas.keys():
        f = open(f"{nombre}.csv", "w", newline='')
        csv_files[nombre] = f
        csv_writers[nombre] = csv.writer(f)
        csv_writers[nombre].writerow(["tipo", "timestamp", "media", "desv"])

    while len(fin) < 3:
        for nombre, cola in colas.items():
            if nombre in fin:
                continue
            try:
                resultado = cola.get(timeout=1)
                if resultado is None:
                    fin.add(nombre)
                    print(f"[Verificador] {nombre} terminó.")
                    continue

                ts = resultado['timestamp']
                if ts not in resultados_pendientes:
                    resultados_pendientes[ts] = {}
                resultados_pendientes[ts][nombre] = resultado

                if len(resultados_pendientes[ts]) == 3:
                    datos = {
                        'frecuencia': {
                            'media': resultados_pendientes[ts]['frecuencia']['media'],
                            'desv': resultados_pendientes[ts]['frecuencia']['desv']
                        },
                        'presion': {
                            'media': resultados_pendientes[ts]['presion']['media'],
                            'desv': resultados_pendientes[ts]['presion']['desv']
                        },
                        'oxigeno': {
                            'media': resultados_pendientes[ts]['oxigeno']['media'],
                            'desv': resultados_pendientes[ts]['oxigeno']['desv']
                        }
                    }

                    alerta = False
                    if datos['frecuencia']['media'] >= 200:
                        alerta = True
                    if not (90 <= datos['oxigeno']['media'] <= 100):
                        alerta = True
                    if datos['presion']['media'] >= 200:
                        alerta = True

                    prev_hash = blockchain[-1]['hash'] if blockchain else '0' * 64
                    bloque = {
                        'indice': len(blockchain),
                        'timestamp': ts,
                        'datos': datos,
                        'alerta': alerta,
                        'hash_previo': prev_hash,
                        'hash': ''
                    }

                    bloque['hash'] = calcular_hash(bloque['hash_previo'], bloque['datos'], bloque['timestamp'])
                    blockchain.append(bloque)

                    with open(archivo_blockchain, 'w') as f:
                        json.dump(blockchain, f, indent=4)

                    print(f"[Bloque {bloque['indice']}] {ts} Hash: {bloque['hash']} Alerta: {bloque['alerta']}")

                    for nombre_signal, writer in csv_writers.items():
                        r = resultados_pendientes[ts][nombre_signal]
                        writer.writerow([r['tipo'], r['timestamp'], f"{r['media']:.2f}", f"{r['desv']:.2f}"])

                    del resultados_pendientes[ts]

            except Exception:
                continue

    for f in csv_files.values():
        f.close()

    print("Verificador terminó.")
