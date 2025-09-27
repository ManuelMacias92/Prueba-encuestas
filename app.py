import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Encuestas de Satisfacción",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Analizador de Encuestas de Satisfacción")
st.markdown("**Limpia, analiza y visualiza los datos de tu encuesta automáticamente**")

# Sidebar para navegación
st.sidebar.title("🛠️ Herramientas")
opcion = st.sidebar.selectbox(
    "Selecciona una opción:",
    ["🏠 Inicio", "📤 Cargar y Limpiar Datos", "📈 Análisis y Gráficos"]
)

# Función para normalizar texto
def normalizar_texto(s):
    if not isinstance(s, str):
        return s
    
    # Reemplazos básicos sin caracteres especiales problemáticos
    s = s.replace("Ã¡", "á")
    s = s.replace("Ã©", "é")
    s = s.replace("Ã­", "í")
    s = s.replace("Ã³", "ó")
    s = s.replace("Ãº", "ú")
    s = s.replace("Ã±", "ñ")
    s = s.replace("Â¿", "")
    s = s.replace("Â¡", "")
    s = s.replace("Â", "")
    return s.strip()

def limpiar_dataframe(df_raw):
    df = df_raw.copy()
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [normalizar_texto(f"{c1} {c2}").strip() for c1, c2 in df.columns]
    
    for col in df.columns:
        df[col] = df[col].astype(str).apply(normalizar_texto)

    df = df.replace({"sí": 1, "si": 1, "no": 0, "nan": 0}, regex=True)

    escala = {
        "excelente": 5, "muy bueno": 4, "bueno": 3,
        "regular": 2, "deficiente": 1, "malo": 1, "muy malo": 0
    }

    def escala_map(valor):
        if isinstance(valor, str):
            if ":" in valor:
                valor = valor.split(":")[-1]
            valor = valor.strip().lower()
            return escala.get(valor, None)
        return valor

    for col in df.columns:
        if any(keyword in col.lower() for keyword in ["evalua", "experiencia", "califica"]):
            df[f"{col} (num)"] = df[col].apply(escala_map)
            
    return df

def encontrar_columna_sesiones(df):
    """Encuentra automáticamente la columna que contiene las sesiones"""
    for col in df.columns:
        if any(palabra in col.lower() for palabra in ["sesion", "session", "evaluar"]):
            return col
    return None

