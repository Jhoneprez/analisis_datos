#%%
import pandas as pd
import matplotlib.pyplot as plt
pd.options.display.max_columns = None

#Cargar el archivo
#%%
data = pd.read_csv("trade_data.csv", encoding="utf-8", sep=';')

#Muestra las columnas de la data
#%%
print(data.columns)

#%%
print(data.info())

#%%
#Muestra los 5 primero datos
print(data.head())

#%%
print(data.columns)

#%%
#Eliminar columnas innecesarias
columnas_utiles = ['Year', 'Cod', 'Product2', 'netWgt', 'cifvalue']
data = data[columnas_utiles]
print(data.columns)

# %%
#Renombrar las columnas a utilizar
data.rename(columns={
 "Year": "Anios",
 "Cod": "Codigo",
 "Product2": "Producto",
 "netWgt": "Peso_kg",
 "cifvalue": "Valor_USD"
}, inplace=True)
print(data.columns)

# %%
#Ver cuántas filas vacías hay
print(data.isnull().sum())

#%%
print(data.head())

# Muestra los 10 ultimos
#%%
print(data.tail(10))

# %%
#Convertir texto a números
data['Peso_kg'] = (
    data['Peso_kg']
    .astype(str)
    .str.replace('kg', '', case=False, regex=False)
    .str.replace(',', '', regex=False)
    .str.strip()
)
data['Peso_kg'] = pd.to_numeric(data['Peso_kg'], errors='coerce').round(1)
data['Valor_USD'] = (
    data['Valor_USD']
    .astype(str)
    .str.replace('$', '', regex=False)
    .str.replace('USD', '', case=False, regex=False)
    .str.replace(',', '', regex=False)
    .str.strip()
)
data['Valor_USD'] = pd.to_numeric(data['Valor_USD'], errors='coerce')
data['Valor_USD'] = data['Valor_USD'].astype('int64')

#%%
print(data.info())

#%%
print(data.tail())

#%%
#Muestra si hay duplicados
#duplicados = data.duplicated()
#print(duplicados.sum())

#%%
#Evolución del valor total de importaciones (2018–2023)
valor_anual = data.groupby('Anios')['Valor_USD'].sum()
print(valor_anual)
#Grafica_1
plt.figure(figsize=(8,5))
valor_anual.plot(kind='bar', color='skyblue')
plt.title("Valor total de importaciones por año (USD)")
plt.xlabel("Año")
plt.ylabel("Valor CIF (USD)")
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

#%%
#Impacto de la pandemia (2020) en peso y valor
resumen_pandemia = data.groupby('Anios')[['Valor_USD', 'Peso_kg']].sum()
print(resumen_pandemia)
#Grafica_2
plt.figure(figsize=(10,5))
resumen_pandemia.plot(kind='line', marker='o')
plt.title("Impacto de la pandemia en las importaciones (valor y peso)")
plt.xlabel("Año")
plt.ylabel("Total")
plt.grid(True)
plt.tight_layout()
plt.show()

#%%
#Productos más importados por valor y peso
top_valor_v = data.groupby(['Codigo','Producto'])['Valor_USD'].sum().sort_values(ascending=False).head(10)
top_peso_p = data.groupby(['Codigo','Producto'])['Peso_kg'].sum().sort_values(ascending=False).head(10)
print(top_valor_v)
print(top_peso_p)
top_valor = data.groupby('Codigo')['Valor_USD'].sum().sort_values(ascending=False).head(10)
top_peso = data.groupby('Codigo')['Peso_kg'].sum().sort_values(ascending=False).head(10)

#Grafica_3
plt.figure(figsize=(10,4))
top_valor.plot(kind='bar', color='orange')
plt.title("Top 10 productos por valor CIF")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,4))
top_peso.plot(kind='bar', color='green')
plt.title("Top 10 productos por peso neto")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#%%
# Comparación del comportamiento del Dolar conversion a Peso
tasa_dolar = {
    2018: 2950, 2019: 3280, 2020: 3700,
    2021: 3760, 2022: 4020, 2023: 4100
}
print(tasa_dolar)

#%%
# Estimativo de cómo las variaciones del dólar afectaron el valor CIF.
data['Valor_COP'] = data.apply(lambda x: x['Valor_USD'] * tasa_dolar.get(x['Anios'], 1), axis=1)

valor_cop_anual = data.groupby('Anios')['Valor_COP'].sum()
valor_cop_anual.plot(kind='bar', figsize=(8,5), color='purple')
plt.title("Valor CIF ajustado por dólar (COP)")
plt.ylabel("Valor en COP")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#%%
# los 5 productos top frecuentemente mas importados
top_productos = data['Producto'].value_counts().head(5).index
# Filtrar la data
filtro_top = data[data['Producto'].isin(top_productos)].copy()
# Crear una nueva columna con nombres de productos más cortos (máximo 30 caracteres)
filtro_top['Producto_corto'] = filtro_top['Producto'].apply(lambda x: x[:30] + '...' if len(x) > 30 else x)

