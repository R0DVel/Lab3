import streamlit as st
import pandas as pd
import altair as alt
import csv
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F5E7FE;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title(":bar_chart: Analizador de Archivos CSV")

tab1, tab2, tab3, tab4 = st.tabs([
    ":red_car: Vehículos", 
    ":weight_lifting_woman: Gimnasio", 
    ":video_game: Videojuegos", 
    ":clapper: Netflix"
])

with tab1:
    st.title(":red_car: Electric Vehicle Population")
    df = pd.read_csv("Electric_Vehicle_Population.csv")
    st.header(":pushpin: Datos del Archivo CSV")
    st.write("Numero de filas:", df.shape[0])
    st.write("Numero de columnas:", df.shape[1]) 
    st.header(":clipboard: Nombres de la columnas:")
    df.columns
    st.header(":eyes: Primeras 6 filas")
    st.dataframe(df.head(6))
    st.header(":chart_with_upwards_trend: Estadísticas Generales")
    st.write(df.describe())
    st.divider()
    #Ingreso de nuevos datos
    tabla_simple_v = df[["Model Year", "Electric_Range", "Base_MSRP"]]
    st.subheader("Agregar vehículo")
    # inputs
    anio = st.number_input("Año del modelo", min_value=2000, max_value=2025)
    rango = st.number_input("Rango eléctrico")
    precio = st.number_input("Precio base")
    # botón
    if st.button("Agregar vehículo"):
        nueva_fila = [anio, rango, precio]
        tabla_simple_v.loc[len(tabla_simple_v)] = nueva_fila
        st.success("Vehículo agregado")
    # mostrar tabla
    st.dataframe(tabla_simple_v)
    st.divider()
    # Nueva columna Categoria de Rango
    rango = 'Electric_Range' if 'Electric_Range' in df.columns else None
    if rango is not None:
        df['RangoCategoria'] = df[rango].apply(lambda x: 'Bajo' if x < 100 else 'Medio' if x <= 250 else 'Alto')
    else:
        df['RangoCategoria'] = None
    st.header("Primeras 6 filas con Rango Electrico como nueva columna:")
    st.dataframe(df.head(6))
    st.divider()
    # Filtros implementados en base a año del modelo y el precio
    st.header("Filtrar Vehículos Eléctricos")
    añoModelo = st.number_input("Filtrar vehículos con modelo antes de:", min_value=2000, max_value=2025, value=2025)
    valorMax = st.number_input("Filtrar vehículos con MSRP Base menor que ($):", min_value=0.0, max_value=845000.0, value=845000.0)
    filtered_df = df[(df['Model Year'] < añoModelo) & (df['Base_MSRP'] < valorMax)]
    st.header("Datos Filtrados")
    st.write("Numero de filas después del filtro:", filtered_df.shape[0])
    st.header("Primeras 6 filas despues de los filtros:")
    st.dataframe(filtered_df.head(6))
    #Registros que pertenecen a cada categoria de rango electrico
    st.header("Cantidad de registros por Categoría de Rango:")
    st.write(df['RangoCategoria'].value_counts())
    st.divider()
    # Gráfico de barras para la cantidad de registros por categoría de rango de carros electricos
    count_rango = df['RangoCategoria'].value_counts().reset_index()
    count_rango.columns = ['Categoria', 'Cantidad']
    chart_rango = alt.Chart(count_rango).mark_bar().encode(
        x=alt.X('Categoria:N', title='Categoría de rango eléctrico'),
        y=alt.Y('Cantidad:Q', title='Número de registros'),
        color=alt.Color('Categoria:N', legend=None),
        tooltip=['Categoria', 'Cantidad']
    ).properties(title='Electric Vehicle Population: Registros por Categoría de Rango')
    st.altair_chart(chart_rango, use_container_width=True)

