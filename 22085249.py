import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as stats
import textwrap

def executing_data(data, indicator_name):
    dt = pd.read_csv(data, skiprows=3)
    countries = ['India', 'United Kingdom',
                 'China', 'Pakistan', 'Brazil', 'Australia']
    data = dt[(dt['Indicator Name'] == indicator_name)
              & (dt['Country Name'].isin(countries))]
    data_dff = data.drop(['Country Code', 'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
                          '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984',
                          '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000',
                          '2001', '2002', '2003', '2004', '2005', '2020', '2021', '2022', 'Unnamed: 67'], axis=1).reset_index(drop=True)
    data_df = data_dff.transpose()
    data_df.columns = data_df.iloc[0]
    data_df = data_df.iloc[1:]
    data_df.index = pd.to_numeric(data_df.index)
    data_df['Years'] = data_df.index
    return data_dff, data_df


def dataframe(df):
    df = df[['Country Name', '2019']]
    return df


def merge_df(d1, d2, d3, d4):
    mer_1 = pd.merge(d1, d2, on='Country Name', how='outer')
    mer_2 = pd.merge(mer_1, d3, on='Country Name', how='outer')
    mer_3 = pd.merge(mer_2, d4, on='Country Name', how='outer')
    mer_3 = mer_3.reset_index(drop=True)
    return mer_3

# Read and process data for different indicators
population, po_t = executing_data('data.csv', 'Population growth (annual %)')
co2emission, co2_t = executing_data('data.csv', 'CO2 emissions (kt)')
agricultural, ag_t = executing_data(
    'data.csv', 'Agricultural land (% of land area)')
agri_forest_fishing, aff_t = executing_data(
    'data.csv', 'Agriculture, forestry, and fishing, value added (% of GDP)')

# Slice and rename columns for better readability
po_cor = dataframe(population).rename(columns={'2019': 'Population growth'})
co2_cor = dataframe(co2emission).rename(columns={'2019': 'CO2_emission'})
ag_cor = dataframe(agricultural).rename(columns={'2019': 'Agricultural land'})
aff_cor = dataframe(agri_forest_fishing).rename(
    columns={'2019': 'Agri,Forestry & Fishing'})

# Merge the DataFrames for analysis
hm = merge_df(po_cor, co2_cor, ag_cor, aff_cor)

# Create subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(
    16, 12), gridspec_kw={'hspace': 0.5}, facecolor='gray')
fig.patch.set_facecolor('gray')

# Title for the entire dashboard
fig.suptitle('         Environmental and Agricultural Indicators ', fontsize=25, color='white')

# Plot a line chart for population growth over the years
for country in ['United Kingdom', 'India', 'China', 'Pakistan', 'Brazil', 'Australia']:
    sns.lineplot(x=po_t[country].index, y=po_t[country],
                 ax=axes[0, 0], marker='o', label=country)

axes[0, 0].legend(loc='upper right', fontsize='5', labelspacing=1)
axes[0, 0].set_title('Population growth (annual %)')
axes[0, 0].set_xlabel("Years")
axes[0, 0].set_ylabel('Total(%)')

# Plot a bar chart for CO2 emissions over the years
co2_t.plot(kind='bar', ax=axes[0, 1],
           xlabel='Years', ylabel='Kg per hectare', rot=0)
axes[0, 1].legend(loc='upper left', fontsize='5', labelspacing=1)
axes[0, 1].set_title('CO2 emissions (kt)')

# Histogram for Agricultural land from 2006-2019
axes[1, 0].hist(ag_t['United Kingdom'], bins='auto',
                alpha=0.7, color='green', edgecolor='black')
axes[1, 0].grid(True)
axes[1, 0].set_title("Agricultural land from 2006-2019")
axes[1, 0].set_xlabel("United Kingdom Agri Land Area(sq)m")
axes[1, 0].set_ylabel('Frequency')

# Boxplot for Agriculture, forestry, and fishing, value added (% of GDP)
sns.boxplot(data=agri_forest_fishing, ax=axes[1, 1], palette='Set3')
axes[1, 1].set_title(
    'Agriculture, forestry, and fishing, value added (% of GDP)')

# Rotate x-axis labels for better readability
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45)
axes[1, 1].set_xlabel('Years')
axes[1, 1].set_ylabel('GDP Growth')

# Adding a information to the dashboard
report_text = """
    - Population emissions are shown for the years 2006 
      through 2019. Our goal is to offer important insights 
      into the intricate linkages that exist between the acts 
      of humans and climate change by examining the 
      patterns and correlations among different indicators.
      
    - The High Co2 emission due to human activity, such as 
      burning fossil fuels, deforestation, and cement 
      manufacturing, is carbon dioxide, an odorless and 
      colorless gas. Since the industrial revolution, the 
      amount of CO2 in the Earth's atmosphere has 
      increased by 43%, mostly as a result of burning fossil 
      fuels. It gets harder for Earth to keep a steady 
      temperature as more CO2 is absorbed by the planet.
      Based on the available statistics, India's carbon 
      dioxide emissions rose from 1.3 (Gt) in 2006 to 2.4 Gt
      in 2019. In terms of global rankings, India's CO2 
      emissions rose from the 20th to the 22nd position.
      
    - The skewness for agricultural land in the UK is 
      negative, it means that the data distribution is leftskewed.
      Since the data relates to agricultural land in 
      the United Kingdom, negative skewness may indicate 
      that over time, there have been more occurrences of 
      above-average than below-average values for 
      agricultural land area. This could suggest that 
      agricultural land area is rather stable, with 
      fluctuations leaning more toward the higher end of 
      spectrum.
      
    - This measure shows what proportion of a nation's 
      GDP comes from the value added that comes from the 
      fisheries, forestry, and agriculture industries put 
      together comprises tasks associated with tilling land, 
      growing crops, and rearing animals. High percentage 
      nations could be highly dependent on traditional 
      agriculture and the natural resource sectors. Pakistan 
      is the nation with the greatest total values when the 
      "Agriculture, forestry, and fishing, value added (%) of 
      GDP)" for the chosen countries is analyzed.
    
    -If population growth raises the demand for 
     agricultural goods and, in turn, increases the amount 
     of land used for agriculture then there may be a 
     positive link in this case. A positive link could imply 
     that nations with larger CO2 emissions are typically 
     those with more agricultural operations, which need 
     more land.
"""

# Add report text to the top-right corner of the last subplot
axes[1, 1].text(1.05, 1.5, report_text, transform=axes[1, 1].transAxes, fontsize=10,
                verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

# Add your name and roll number to the bottom-right corner
fig.text(0.98, 0.02, 'Barath | Roll No: 22085249', color='white', fontsize=25, ha='right')

# Adjust layout to prevent clipping of labels
plt.tight_layout()

# Save the figure (optional)
plt.savefig("dashboard.png", dpi=300)

