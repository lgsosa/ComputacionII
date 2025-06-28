def verificador(queue_a, queue_b, queue_c):
    fin = set()
    colas = {
        'frecuencia': queue_a,
        'presion': queue_b,
        'oxigeno': queue_c
    }

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
                print(f"[Verificador] {resultado['tipo']} - {resultado['timestamp']} | media={resultado['media']:.2f} desv={resultado['desv']:.2f}")
            except Exception:
                continue

    print("Verificador terminó.")
