import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Carga de datos
df = pd.read_csv('dataset_inquilinos.csv', index_col='ID')

df.columns = ['horario', 'bioritmo', 'nivel_educativo', 'leer', 'animacion', 
              'cine', 'mascotas', 'cocinar', 'deporte', 'dieta', 'fumar', 'visitas',
              'orden', 'musica_tipo', 'musica_alta', 'plan_perfecto', 'instrumento']

# 3 One-Hot Encoding
df = df.astype(str).fillna("Desconocido")
encoder = OneHotEncoder(sparse_output=False)
df_encoded = pd.DataFrame(encoder.fit_transform(df), columns=encoder.get_feature_names_out(), index=df.index)

# 4 Matriz de compatibilidad
assert not df_encoded.isnull().values.any(), "Hay valores NaN en df_encoded"
matriz_s = np.dot(df_encoded, df_encoded.T)

# Definir el rango de destino
rango_min = -100
rango_mx = 100

# Encontrar mínimos y máximos de la matriz_s
min_original = np.min(matriz_s)
max_original = np.max(matriz_s)

# Reescalar la matriz
matriz_s_reescalada = (matriz_s - min_original) / (max_original - min_original) * (rango_mx - rango_min) + rango_min

# Pasar a pandas
df_similitud = pd.DataFrame(matriz_s_reescalada, index=df.index, columns=df.index)

# 5 Búsqueda de inquilinos compatibles


def inquilinos_compatibles(id_inquilinos, topn):
    """
    Input:
    - id_inquilinos: lista de IDs de inquilinos a buscar.
    - topn: número de inquilinos más compatibles a encontrar.

    Output:
    Retorna una lista con dos elementos:
    1. Características de los inquilinos compatibles.
    2. Dato de similitud.
    """
    # Código de la función...

    # Verificar si todos los ID de inquilinos existen en la matriz de similitud
    for ID in id_inquilinos:
        if ID not in df_similitud.index:
            return f"Error: El ID {ID} no se encuentra en la base de datos."

    # Obtener las filas correspondientes a los inquilinos dados
    filas_inquilinos = df_similitud.loc[id_inquilinos]
    
    # Calcular la similitud promedio entre los inquilinos
    similitud_promedio = filas_inquilinos.mean(axis=0)
    
    # Ordenar los inquilinos en función de similitud promedio
    inquilinos_similares = similitud_promedio.dropna().sort_values(ascending=False)
    
    # Excluir los inquilinos de referencia
    inquilinos_similares = inquilinos_similares.drop(id_inquilinos)
    
    # Tomar los topn inquilinos más compatibles
    topn_inquilinos = inquilinos_similares.head(topn)
    
    # Obtener los registros de los inquilinos similares
    registros_similares = df.loc[topn_inquilinos.index]
    
    # Obtener los registros de los inquilinos buscados
    registros_buscados = df.loc[id_inquilinos]
    
    return [registros_similares, topn_inquilinos]
