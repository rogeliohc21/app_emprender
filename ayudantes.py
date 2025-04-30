import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st
from matplotlib.ticker import FuncFormatter

# Función para generar el gráfico de compatibilidad
def generar_grafico_compatibilidad(compatibilidad):
    compatibilidad = compatibilidad / 100

    # Configuración del gráfico de Seaborn
    fig, ax = plt.subplots(figsize=(5, 4))

    # Crear el gráfico de barras con los valores convertidos en porcentaje
    sns.barplot(x=compatibilidad.index, y=compatibilidad.values, ax=ax, color='lightblue')

    # Quitar bordes innecesarios
    sns.despine(top=True, right=True, bottom=False)

    # Configurar etiquetas de los ejes y rotar etiquetas del eje X
    ax.set_xlabel('Identificador del inquilino', fontsize=10)
    ax.set_ylabel('Similitud (%)', fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Ajustar etiquetas del eje Y con formato de porcentaje
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:,.1f}%'.format(y * 100)))

    # Añadir etiquetas de porcentaje sobre cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.1f}%'.format(height * 100),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=8)
    return fig    

# Función para generar la tabla de compañeros
def generar_tabla_compatibilidad(resultado):
    # Cambiar el nombre de la columna 'index' y ajustar el ancho de las columnas
    resultado_0_with_index = resultado[0].reset_index()
    resultado_0_with_index.rename(columns={resultado_0_with_index.columns[0]: 'ATRIBUTO'}, inplace=True)

    # Configurar la tabla de Plotly
    fig_table = go.Figure(data=[go.Table(
        columnwidth=[20] + [10] * (len(resultado_0_with_index.columns) - 1),
        header=dict(values=list(resultado_0_with_index.columns),
                    fill_color='paleturquoise',
                    align='left')),
    ])

    # Configurar el layout de la tabla de Plotly
    fig_table.update_layout(width=700, height=320, margin=dict(l=0, r=0, t=0, b=0))
    return fig_table

# Función para generar la lista de los inquilinos semilla
def obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn):
    # Crear una lista con los identificadores de inquilinos ingresados y convertirlos a enteros
    id_inquilinos = []
    for inquilino in [inquilino1, inquilino2, inquilino3]:
        try:
            if inquilino:  # Si hay algún texto en el input
                id_inquilinos.append(int(inquilino))  # Convertir a entero y agregar a la lista
        except ValueError:
            st.warning(f"El identificador '{inquilino}' no es un número válido y será ignorado.")
    
    return id_inquilinos  # Retorna la lista de inquilinos semilla con la cantidad de inquilinos solicitados