with tab2:
    #Parte del gym
    st.title(":weight_lifting_woman: Gym Exercise Tracking")
    df = pd.read_csv("GymExerciseTracking.csv")
    st.header(":pushpin: Datos de la Aplicación")
    st.write("Numero de filas:", df.shape[0])
    st.write("Numero de columnas:", df.shape[1]) 
    st.header("Nombres de la columnas")
    df.columns
    st.header("Primeras 6 filas")
    st.dataframe(df.head(6))
    st.header("Estadísticas Generales")
    st.write(df.describe())
    st.divider()
    # Nueva columna Categoria de NivelDeFrecuencia (GYM)
    nivel = 'Workout_Frequency (days/week)' if 'Workout_Frequency (days/week)' in df.columns else None
    if nivel is not None:
        df['Frecuencia'] = df[nivel].apply(lambda x: 'Bajo' if 1 <= x <= 3 else 'Medio' if 4 <= x <= 5 else 'Alto' if x >= 6 else None)
    else:
        df['Frecuencia'] = None
    st.header("Primeras 6 filas con Nivel de Frecuencia como nueva columna:")
    st.dataframe(df.head(6))
    st.divider()
    # Filtrado de datos en base a calorias quemadas y porcentaje de grasa
    st.header("Filtrar Ejercicios")
    caloriasMin = st.number_input("Ejercicios con Calorías Quemadas mayor o igual a:", min_value=0.0, value=0.0)
    PorcentageDeGrasa = st.number_input("Ejercicios con Porcentaje de Grasa menor o igual a (%):", min_value=0.0, max_value=100.0, value=100.0)
    filtered_df = df[(df['Calories_Burned'] >= caloriasMin) & (df['Fat_Percentage'] <= PorcentageDeGrasa)]
    st.header("Datos Filtrados")
    st.write("Numero de filas después del filtro:", filtered_df.shape[0])
    st.header("Primeras 6 filas de los datos filtrados")
    st.dataframe(filtered_df.head(6))
    #Registros que pertenecen a cada categoria de la varible de frecuencia
    st.header("Cantidad de registros por Nivel de Frecuencia:")
    st.write(df['Frecuencia'].value_counts())
    st.divider()
    # Gráfico de barras para la cantidad de registros por categoría de frecuencia de ejercicios
    count_frecuencia = df['Frecuencia'].value_counts().reset_index()
    count_frecuencia.columns = ['Frecuencia', 'Cantidad']
    chart_frecuencia = alt.Chart(count_frecuencia).mark_bar().encode(
        x=alt.X('Frecuencia:N', title='Nivel de Frecuencia'),
        y=alt.Y('Cantidad:Q', title='Número de registros'),
        color=alt.Color('Frecuencia:N', legend=None),
        tooltip=['Frecuencia', 'Cantidad']
    ).properties(title='Gym Exercise Tracking: Registros por Nivel de Frecuencia')
    st.altair_chart(chart_frecuencia, use_container_width=True)

with tab3:
    #Datos de la tienda de steam 
    st.title(":video_game: Steam Store data 2024")
    df = pd.read_csv("steam_store_data_2024.csv")
    st.header(" :pushpin: Datos de la Tienda de Steam")
    st.write("Numero de filas:", df.shape[0])
    st.write("Numero de columnas:", df.shape[1]) 
    st.header("Nombres de la columnas")
    df.columns
    st.header("Primeras 6 filas")
    st.dataframe(df.head(6))
    st.header("Estadísticas Generales")
    st.write(df.describe())
    st.divider()
    #Ingreso de nuevos datos
    st.subheader("Agregar videojuego :video_game:")
    tabla_simple2 = df[["title", "description", "price", "salePercentage", "recentReviews","allReviews"]]
    #inputs
    titulo=st.text_input("Nombre del juego")
    descripcion=st.text_input("Breve descripción del juego")
    precio2 = st.number_input("Precio del juego")
    porcentaje=st.number_input("Ingrece e procentaje de ventas del juego")
    reviews=st.text_input("Escriba una review del juego")
    all_review=st.text_input("Escrib su opinión general del juego")
    porcentaje_texto = f"-{int(porcentaje)}%"
    #boton
    if st.button("Agregar juego"):
        nueva_fila = [titulo, descripcion, precio2, porcentaje_texto,reviews, all_review]
        tabla_simple2.loc[len(tabla_simple2)] = nueva_fila
        st.success("Juego agregado")
    # mostrar tabla
    st.dataframe(tabla_simple2)
    # Nueva columna Categoria de Gama de Juego
    df['price'] = df['price'].str.split("$").str[1]
    gama = 'price' if 'price' in df.columns else None
    if gama is not None:
        df['Gama'] = df[gama].apply(lambda x: 'Baja' if float(x) < 10 else 'Media' if 10 <= float(x) <= 24 else 'Alto' if float(x) >= 25 else None) 
    else:
        df['Gama'] = None
    st.header("Primeras 6 filas con Gama como nueva columna:")
    st.dataframe(df.head(6))
    st.divider()
    # Filtrado de datos en base a precio y porcentaje de descuento
    st.header(":moneybag: Filtros para los Juegos")
    precioMin = st.number_input("Juegos con Precio superior a ($):", min_value=0.0, value=0.0)
    descuentoMax = st.number_input("Juegos con Porcentaje de descuento menor a (%):", min_value=0.0, max_value=100.0, value=100.0)
    # filtro precio
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    filtrado_precio = df[df['price'] > precioMin]
    st.write("Filtrado por precio")
    st.dataframe(filtrado_precio.head())
    # filtro descuento
    df['salePercentage'] = df['salePercentage'].astype(str)
    df['salePercentage'] = df['salePercentage'].str.replace('%', '')
    df['salePercentage'] = df['salePercentage'].str.replace('-', '')  # ← ESTA ES LA CLAVE
    df['salePercentage'] = pd.to_numeric(df['salePercentage'], errors='coerce')
    filtrado_descuento = df[df['salePercentage'] < descuentoMax]
    st.write("Filtrado por descuento")
    st.dataframe(filtrado_descuento.head())
    st.divider()
    #Registros que pertenecen a cada categoria de la varible de gama
    st.header("Cantidad de registros por Gama:")
    st.write(df['Gama'].value_counts())
    st.divider()
    # Gráfico de barras para la cantidad de registros por categoría de gama de juegos
    count_gama = df['Gama'].value_counts().reset_index()
    count_gama.columns = ['Gama', 'Cantidad']
    chart_gama = alt.Chart(count_gama).mark_bar().encode(
        x=alt.X('Gama:N', title='Gama de Juego'),
        y=alt.Y('Cantidad:Q', title='Número de registros'),
        color=alt.Color('Gama:N', legend=None),
        tooltip=['Gama', 'Cantidad']
    ).properties(title='Steam Store data 2024: Registros por Gama')
    st.altair_chart(chart_gama, use_container_width=True)

