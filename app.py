
### Despliegue en la Nube
- **Streamlit Cloud**: Conecta directamente tu repositorio de GitHub
- **Heroku**: Usa el `Procfile` incluido para despliegue automático

## 🌐 Demo en Vivo

👉 **[Ver Demo en Streamlit Cloud](https://share.streamlit.io/TU_USUARIO/analizador-encuestas/main/app.py)**

## 📋 Requisitos del Sistema

- Python 3.8+
- Librerías principales:
  - streamlit >= 1.28.0
  - pandas >= 1.3.0
  - plotly >= 5.0.0
  - numpy >= 1.20.0

## 🎯 Uso de la Aplicación

### 📁 Paso 1: Cargar y Limpiar Datos
1. Ve a la sección **"📤 Cargar y Limpiar Datos"**
2. Usa el **file uploader** para subir tu archivo CSV
3. Revisa la vista previa de los datos originales
4. Los datos se limpian automáticamente al cargar

### 📊 Paso 2: Análisis y Gráficos
1. Ve a la sección **"📈 Análisis y Gráficos"**
2. Visualiza la tabla de resultados con métricas clave
3. Explora los gráficos interactivos con zoom y hover
4. Descarga los resultados procesados

## 📊 Formato de Datos Soportado

Tu archivo CSV debe contener:
- **Encabezados** en las primeras dos filas
- **Columna de sesiones** (ej: "Sesión 1", "Sesión 2")
- **Columnas de evaluación** con escalas como:
  - Excelente, Muy Bueno, Bueno, Regular, Deficiente, Malo
  - Sí / No
  - Valores numéricos

## 🌐 Despliegue en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona tu repositorio
4. Especifica `app.py` como archivo principal
5. ¡Tu app estará en línea en minutos!

## 📝 Changelog

### v2.0.0 (2025-09-27)
- 🌐 **BREAKING**: Migración completa de Tkinter a Streamlit
- ✅ Interfaz web moderna y responsiva
- ✅ Gráficos interactivos con Plotly
- ✅ Despliegue en la nube listo
- ✅ Navegación por pestañas mejorada

## 🚀 Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Gráficos**: Plotly Express
- **Procesamiento**: Pandas, NumPy
- **Despliegue**: Streamlit Cloud

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**[Tu Nombre]**
- GitHub: [@tu_usuario](https://github.com/tu_usuario)
- Email: tu.email@example.com

## 🙏 Agradecimientos

- Construido con ❤️ usando Streamlit
- Gráficos interactivos con Plotly
- Inspirado en la necesidad de democratizar el análisis de encuestas
