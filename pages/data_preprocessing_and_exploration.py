import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# load dataset
df = pd.read_csv('Global_Dataset_of_Inflation.csv', encoding='latin1')

df.head()


# memilih variabel yang dibutuhkan 
df = df[['Country Code', #'IMF Country Code', 
         'Country', 'Indicator Type',
       #'Series Name', '1970', '1971', '1972', '1973', '1974', '1975', '1976',
       #'1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985',
       #'1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994',
       #'1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
       #'2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
       #'2013', '2014', '2015', 
       '2016', '2017', '2018', '2019', '2020', '2021',
       '2022', #'Note', 'Unnamed: 59', 'Unnamed: 60', 'Unnamed: 61','Unnamed: 62', 'Unnamed: 63'
       ]].copy()

checking = []
def check(df):
    for col in df.columns:
        dtypes = df[col].dtypes
        
        checking.append([col, dtypes])
    check_values = pd.DataFrame(checking)
    check_values.columns = ['col', 'dtypes']
    return check_values
check(df)

# membuat variabel menajadi huruf kecil semua
df.columns = df.columns.str.lower()

# menghapus data yg duplikat
df = df[~df.duplicated()]
df = df[~df.duplicated(subset=['country'])].reset_index(drop=True)

# membuat visualisasi untuk Rata-Rata Tingkat Inflasi per Tahun
columns_to_plot = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
columns_to_plot_existing = [col for col in columns_to_plot if col in df.columns]

df_mean = df[columns_to_plot_existing].mean().reset_index()
df_mean.columns = ['Year', 'Average Inflation Rate']

st.title('Rata-Rata Tingkat Inflasi per Tahun')
st.plotly_chart(px.bar(df_mean, x='Year', y='Average Inflation Rate', title='Rata-Rata Tingkat Inflasi per Tahun'))


# memilih tahun yang memiliki nilai inflasi lebih dari 100
st.title('Data dengan Inflasi Lebih dari 100')
st.write(df[(df['2016'] > 100) | (df['2017'] > 100) | (df['2018'] > 100) | (df['2019'] > 100) | (df['2020'] > 100) | (df['2021'] > 100) | (df['2022'] > 100)])

# memilih negara yg memiliki nilai inflasi kurang dari 1000 pada tahun 2018 & 2020
st.title('Data dengan Inflasi Kurang dari 1000 pada Tahun 2018 & 2020')
df_filtered = df[(df['2018'] < 1000) & (df['2020'] < 1000)]
st.write(df_filtered)

# menambah kolom baru yaitu continent untuk membuat grup berdasarkan benua
url = 'https://statisticstimes.com/geography/countries-by-continents.php'

html = pd.read_html(url, match = 'Continent')

df1 = html[0]
df1.rename(columns={'ISO-alpha3 Code' : 'country code'}, inplace=True)

df2 = pd.merge(df_filtered, df1, on='country code', how='inner')

df = df2[['country code', 'country', 'Continent', 'indicator type', '2016', '2017','2018', '2019', '2020', '2021', '2022', 'Region 1']].copy()

df.columns = df.columns.str.lower()

continent = df.groupby('continent')['2016', '2017', '2018', '2019', '2020', '2021', '2022'].mean()\
.reset_index()
continent1 = continent.T
continent1.columns = continent['continent'].values
continent1.index.name = 'year'
continent1.drop('continent', inplace=True)
continent1.reset_index(inplace=True)

st.title('Tingkat Inflasi Berdasarkan Benua')
fig = px.line(continent1, x='year', y=continent1.columns[0:], 
             labels = {'variable' : 'Benua','value' : 'tingkat inflasi dalam %', 'year' : 'Tahun'},
             title = 'Tingkat Inflasi Berdasarkan Benua', 
             template = 'plotly',
              markers=True)
st.plotly_chart(fig)

df['difference'] = df.apply(lambda x: x['2022'] - x['2021'], axis=1)

def checking (var): 
    if var < 0: 
        return 'deflation'
    else:
        return 'Inflation'
    
df['inflation_category'] = df['difference'].apply(checking)

deflation = df[df['inflation_category'] == 'deflation']
deflation_agg = deflation.groupby('continent')['difference'].agg(['count', 'mean']).reset_index()

final = deflation.sort_values(by='difference', ascending=False).head(11)
final['difference'] = final['difference'] * -1

st.title('Penurunan Inflasi di Tahun 2022')
fig = px.bar(final, x='country', y='difference', color='continent', 
            labels={'continent' : 'Benua', 'difference': 'Penurunan Tingkat Inflasi', 'country': 'Negara'}, 
            title='Penurunan Inflasi di Tahun 2022', 
            template='plotly')
st.plotly_chart(fig)

inflation = df[df['inflation_category'] == 'Inflation'].sort_values(by=['difference'], ascending=False).head(10)

st.title('Top-10 Negara dengan Tingkat Inflasi yang Meningkat')
fig = px.bar(inflation, x='country', y='difference', color='continent',
            title = 'Top-10 Negara dengan Tingkat Inflasi yang Meningkat',
            labels = {'continent' : 'Benua', 'difference' : 'Tingkat Inflasi yang Meningkat'})
st.plotly_chart(fig)
