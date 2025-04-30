import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

# Configurar la página para utilizar un layout más amplio
st.set_page_config(layout='wide')

resultado = None

# Mostrar imagen en la parte superior
st.image('/Users/rogeliohidalgo/Documents/visual_code/app/media/png-transparent-building-cartoon-facade-building-service-condominium-apartment-thumbnail.png', use_container_width=True)

# Insertar un espacio vertical de 60px
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Configurar el sidebar con inputs y un botón
with st.sidebar:
    st.header('¿Quién ya vive en el piso?')
    inquilino1 = st.text_input('Inquilino 1')
    inquilino2 = st.text_input('Inquilino 2')
    inquilino3 = st.text_input('Inquilino 3')

    num_compañeros = st.text_input('¿Cuántos nuevos compañeros quieres buscar?')

    if st.button('Buscar compañeros'):
        # Verificar que el número de compañeros sea válido
        num_compañeros = num_compañeros.strip()
        if num_compañeros.isdigit():
            topn = int(num_compañeros)
        else:
            st.error('Por favor ingrese un número válido para el número de compañeros')
            topn = None

        # Obtener los identificadores de inquilinos
        id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn)
        
        if id_inquilinos and topn is not None:
            # Llamar a la función inquilinos_compatibles
            resultado = inquilinos_compatibles(id_inquilinos, topn)

# Verificar si `resultado` contiene un mensaje de error (cadena de texto)
if isinstance(resultado, str):
    st.error(resultado)
# Si no, y si `resultado` no es None, mostrar el gráfico de barras y la tabla
elif resultado is not None and isinstance(resultado, (list, tuple)) and len(resultado) == 2:
    cols = st.columns((1, 2))  # Divide el layout en dos columnas
    with cols[0]:
        st.write('Nivel de compatibilidad de cada nuevo compañero:')
        fig_grafico = generar_grafico_compatibilidad(resultado[1])
        st.pyplot(fig_grafico)
    with cols[1]:
        st.write('Comparativo entre compañeros:')
        df_compatibles = resultado[0]  # Extrae la tabla de inquilinos compatibles
        st.dataframe(df_compatibles)
        #fig_tabla = generar_tabla_compatibilidad(resultado)
        #st.plotly_chart(fig_tabla, use_container_width=True)