# Agrupar por año y producto reducido
tendencias = filtro_top.groupby(['Anios', 'Producto_corto'])['Valor_USD'].sum().unstack().fillna(0)

tendencias.plot(kind='line', figsize=(10,5), marker='o')
plt.title("Tendencia del valor CIF por producto (Top 5)")
plt.xlabel("Año")
plt.ylabel("Valor USD")
plt.grid(True)
plt.tight_layout()
plt.show()

#%%
#Productos importados todos los años
productos_constantes = data.groupby(["Codigo", "Producto"])['Anios'].nunique()
productos_seis_anios = productos_constantes[productos_constantes == 6]
print("Productos importados en todos los años (2018-2023):")
print(productos_seis_anios)

#%%
#Gráfica de torta: Participación Top 5 de producto por valor USD
participacion = data.groupby('Producto')['Valor_USD'].sum().sort_values(ascending=False).head(5)
# Acortar nombres de productos (ej: a 30 caracteres)
participacion.index = participacion.index.str.slice(0, 30) + '...'

# Gráfica de torta
plt.figure(figsize=(6,6))
participacion.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.ylabel('')
plt.title("Participación de productos más importados (USD)")
plt.tight_layout()
plt.show()


#%%
#¿Cuáles productos representan un mayor costo por unidad de peso?
data['costo_por_kg'] = data['Valor_USD'] / data['Peso_kg']
productos_costosos_1 = data.groupby(["Codigo", "Producto"])['costo_por_kg'].mean().sort_values(ascending=False).head(10)
productos_costosos = data.groupby("Codigo")['costo_por_kg'].mean().sort_values(ascending=False).head(10)
print("⚖️ Productos con mayor costo por kilogramo:")
print(productos_costosos_1)

# Visualización
productos_costosos.plot(kind='bar', figsize=(10,5), color='crimson')
plt.title("Top 10 productos con mayor costo por kg (USD/kg)")
plt.ylabel("USD por kg")
plt.xticks(rotation=90)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

#%%
#¿Se observa una tendencia de diversificación o concentración?
productos_por_anio = data.groupby('Anios')['Producto'].nunique()
print("📦 Número de productos únicos importados por año:")
print(productos_por_anio)

# Visualización
productos_por_anio.plot(kind='line', marker='o', figsize=(8,5), color='darkblue')
plt.title("Número de productos únicos importados por año")
plt.xlabel("Año")
plt.ylabel("Cantidad de productos únicos")
plt.grid(True)
plt.tight_layout()
plt.show()








"""
#%%
#. ¿Cuáles fueron los productos más importados por Colombia entre 2018 y 2023 según su valor USD?
top_productos_valor = data.groupby(["Codigo", "Producto"])["Valor_USD"].sum().sort_values(ascending=False).head(10)
print(top_productos_valor)

# %%
#Los 10 productos que tuvieron el mayor peso neto en las importaciones?
top_productos_peso = data.groupby(["Codigo", "Producto"])["Peso_kg"].sum().sort_values(ascending=False).head(10).round(1)
print(top_productos_peso)

# %%
#¿Cómo ha evolucionado el valor total de las importaciones Anios tras Anios?
valor_por_Anios_codigo = data.groupby(['Anios', 'Codigo'])['Valor_USD'].sum().reset_index()
print(valor_por_Anios_codigo)

# %%
#Evolucion del valor USD de producto filtrado por codigo
codigo = 102
filtro = valor_por_Anios_codigo[valor_por_Anios_codigo['Codigo'] == codigo]
# Graficar
plt.plot(filtro['Anios'], filtro['Valor_USD'], marker='o')
plt.title(f'Evolución del valor USD para el código {codigo}')
plt.xlabel('Años')
plt.ylabel('Valores USD')
plt.grid(True)
plt.show()

# %%
#¿Qué productos se importaron de manera constante durante los seis Anios?
productos_constantes = data.groupby(["Codigo","Producto"])["Anios"].nunique()
productos_6_Anios= productos_constantes[productos_constantes == 6]
print(productos_6_Anios)

#%%
#¿En qué año se registró el mayor volumen de importaciones en términos de peso y valor?
mayor_valor = data.groupby("Anios")["Valor_USD"].sum().idxmax()
mayor_peso = data.groupby("Anios")["Peso_kg"].sum().idxmax()
print(f"Año con mayor valor USD: {mayor_valor}")
print(f"Año con mayor peso neto: {mayor_peso}")


"""