with tab4:
    #Datos de Netflix :D
    st.title(":clapper: Netflix titulos")
    df = pd.read_csv("netflix_titles.csv")
    st.header("Datos de Netflix :pushpin:")
    st.write("Numero de filas:", df.shape[0])
    st.write("Numero de columnas:", df.shape[1]) 
    st.header("Nombres de la columnas")
    df.columns
    st.header("Primeras 6 filas")
    st.dataframe(df.head(6))
    st.header("Estadísticas Generales")
    st.write(df.describe())
    st.divider()
    #Filtrado de datos en base a duracion y año de filmacion
    st.header(":clapper: Títulos de Netflix")
    duracionMin = st.number_input("Películas con duración mayor a (minutos):", min_value=0, value=0)
    añoMax = st.number_input("Contenido añadido antes del año:", min_value=1900, max_value=2025, value=2025)
    st.divider()
    # Nueva columna de Categoria de Tipo de audiencia (Netflix)
    tipoDeAudiencia = 'rating' if 'rating' in df.columns else None
    if tipoDeAudiencia is not None:
        df['TipoDeAudiencia'] = df[tipoDeAudiencia].apply(lambda x: 'Niños' if x in ['G', 'TV-Y', 'TV-G', 'TV-Y7', 'TV-Y7-FV'] else 'Adolescentes' if x in ['PG', 'TV-PG'] else 'Adultos' if x in ['R', 'TV-MA', 'NC-17'] else "Jóvenes" if x in ['PG-13', 'TV-14'] else None)
    else:
        df['TipoDeAudiencia'] = None
    st.header("Primeras 6 filas con Tipo de Audiencia como nueva columna:")
    st.dataframe(df.head(6))
    # Procesar datos para filtrado
    peliculas = df[df['type'] == 'Movie'].copy()
    peliculas['duration_min'] = peliculas['duration'].str.extract('(\d+)').astype(float)
    peliculas['date_added'] = pd.to_datetime(peliculas['date_added'], errors='coerce')
    filtered_df = peliculas[(peliculas['duration_min'] > duracionMin) & (peliculas['date_added'].dt.year < añoMax)]
    st.header("Datos Filtrados")
    st.write("Numero de filas:", filtered_df.shape[0])
    st.header("Primeras 6 filas")
    st.dataframe(filtered_df.head(6))
    st.divider()
    #Registros que pertenecen a cada categoria de la variable de tipo de audiencia
    st.header("Cantidad de registros por Tipo de Audiencia:")
    st.write(df['TipoDeAudiencia'].value_counts())
    st.divider()
    # Gráfico de barras para la cantidad de registros por categoría de tipo de audiencia
    count_audiencia = df['TipoDeAudiencia'].value_counts().reset_index()
    count_audiencia.columns = ['TipoDeAudiencia', 'Cantidad']
    chart_audiencia = alt.Chart(count_audiencia).mark_bar().encode(
        x=alt.X('TipoDeAudiencia:N', title='Tipo de Audiencia'),
        y=alt.Y('Cantidad:Q', title='Número de registros'),
        color=alt.Color('TipoDeAudiencia:N', legend=None),
        tooltip=['TipoDeAudiencia', 'Cantidad']
    ).properties(title='Netflix titulos: Registros por Tipo de Audiencia')
    st.altair_chart(chart_audiencia, use_container_width=True)
