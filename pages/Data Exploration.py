import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Data Exploration",
)
st.sidebar.title("Data Exploration")

# load dataset
df = pd.read_csv('Global_Dataset_of_Inflation_2.csv', encoding='latin1')

# membuat visualisasi untuk Rata-Rata Tingkat Inflasi per Tahun
columns_to_plot = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
columns_to_plot_existing = [col for col in columns_to_plot if col in df.columns]

df_mean = df[columns_to_plot_existing].mean().reset_index()
df_mean.columns = ['Year', 'Average Inflation Rate']

st.title('Rata-Rata Tingkat Inflasi per Tahun')
st.plotly_chart(px.bar(df_mean, x='Year', y='Average Inflation Rate', title='Rata-Rata Tingkat Inflasi per Tahun'))

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
