#%%
#Importar librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
#Cargar data
archivo = 'ventas_starbucks_2025.csv'
df_starbucks = pd.read_csv(archivo)

#%%
#Mostrar informacion data
df_starbucks.info()

# %%
nan_columna = df_starbucks.isnull().sum()
nan_columna
print('Cantidad de valores nulos: ',nan_columna)
#%%
valores_unicos = df_starbucks.nunique()
valores_unicos
print('Valores unicos: ', valores_unicos)
# %%
cantidad_unicos = df_starbucks['Tamaño'].unique()
print('Cantidad unicos: ', cantidad_unicos)
# %%
duplicados = df_starbucks.duplicated().sum()
print('Cantidad de duplicados: ',duplicados)
# %%
df_starbucks['Nombre_Producto'].unique()
# %%
df_starbucks[df_starbucks['Nombre_Producto']=='Termo Reutilizable']
# %%
df_starbucks.query("Nombre_Producto == 'Termo Reutilizable'")


#%%
df_starbucks.groupby('Nombre_Producto')['Tamaño'].nunique()


#%%
print("Categorías de Producto con valores NULOS en 'Tamaño':")
print(df_starbucks[df_starbucks['Tamaño'].isnull()]['Categoría_Producto'].unique())

#%%
print("Categorías de Producto con valores NO NULOS en 'Tamaño':")
print(df_starbucks[df_starbucks['Tamaño'].notnull()]['Categoría_Producto'].unique())

# %%
#No tiene datos nulos
data_tama = df_starbucks[df_starbucks['Tamaño'].notnull()]
#tiene datos nulos
data_no_tama = df_starbucks[~df_starbucks['Tamaño'].notnull()]
#data_no_tama = df_starbucks[df_starbucks['Tamaño'].isna()]
#%%
#Verificacion que no tiene nulos
data_tama['Tamaño'].isna().sum()
#%%
#Verificacion que tiene nulos
data_no_tama['Tamaño'].isna().sum()
# %%

data_tama.info()

# %%
data_tama.head(10)
# %%
data_tama['Total_Factura'] = data_tama['Total_Venta'] - data_tama['Total_Venta']*(data_tama['Descuento_Miembro']/100)
data_tama.head(5)

#%%
#Esta es una forma de eliminar una columnas especifico
#data_no_tama.pop('Tamaño')
# %%
#Rellenar los datos nulos
# .mode relleno con la moda el cual es el valor que mas se 
# repite se rellena
#data_no_tama['Tamaño'].fillna(data_no_tama['Tamaño'].mode())
# .mean rellena con el promedio
#data_no_tama['Tamaño'].fillna(data_no_tama['Tamaño'].mean())
data_no_tama['Tamaño'] = data_no_tama['Tamaño'].fillna('Sin Tamaño')
data_no_tama.sample(5)
# %%
