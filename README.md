# 🌍 Análisis Prescriptivo de Calidad del Aire

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white) 
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) 
![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-v2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-Map-77B829?style=for-the-badge&logo=openstreetmap&logoColor=white)

> **Autor:** Feibert Guzmán  
> **Repositorio Oficial:** [Seguimiento_2](https://github.com/FeibertGuzman/Seguimiento_2.git)

## 📌 Descripción del Proyecto

Este proyecto es una solución integral orientada a la **Inteligencia de Datos Aplicada**. Se enfoca en extraer datos en tiempo real de la API *World Air Quality Index* (WAQI), los cuales son transformados, analizados, y presentados tanto en una impresionante Landing Page estática (`index.html`) con diseño *Glassmorphism*, como en un dashboard interactivo de **Streamlit** Python (`app.py`).

El análisis trasciende la estadística descriptiva al implementar lógica **Prescriptiva**; es decir, no solo visualiza el AQI (Air Quality Index) actual, sino que infiere mediante reglas de negocio la mejor acción en materia de salud pública (por ejemplo: "*Usar mascarilla*", "*Evitar exposición*").

---

## 🛠️ Tecnologías y Estructura

El ecosistema cuenta con dos interfaces destinadas a distintos modelos de consumo de información:

1. **`index.html`**: Una Landing Page desarrollada en HTML5 y Vanilla CSS que funciona como presentación ejecutiva. Documenta las **"Fichas de Paso"** del proyecto y guía visualmente a cualquier usuario a través del flujo de los datos.
2. **`app.py`**: El corazón analítico. Es una aplicación Web escrita en Streamlit (Python) que consolida:
   - Panel de navegación dinámico.
   - Filtros de consulta.
   - Conexión real a la API.
   - Visualización geográfica utilizando mapas de calor (`Folium`).
   - Tabuladores de frecuencia y gráficas (`plotly`, `pandas`).

---

## 🚀 Guía de Instalación y Despliegue (Clonación)

Si deseas obtener una copia de este proyecto para ejecutarlo en un servidor (VPS) o tu máquina local, sigue las instrucciones profesionales a continuación:

### 1. Clonar el repositorio

Abre tu terminal (PowerShell, Git Bash o CMD) y ejecuta el comando de clonación:

```bash
git clone https://github.com/FeibertGuzman/Seguimiento_2.git
```

### 2. Ingresar al directorio del proyecto

```bash
cd Seguimiento_2
```

### 3. Crear un entorno virtual (Recomendado)

Para aislar las dependencias y asegurarte de tener un entorno limpio:

```bash
python -m venv env
```

### 4. Activar el entorno virtual

* En **Windows**:
```bash
.\env\Scripts\activate
```

* En **Linux / macOS (VPS)**:
```bash
source env/bin/activate
```

### 5. Instalar los Requerimientos Universitarios

Instalamos todas las dependencias listadas en el `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 6. Ejecutar la Aplicación Streamlit

Arranca el servidor local de Streamlit para desplegar el dashboard prescriptivo interactivo:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador por defecto (usualmente en `http://localhost:8501`).

---

## 🌎 Visualizando la Landing Page

No requieres de un servidor para evaluar el diseño estético de la portada:
Simplemente abre el archivo **`index.html`** dándole doble clic o arrastrándolo a tu navegador de preferencia.

---

## 📝 Nota sobre Analítica Prescriptiva en Tiempo Real

El sistema automatiza un flujo de Machine Learning tradicional aplicando reglas lógicas. Extraído el AQI de ciudades críticas (*Medellín, Bogotá, Cali, México, Shanghai*), se evalúa y clasifica automáticamente. Modificar a nivel de código las variables en  `app.py` permite parametrizar las alertas e ingresar nuevas coordenadas geográficas de interés inmediato.

## 🌎 Realizado por:

> Feibert Alirio Guzmán Pérez
