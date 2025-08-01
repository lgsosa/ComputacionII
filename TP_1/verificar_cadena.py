import json
import hashlib

def calcular_hash(prev_hash, datos, timestamp):
    texto = prev_hash + json.dumps(datos, sort_keys=True) + timestamp
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

def verificar_cadena(archivo_json, archivo_reporte):
    with open(archivo_json, 'r') as f:
        blockchain = json.load(f)

    bloques_totales = len(blockchain)
    bloques_alerta = 0
    errores = []

    suma_frecuencia = 0
    suma_presion = 0
    suma_oxigeno = 0

    for i, bloque in enumerate(blockchain):
        prev_hash = bloque['hash_previo']
        datos = bloque['datos']
        timestamp = bloque['timestamp']
        hash_almacenado = bloque['hash']

        # Recalcular hash
        hash_recalculado = calcular_hash(prev_hash, datos, timestamp)

        # Verificar que el hash coincida
        if hash_recalculado != hash_almacenado:
            errores.append(f"Bloque {i}: Hash incorrecto.")

        # Verificar encadenamiento (excepto primer bloque)
        if i > 0:
            hash_prev_esperado = blockchain[i-1]['hash']
            if prev_hash != hash_prev_esperado:
                errores.append(f"Bloque {i}: hash_previo no coincide con hash del bloque anterior.")

        if bloque['alerta']:
            bloques_alerta += 1

        suma_frecuencia += datos['frecuencia']['media']
        suma_presion += datos['presion']['media']
        suma_oxigeno += datos['oxigeno']['media']

    promedio_frecuencia = suma_frecuencia / bloques_totales if bloques_totales > 0 else 0
    promedio_presion = suma_presion / bloques_totales if bloques_totales > 0 else 0
    promedio_oxigeno = suma_oxigeno / bloques_totales if bloques_totales > 0 else 0

    with open(archivo_reporte, 'w') as f:
        f.write(f"Cantidad total de bloques: {bloques_totales}\n")
        f.write(f"Número de bloques con alertas: {bloques_alerta}\n")
        f.write(f"Promedio general de frecuencia: {promedio_frecuencia:.2f}\n")
        f.write(f"Promedio general de presión: {promedio_presion:.2f}\n")
        f.write(f"Promedio general de oxígeno: {promedio_oxigeno:.2f}\n\n")

        if errores:
            f.write("Bloques corruptos detectados:\n")
            for e in errores:
                f.write(e + "\n")
        else:
            f.write("No se detectaron bloques corruptos.\n")

    print("Verificación completada. Revisa reporte.txt")

if __name__ == "__main__":
    verificar_cadena("blockchain.json", "reporte.txt")
