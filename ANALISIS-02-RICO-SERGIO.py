#%%
from itertools import count
import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt

#Tema para gráfica
sns.set_theme(style="whitegrid")
# %%
# lectura de datos en variable sldb
sldb = pd.read_csv('synergy_logistics_database.csv')

# %%
#calculo de ingreso total de todo el df
ingreso_total = sldb.sum()['total_value']
#print('ingreso Total: {}'.format(ingreso_total))

# %%
#=========================================== OP 1 ==========================================

#DF agrupado por dirección, origen y destino con la columna de valor toal, cuenta y suma 
# para presentar las 10 rutas más demandadas
rutas_mas_demandadas = sldb.groupby(['direction', 'origin', 'destination'])['total_value']\
                .agg({'count', 'sum'})\
                .rename(columns={'count': 'frecuencia', 'sum': 'valor_acumulado'})\
                .sort_values(by=['frecuencia'], ascending=False).reset_index()

# Calculo del ingreso de las rutas más demandadas 
ingreso_rutas_mas_demandadas = rutas_mas_demandadas[:10].sum()['valor_acumulado']

# Top 10 rutas más demandadas
print('OPCIÓN 1:')
print(" > Top 10 rutas más demandadas: \n{}\n".format(rutas_mas_demandadas.head(10)))

# Porcentaje respecto al total considerando las 10 rutas más usadas
porcentaje_irutas_itotal = (ingreso_rutas_mas_demandadas / ingreso_total) * 100
print('Porcentaje de ingreso considerando las rutas más demandadas: {}%\n\n'\
    .format(round(porcentaje_irutas_itotal,2)))


# %%
print('OPCIÓN 2:')
#=========================================== OP 2 ==========================================
transportes_utilizados = sldb.groupby(['transport_mode'])\
                        ['total_value'].agg({'count', 'sum'})\
                        .rename(columns = {'count': 'frecuencia_uso', 'sum': 'ingreso'})\
                        .sort_values(by=['ingreso'], ascending=False).reset_index()

# Nueva columna con el porcetaje de oportacion al ingreso total
transportes_utilizados['Porcentaje_aportado'] = (transportes_utilizados['ingreso'] / ingreso_total)*100
# Datos según transporte utilizado 
print(' > Métricas según el transporte utilizados:\n\n{}\n'.format(transportes_utilizados))

# Porcentaje de ingreso con los 3 transportes que más aportan
transporte_aporte = transportes_utilizados[:3]['Porcentaje_aportado'].sum()
print('Considerando los 3 medios más importantes para Synergy Logistics se considera el {}%'.format(round(transporte_aporte, 2)))

# %%
# Gráficos de transporte vs porcentaje aportado al ingreso total 
transporte_vs_aporte = sns.barplot(x="transport_mode", y="Porcentaje_aportado", data=transportes_utilizados)
plt.show()
# %%
#=========================================== OP 3 ==========================================
paises_aporte = sldb.groupby(['origin'])\
                ['total_value'].agg({'sum'})\
                .rename(columns = {'sum':'total'})\
                .sort_values(by=['total'], ascending=False).reset_index()

paises_aporte['porcentaje'] = round((paises_aporte['total']/ingreso_total)*100, 2)
paises_aporte['p_acumulado'] = paises_aporte['porcentaje'].cumsum()

# %%
print('OPCIÓN 3:')
print(' > Rutas que generan el 80% de los ingresos: \n{}\n'.format(paises_aporte[:9]))

porcentaje_paises_aporte = ((paises_aporte[:9].sum()['total'])/ingreso_total)*100

print('Porcentaje de ingreso considerando el 80% del valor de las importaciones/exportaciones: {}%'\
    .format(round(porcentaje_paises_aporte, 2)))
