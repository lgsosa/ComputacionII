import csv

def verificador(queue_a, queue_b, queue_c):
    fin = set()
    colas = {
        'frecuencia': queue_a,
        'presion': queue_b,
        'oxigeno': queue_c
    }

    archivos = {}
    escritores = {}
    for nombre in colas.keys():
        f = open(f"{nombre}.csv", "w", newline='')
        archivos[nombre] = f
        escritores[nombre] = csv.writer(f)
        escritores[nombre].writerow(["tipo", "timestamp", "media", "desv"])  # encabezado

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
                #  resultado en CSV
                escritores[nombre].writerow([
                    resultado['tipo'],
                    resultado['timestamp'],
                    f"{resultado['media']:.2f}",
                    f"{resultado['desv']:.2f}"
                ])
                print(f"[Verificador] {resultado['tipo']} - {resultado['timestamp']} | media={resultado['media']:.2f} desv={resultado['desv']:.2f}")
            except Exception:
                continue


    for f in archivos.values():
        f.close()

    print("Verificador terminó.")
