# Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Pandas to read_csv
air_quality = pd.read_csv('sp_air_quality.csv')
print(air_quality.head(3))

# Inputing NO2 median values by 'Station' sub-group.
NO2_dict = air_quality.groupby('Station')['NO2'].median().dropna().to_dict()
air_quality['NO2'] = air_quality['NO2'].fillna(air_quality['Station'].map(NO2_dict))
print(air_quality.isna().sum())

# Handling with outliers by 'Station' sub-group.
Q1 = air_quality.groupby('Station')['NO2'].transform(lambda x: x.quantile(0.25))
Q3 = air_quality.groupby('Station')['NO2'].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

air_quality = air_quality[(air_quality['NO2'] >= lower) & (air_quality['NO2'] <= upper)]
print(air_quality.head())

# Creating a new column 'Hour'
air_quality['Datetime'] = pd.to_datetime(air_quality['Datetime'])
air_quality['Hour'] = air_quality['Datetime'].dt.hour

# Dict 1 for a new table: region_list
stations = {
    'Station':['Araçatuba', 'Catanduva', 'Pico do Jaraguá', 'Ribeirão Preto','Araraquara', 'São José do Rio Preto', 
'Bauru', 'Jaú', 'Jundiaí', 'Marília', 'Paulínia', 'Piracicaba', 'Sorocaba', 'Tatuí', 'Campinas-Centro', 'Campinas-V.União', 'Campinas-Taquaral',
'Americana','Limeira','Santa Gertrudes', 'Carapicuíba', 'Diadema', 'Guarulhos-Paço Municipal', 'Guarulhos-Pimentas', 
'Mauá', 'Osasco', 'Perus', 'S.André-Capuava', 'S.Bernardo-Centro', 'S.Bernardo-Paulicéia', 'São Caetano do Sul', 'Taboão da Serra',
'Guaratinguetá', 'Jacareí', 'S.José Campos', 'S.José Campos-Jd.Satelite', 'S.José Campos-Vista Verde', 'Taubaté',
'Capão Redondo', 'Congonhas', 'Grajaú-Parelheiros', 'Interlagos', 'Santo Amaro', 'Cubatão-Centro', 'Cubatão-V.Parisi', 'Cubatão-Vale do Mogi', 
'Santos', 'Santos-Ponta da Praia', 'Cerqueira César', 'Ibirapuera', 'Marg.Tietê-Pte Remédios', 'Parque D.Pedro II', 'Rio Claro-Jd.Guanabara',
'N.Senhora do Ó', 'Santana', 'Itaim Paulista', 'Itaquera', 'Mooca']
}

# Dict 2 for a new table: region_list
region =  {
    'Interior': ['Bauru', 'Jaú', 'Jundiaí', 'Marília', 'Paulínia', 'Piracicaba', 'Sorocaba', 'Tatuí', 'Araraquara', 'São José do Rio Preto','Araçatuba', 'Catanduva', 'Ribeirão Preto', 'Rio Claro-Jd.Guanabara', 'Campinas-Centro', 'Campinas-V.União', 'Campinas-Taquaral','Americana','Limeira','Santa Gertrudes'],
    'Região Metropolitana': ['Carapicuíba', 'Diadema', 'Guarulhos-Paço Municipal', 'Guarulhos-Pimentas', 'Mauá', 'Osasco', 'Perus', 'S.André-Capuava', 'S.Bernardo-Centro', 'S.Bernardo-Paulicéia', 'São Caetano do Sul', 'Taboão da Serra', 'Pico do Jaraguá'], 
    'Vale do Paraíba': ['Guaratinguetá', 'Jacareí', 'S.José Campos', 'S.José Campos-Jd.Satelite', 'S.José Campos-Vista Verde', 'Taubaté'], 
    'Litoral': ['Cubatão-Centro', 'Cubatão-V.Parisi', 'Cubatão-Vale do Mogi', 'Santos', 'Santos-Ponta da Praia'], 
    'Capital': ['Cerqueira César', 'Ibirapuera', 'Marg.Tietê-Pte Remédios', 'Parque D.Pedro II','N.Senhora do Ó', 'Santana','Itaim Paulista', 'Itaquera', 'Mooca', 'Capão Redondo', 'Congonhas', 'Grajaú-Parelheiros', 'Interlagos', 'Santo Amaro']
}

# New DataFrame
region_list =pd.DataFrame(stations)
station_to_region = {station: reg for reg, stations in region.items() for station in stations}
region_list['Region'] = region_list['Station'].map(station_to_region)

# Final DataFrame
air_quality_merge = air_quality.merge(region_list, how='left', on='Station')

# Calculation NO2 for each Region using Pandas groupby
NO2_mean_per_region = air_quality_merge.groupby('Region')['NO2'].mean()
print(NO2_mean_per_region)

# Plotting using Matplotlib and Seaborn
sns.set_context('paper')
a = sns.relplot(x='Hour', y='NO2', data=air_quality_merge, kind='line', hue='Region')
a.fig.suptitle('NO2 (µg/m³) per hour in São Paulo')
a.set(xlabel= 'Hour', ylabel='Nitrogen dioxide (µg/m³)')
plt.xticks(range(24))
plt.show()