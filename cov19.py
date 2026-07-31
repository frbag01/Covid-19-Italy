#1. L'Andamento Nazionale (Rolling Average):

#Task: Crea un grafico a linee dei nuovi casi giornalieri a livello nazionale 


df = pd.read_csv('covid19_italy_region.csv', sep=';')
df=df.dropna(how='all')

casi_giornalieri=df.groupby('Date')['NewPositiveCases'].sum()
# Convert the index to datetime objects for proper chronological sorting
casi_giornalieri.index = pd.to_datetime(casi_giornalieri.index, format='%d/%m/%Y %H:%M')
casi_giornalieri = casi_giornalieri.sort_index()
casi_giornalieri.plot(figsize=(12, 6), title='Nuovi casi giornalieri di COVID-19 in Italia')
plt.ylabel('Nuovi casi giornalieri')
plt.xlabel('Data')
plt.show()


#2. Confronto tra Regioni (Growth Rate):

#Task: Scegli le 5 regioni più colpite e confronta la loro curva di crescita logaritmica. Quale regione ha mostrato la salita più ripida?


df = pd.read_csv('covid19_italy_region.csv', sep=';')
df=df.dropna(how='all')

# First, sort the DataFrame by 'TotalPositiveCases' in descending order
regcas_sorted = df[['RegionName', 'TotalPositiveCases']].sort_values(by='TotalPositiveCases', ascending=False)
top5 = regcas_sorted.drop_duplicates(subset=['RegionName']).head(5)
top5_region_names = top5['RegionName'].tolist()
top5_region_names

for i in top5_region_names:
  df_filtered = df[df['RegionName'] == i]
  casi_giornalieri=df_filtered.groupby('Date')['NewPositiveCases'].sum()
  # Convert the index to datetime objects for proper chronological sorting
  casi_giornalieri.index = pd.to_datetime(casi_giornalieri.index, format='%d/%m/%Y %H:%M')
  casi_giornalieri = casi_giornalieri.sort_index()
  casi_giornalieri.plot(figsize=(12, 6), logy=True, title=f'Nuovi casi giornalieri in scala log di COVID-19 in {i}')
  plt.ylabel('Nuovi casi giornalieri')
  plt.xlabel('Data')
  plt.show()


#3.Heatmap Temporale:

#Task: Crea una barplot che mostri i giorni della settimana sull'asse X e i mesi, sull'asse Y il numero di nuovi casi. Esiste un "effetto lunedì" nel reporting dei dati?



df = pd.read_csv('covid19_italy_region.csv', sep=';')
df=df.dropna(how='all')


casi_giornalieri=df.groupby('Date')['NewPositiveCases'].sum()
casi_giornalieri.index = pd.to_datetime(casi_giornalieri.index, format='%d/%m/%Y %H:%M')
casi_giornalieri = casi_giornalieri.sort_index()

casi_giornalieri = casi_giornalieri.reset_index()

casi_giornalieri['day']=casi_giornalieri['Date'].dt.day_name()
casi_giornalieri['month']=casi_giornalieri['Date'].dt.month # Get month as integer

# Define the desired order for days of the week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# Convert 'day' column to a categorical type with the specified order
casi_giornalieri['day'] = pd.Categorical(casi_giornalieri['day'], categories=day_order, ordered=True)

# Group by the ordered 'day' and 'month'
casi=casi_giornalieri.groupby(['day','month'])['NewPositiveCases'].sum().reset_index()

plt.figure(figsize=(14, 7))
sns.barplot(data=casi, x='month', y='NewPositiveCases', hue='day', palette='viridis')
plt.xlabel('Month')
plt.ylabel('Total New Positive Cases')
plt.title('Total New Positive Cases per Month by Day of the Week')
plt.xticks(rotation=45)
plt.legend(title='Day of Week', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


