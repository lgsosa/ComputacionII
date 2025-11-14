
# TP2 - Sistema de Scraping y Análisis Web Distribuido  
### **Computación II — Universidad de Mendoza**

## 📌 Descripción General

Este trabajo práctico implementa un sistema **distribuido**, compuesto por dos servidores independientes, que colaboran para realizar scraping, análisis web y procesamiento pesado en paralelo.  
El cliente interactúa únicamente con el servidor principal, logrando una arquitectura limpia, modular y completamente transparente.

El objetivo del TP es demostrar dominio en:

- Programación **asíncrona** con `asyncio`
- Programación **paralela** con `multiprocessing`
- Comunicación entre procesos usando **sockets TCP**
- Implementación de un **protocolo binario**
- Web Scraping real con **BeautifulSoup**
- Procesamiento de imágenes con **Pillow**
- Manejo de errores, caché, rate limit y timeouts
- Arquitectura distribuida y diseño limpio

---

# 🧩 Arquitectura General del Sistema

El proyecto contiene **tres componentes** principales:

---

## **1️⃣ Servidor de Procesamiento — Parte B**  
📄 Archivo: `server_processing.py`  
🧠 Función: ejecutar tareas pesadas en paralelo  
🛠 Tecnologías: `multiprocessing`, `socketserver`, `Pillow`

Este servidor se encarga de:

- Generar un screenshot (placeholder representativo)
- Analizar rendimiento de la página:
  - tiempo de carga
  - peso del HTML
  - cantidad de requests
- Generar thumbnails a partir de imágenes descargadas
- Responder al Servidor A mediante un protocolo binario

Corre en un puerto independiente (default **9000**) y usa un pool de procesos.

---

## **2️⃣ Servidor de Scraping Asíncrono — Parte A**  
📄 Archivo: `server_scraping.py`  
⚡ Tecnologías: `asyncio`, `aiohttp`

Su responsabilidad es:

- Recibir la URL del cliente
- Scrappear la página
- Obtener:
  - título
  - links
  - meta tags
  - estructura HTML (H1–H6)
  - cantidad de imágenes
- Descargar algunas imágenes
- Enviar datos al servidor B y recibir el procesamiento
- Consolidar un JSON final para el cliente

Incluye:

- Caché interna (TTL 1 hora)
- Rate limiting (5 requests por dominio por minuto)
- Manejo robusto de errores de red

Corre en el puerto **8000**.

---

## **3️⃣ Cliente de prueba**  
📄 Archivo: `client.py`

Realiza un GET al servidor principal y muestra el JSON final combinado.

---

# 📂 Estructura del Proyecto

```
TP2/
│── client.py
│── README.md
│── requirements.txt
│── server_scraping.py
│── server_processing.py
│
├── scraper/
│   ├── async_http.py
│   ├── html_parser.py
│   ├── metadata_extractor.py
│
├── processor/
│   ├── screenshot.py
│   ├── performance.py
│   ├── image_processor.py
│
└── common/
    ├── protocol.py
    ├── serialization.py
```

---

# 🚀 Cómo Ejecutar Todo Fácilmente

## **0️⃣ Entrar a la carpeta TP2**

```bash
cd TP2
```

---

# 🛠️ 1️⃣ Crear el entorno virtual (requerido en Linux)

```bash
python3 -m venv venv
```

Si aparece error sobre "venv", instalar:

```bash
sudo apt install python3-venv
python3 -m venv venv
```

---

# 🔌 2️⃣ Activar el entorno virtual

```bash
source venv/bin/activate
```

La terminal debe verse así:

```
(venv) usuario@pc:~/TP2$
```

---

# 📦 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ⚙️ 4️⃣ Levantar el Servidor de Procesamiento (Parte B)

Terminal 1:

```bash
python server_processing.py -i 127.0.0.1 -p 9000 -n 4
```

Debería mostrar:

```
[processing] escuchando en 127.0.0.1:9000
```

---

# 🌐 5️⃣ Levantar el Servidor de Scraping (Parte A)

Terminal 2:

```bash
cd TP2
source venv/bin/activate
python server_scraping.py -i 127.0.0.1 -p 8000 --processing-ip 127.0.0.1 --processing-port 9000
```

Verás:

```
======== Running on http://127.0.0.1:8000 ========
(Press CTRL+C to quit)
```

---

# 🧪 6️⃣ Probar con el Cliente

Terminal 3:

```bash
cd TP2
source venv/bin/activate
python client.py
```

---

# 📤 Ejemplo de Respuesta JSON

```json
{
  "url": "https://example.com",
  "timestamp": "2025-11-14T20:03:12.781989Z",
  "scraping_data": {
    "title": "Example Domain",
    "links": ["https://iana.org/domains/example"],
    "meta_tags": {},
    "structure": { "h1": 1, "h2": 0, "h3": 0, "h4": 0, "h5": 0, "h6": 0 },
    "images_count": 0
  },
  "processing_data": {
    "screenshot": "base64(...)",
    "performance": {
      "load_time_ms": 701,
      "total_size_kb": 0.5,
      "num_requests": 1
    },
    "thumbnails": []
  },
  "status": "success"
}
```

---
