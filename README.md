# 🧠 Sistema Concurrente de Análisis Biométrico

> Trabajo Práctico 1 – Computación II  
> Universidad / Cátedra – Año 2025

---

## 📌 Descripción

Este proyecto implementa un **sistema concurrente** distribuido en múltiples procesos que simula la captura, análisis y verificación de datos biométricos durante una prueba de esfuerzo. Está desarrollado en Python utilizando `multiprocessing` y técnicas de comunicación por `Pipe` y `Queue`.

---

## 🔧 Requisitos Técnicos

- Python 3.9 o superior
- Linux (recomendado)
- Librerías estándar:
  - `multiprocessing`
  - `queue`
  - `random`
  - `datetime`
  - `statistics`
  - `time`

---

## 🛠️ Instalación y ejecución

1. **Clonar o copiar el repositorio**
   ```bash
   git clone https://github.com/lgsosa/ComputacionII
   cd proyecto_biometrico

## Arquitectura de la TAREA 1

┌──────────────────────────────┐
│ Proceso Principal (main.py) │
│  - Genera 1 dato/seg por 60s │
│  - Envía a 3 procesos        │
└────────────┬────────────────┘
             │
             ▼
 ┌───────────┴───────────┐
 │ Comunicación vía Pipe│
 └────┬────────┬─────────┘
      ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│Proc A  │ │Proc B  │ │Proc C  │
│Frecuencia│Presión ││Oxígeno │
└────┬─────┴────┬────┴────┬────┘
     ▼          ▼         ▼
 ┌─────────────────────────────┐
 │     Proceso Verificador     │
 │  - Recibe por Queues        │
 │  - Imprime media/desvío     │
 └─────────────────────────────┘

👩‍💻 Autora
Luciana Sosa
Estudiante de Ingeniería en Informática
Facultad de Ingeniería – Universidad de Mendoza