# ================== PÁGINA INICIO ==================
if opcion == "🏠 Inicio":
    st.markdown("## 👋 ¡Bienvenido!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✨ Características principales:
        - 🧹 **Limpieza automática** de caracteres especiales
        - 🔄 **Conversión** de respuestas "Sí/No" a valores numéricos
        - 📊 **Visualizaciones interactivas** de los resultados
        - 🏆 **Ranking** de sesiones mejor y peor evaluadas
        - 📱 **Interfaz amigable** y fácil de usar
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Cómo usar la app:
        1. Ve a **"Cargar y Limpiar Datos"**
        2. Sube tu archivo CSV de encuesta
        3. Revisa los datos limpios
        4. Ve a **"Análisis y Gráficos"** para visualizar
        5. Descarga los resultados procesados
        """)
    
    st.info("💡 **Tip:** Asegúrate de que tu CSV tenga encabezados en las primeras filas y datos de sesiones para obtener mejores resultados.")

# ================== PÁGINA CARGAR DATOS ==================
elif opcion == "📤 Cargar y Limpiar Datos":
    st.markdown("## 📤 Carga tu archivo CSV")
    
    archivo_subido = st.file_uploader(
        "Selecciona tu archivo de encuesta:",
        type=['csv'],
        help="Sube un archivo CSV con los datos de tu encuesta de satisfacción"
    )
    
    if archivo_subido is not None:
        try:
            # Leer el archivo
            contenido = archivo_subido.read().decode('latin1')
            df_original = pd.read_csv(StringIO(contenido), header=[0, 1])
            
            st.success(f"✅ Archivo cargado exitosamente: {archivo_subido.name}")
            st.info(f"📏 Dimensiones: {df_original.shape[0]} filas × {df_original.shape[1]} columnas")
            
            # Mostrar vista previa de datos originales
            with st.expander("👀 Vista previa de datos originales"):
                st.dataframe(df_original.head())
            
            # Limpiar datos
            with st.spinner("🧹 Limpiando datos..."):
                df_limpio = limpiar_dataframe(df_original.copy())
            
            st.success("✅ ¡Datos limpiados exitosamente!")
            
            # Mostrar datos limpios
            st.markdown("### 🎉 Datos Procesados")
            st.dataframe(df_limpio.head())
            
            # Guardar en session_state
            st.session_state['df_limpio'] = df_limpio
            st.session_state['nombre_archivo'] = archivo_subido.name
            
            # Botón para descargar
            csv_limpio = df_limpio.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Descargar datos limpios",
                data=csv_limpio,
                file_name=f"{archivo_subido.name.replace('.csv', '_LIMPIO.csv')}",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")

# ================== PÁGINA ANÁLISIS ==================
elif opcion == "📈 Análisis y Gráficos":
    st.markdown("## 📈 Análisis de Datos")
    
    if 'df_limpio' not in st.session_state:
        st.warning("⚠️ Primero debes cargar y limpiar un archivo en la sección anterior.")
        st.stop()
    
    df = st.session_state['df_limpio']
    
    # Encontrar columna de sesiones
    col_sesiones = encontrar_columna_sesiones(df)
    
    if col_sesiones is None:
        st.warning("⚠️ No se pudo identificar automáticamente la columna de sesiones.")
        col_sesiones = st.selectbox("Selecciona la columna que contiene las sesiones:", df.columns)
    else:
        st.info(f"✅ Columna de sesiones detectada: **{col_sesiones}**")
    
    # Encontrar columnas numéricas de evaluación
    cols_numericas = [col for col in df.columns if "(num)" in col]
    
    if len(cols_numericas) == 0:
        st.warning("No se encontraron columnas de evaluación numérica.")
        st.stop()
    
    # Calcular promedios por sesión
    st.markdown("### 📊 Cálculo de Promedios por Sesión")
    
    promedios_sesion = {}
    conteos_sesion = {}
    
    for idx, row in df.iterrows():
        sesion = row[col_sesiones]
        if pd.isna(sesion) or sesion == "" or str(sesion) == "nan":
            continue
            
        if sesion not in promedios_sesion:
            promedios_sesion[sesion] = 0
            conteos_sesion[sesion] = 0
        
        suma_fila = 0
        count_fila = 0
        for col_num in cols_numericas:
            valor = row[col_num]
            try:
                valor_num = float(valor)
                if not pd.isna(valor_num):
                    suma_fila += valor_num
                    count_fila += 1
            except:
                continue
        
        if count_fila > 0:
            promedios_sesion[sesion] += suma_fila
            conteos_sesion[sesion] += count_fila
    
    # Calcular promedios finales
    resultados = []
    for sesion in promedios_sesion:
        if conteos_sesion[sesion] > 0:
            promedio = promedios_sesion[sesion] / conteos_sesion[sesion]
            resultados.append({"Sesión": sesion, "Promedio": promedio, "Evaluaciones": conteos_sesion[sesion]})
    
    if len(resultados) == 0:
        st.error("No se pudieron calcular promedios. Verifica los datos.")
        st.stop()
    
    df_resultados = pd.DataFrame(resultados).sort_values("Promedio", ascending=False)
    
    # Mostrar tabla de resultados
    st.dataframe(df_resultados, use_container_width=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top 10 Mejor Evaluadas")
        top_10_mejores = df_resultados.head(10)
        fig1 = px.bar(
            top_10_mejores, 
            x="Sesión", 
            y="Promedio",
            title="Sesiones Mejor Evaluadas",
            color="Promedio",
            color_continuous_scale="Greens"
        )
        fig1.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### 📉 Top 10 Peor Evaluadas")
        top_10_peores = df_resultados.tail(10)
        fig2 = px.bar(
            top_10_peores, 
            x="Sesión", 
            y="Promedio",
            title="Sesiones Peor Evaluadas",
            color="Promedio",
            color_continuous_scale="Reds"
        )
        fig2.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Métricas principales
    st.markdown("### 🎯 Métricas Clave")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        mejor_sesion = df_resultados.iloc[0]
        st.metric("🏆 Mejor Sesión", mejor_sesion["Sesión"], f"{mejor_sesion['Promedio']:.2f}")
    
    with col2:
        peor_sesion = df_resultados.iloc[-1]
        st.metric("📉 Peor Sesión", peor_sesion["Sesión"], f"{peor_sesion['Promedio']:.2f}")
    
    with col3:
        promedio_general = df_resultados["Promedio"].mean()
        st.metric("📊 Promedio General", f"{promedio_general:.2f}")
    
    with col4:
        total_sesiones = len(df_resultados)
        st.metric("🔢 Total Sesiones", total_sesiones)
