import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import time

# Configuración de página
st.set_page_config(
    page_title="AQI Analytics Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2530;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .ficha {
        background-color: #1e2530;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #00f2fe;
        margin-bottom: 15px;
    }
    .titulo-principal {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Coordenadas aproximadas para el mapa
COORDINATES = {
    "medellin": [6.2442, -75.5812],
    "bogota": [4.7110, -74.0721],
    "cali": [3.4516, -76.5320],
    "mexico": [19.4326, -99.1332],
    "shanghai": [31.2304, 121.4737]
}

TOKEN = "0ecf8b1be391472a46de9047db71be0fef77eeb5"
CIUDADES = ["medellin", "bogota", "cali", "mexico", "shanghai"]

@st.cache_data(ttl=300) # Cache por 5 minutos
def get_aqi_data():
    datos = []
    for ciudad in CIUDADES:
        try:
            url = f"https://api.waqi.info/feed/{ciudad}/?token={TOKEN}"
            response = requests.get(url)
            data = response.json()
            if data.get("status") == "ok":
                aqi = data["data"]["aqi"]
                # Convertir AQI a numérico. A veces trae '-' si no hay dato
                try:
                    aqi = int(aqi)
                except:
                    aqi = 0
                
                nombre = data["data"]["city"]["name"]
                fecha = data["data"]["time"]["s"]
                
                datos.append({
                    "id_ciudad": ciudad,
                    "ciudad": nombre,
                    "fecha": fecha,
                    "AQI": aqi,
                    "lat": COORDINATES.get(ciudad, [0,0])[0],
                    "lon": COORDINATES.get(ciudad, [0,0])[1]
                })
        except Exception as e:
            pass
            
    df = pd.DataFrame(datos)
    return df

def clasificar_aqi(valor):
    if valor <= 50: return "Buena"
    elif valor <= 100: return "Moderada"
    elif valor <= 150: return "Dañina grupos sensibles"
    elif valor <= 200: return "Dañina"
    elif valor <= 300: return "Muy Dañina"
    else: return "Peligrosa"

def get_color_aqi(categoria):
    colores = {
        "Buena": "#00e400",
        "Moderada": "#ffff00",
        "Dañina grupos sensibles": "#ff7e00",
        "Dañina": "#ff0000",
        "Muy Dañina": "#8f3f97",
        "Peligrosa": "#7e0023"
    }
    return colores.get(categoria, "#808080")

def recomendacion(categoria):
    if categoria == "Buena": return "🟢 Actividades al aire libre sin restricciones."
    elif categoria == "Moderada": return "🟡 Sensibles: Reducir actividad prolongada."
    elif categoria == "Dañina grupos sensibles": return "🟠 Evitar ejercicio intenso en exteriores."
    elif categoria == "Dañina": return "🔴 Usar mascarilla y limitar exposición."
    elif categoria == "Muy Dañina": return "🟣 Evitar toda actividad física al aire libre."
    else: return "🟤 Peligro: Activar alerta sanitaria y confinamiento."

# Panel Lateral de Navegación
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3029/3029373.png", width=100)
st.sidebar.markdown("## Menú de Navegación")
opcion_menu = st.sidebar.radio(
    "Selecciona un módulo:",
    ["Dashboard Principal (Tiempo Real)", "Análisis Prescriptivo", "Fichas de Paso"]
)

st.sidebar.markdown("---")
st.sidebar.info("Proyecto: Análisis Prescriptivo de Calidad del Aire\nAutor: Feibert Guzmán")

# Obtener y preparar datos
with st.spinner("Obteniendo medidas en tiempo real de la API de WAQI..."):
    df = get_aqi_data()

if not df.empty:
    df["Categoría"] = df["AQI"].apply(clasificar_aqi)
    df["Recomendación"] = df["Categoría"].apply(recomendacion)
    df["Color"] = df["Categoría"].apply(get_color_aqi)

if opcion_menu == "Dashboard Principal (Tiempo Real)":
    st.markdown('<p class="titulo-principal">🌍 Monitor Global de Calidad del Aire</p>', unsafe_allow_html=True)
    st.write("Análisis en tiempo real utilizando datos de estaciones ambientales oficiales (WAQI).")
    
    if df.empty:
        st.error("No se pudieron cargar los datos de la API en este momento.")
    else:
        # Filtros
        st.markdown("### 🔍 Filtros de Análisis")
        col1, col2 = st.columns(2)
        with col1:
            ciudades_sel = st.multiselect("Filtrar por Ciudades", options=df["ciudad"].unique(), default=df["ciudad"].unique())
        with col2:
            categorias_sel = st.multiselect("Filtrar por Niveles de AQI", options=df["Categoría"].unique(), default=df["Categoría"].unique())
            
        df_filtrado = df[(df["ciudad"].isin(ciudades_sel)) & (df["Categoría"].isin(categorias_sel))]
        
        st.markdown("---")
        
        # Métricas
        st.markdown("### 📊 Perspectiva General")
        metrics_cols = st.columns(len(df_filtrado) if len(df_filtrado) > 0 else 1)
        for idx, row in df_filtrado.reset_index().iterrows():
            if idx < len(metrics_cols):
                with metrics_cols[idx]:
                    st.metric(label=row["ciudad"], value=f"{row['AQI']} AQI", delta=row["Categoría"], delta_color="off")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_map, col_chart = st.columns([1.5, 1])
        
        with col_map:
            st.markdown("### 🗺️ Mapa de Monitoreo")
            # Mapa centrado promedio
            if not df_filtrado.empty:
                mapCenter = [df_filtrado['lat'].mean(), df_filtrado['lon'].mean()]
                m = folium.Map(location=mapCenter, zoom_start=2, width="100%", height=400)
                
                for i, row in df_filtrado.iterrows():
                    html_tooltip = f"<b>{row['ciudad']}</b><br>AQI: {row['AQI']}<br>Cat: {row['Categoría']}"
                    folium.CircleMarker(
                        location=[row['lat'], row['lon']],
                        radius=15,
                        popup=row['Recomendación'],
                        tooltip=html_tooltip,
                        color=row['Color'],
                        fill=True,
                        fill_color=row['Color'],
                        fill_opacity=0.7
                    ).add_to(m)
                st_folium(m, height=400, returned_objects=[])
        
        with col_chart:
            st.markdown("### 📈 Comparativa AQI")
            if not df_filtrado.empty:
                fig = px.bar(
                    df_filtrado, 
                    x="ciudad", 
                    y="AQI", 
                    color="Categoría",
                    color_discrete_map={
                        "Buena": "#00e400", "Moderada": "#ffff00", 
                        "Dañina grupos sensibles": "#ff7e00", "Dañina": "#ff0000", 
                        "Muy Dañina": "#8f3f97", "Peligrosa": "#7e0023"
                    },
                    text="AQI"
                )
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📋 Tabla de Frecuencias y Datos Brutos")
        st.dataframe(df_filtrado[["ciudad", "fecha", "AQI", "Categoría", "Recomendación"]], use_container_width=True)

elif opcion_menu == "Análisis Prescriptivo":
    st.markdown('<p class="titulo-principal">🧠 Motor Prescriptivo de Salud Pública</p>', unsafe_allow_html=True)
    st.write("Con base en el análisis predictivo/tiempo real, el sistema genera recomendaciones paramétricas.")
    
    if not df.empty:
        for idx, row in df.iterrows():
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {row['Color']}20, transparent); border-left: 5px solid {row['Color']}; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <h3 style="margin:0;">{row['ciudad']} <span style="font-size: 1rem; color: #aaa;">| Reporte a las: {row['fecha']}</span></h3>
                <h4 style="color: {row['Color']}; margin: 5px 0;">Nivel de Alerta: {row['Categoría']} (AQI: {row['AQI']})</h4>
                <p style="margin:0; font-size: 1.1rem;"><b>Acción Prescriptiva:</b> {row['Recomendación']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
         st.warning("No hay datos para generar análisis.")

elif opcion_menu == "Fichas de Paso":
    st.markdown('<p class="titulo-principal">📚 Fichas de Paso Metodológicas</p>', unsafe_allow_html=True)
    st.write("Recorrido paso a paso (basado en el cuaderno Jupyter original) de la arquitectura del proyecto.")
    
    st.markdown("""
    <div class="ficha">
        <h3>Paso 1: Conexión API y Extracción</h3>
        <p>Se utiliza la API World Air Quality Index con <code>requests.get()</code> hacia <code>api.waqi.info/feed/</code> mediante un token de acceso autorizado para recopilar datos telemetrizados mundiales.</p>
    </div>
    <div class="ficha">
        <h3>Paso 2: Transformación (Pandas)</h3>
        <p>Los JSON resultantes con datos anidados espacialmente se normalizan creando listas de diccionarios. Estas son ingeridas por <code>pd.DataFrame()</code> para un tratamiento relacional tabular de alto rendimiento.</p>
    </div>
    <div class="ficha">
        <h3>Paso 3: Funciones de Regla de Negocio (Clasificación)</h3>
        <p>Se aplica la función <code>clasificar_aqi(valor)</code> mediante mapeo vectorial <code>df['AQI'].apply()</code>. Se utilizan los intervalos internacionales estandarizados que transforman números continuos en factores categóricos de riesgo.</p>
    </div>
    <div class="ficha">
        <h3>Paso 4: Inferencia Prescriptiva</h3>
        <p>Sobre el factor categórico, se aplica otro paso de transformación <code>recomendacion(categoria)</code>. El algoritmo infiere y prescribe la decisión de salud pública correspondiente (e.g. 'Reducir actividad').</p>
    </div>
    <div class="ficha">
        <h3>Paso 5: Visualización de Interfaz e Interacción</h3>
        <p>Las librerías <b>Streamlit</b>, <b>Plotly</b>, y <b>Folium</b> unen los scripts del backend de Python y exponen un Front-End reactivo capaz de renderizar dashboards profesionales en el navegador en escasos milisegundos.</p>
    </div>
    """, unsafe_allow_html=True)
