import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Prediction",
)

st.write("Anda telah masuk", st.session_state["my_input"])

# load dataset
df = pd.read_csv('Global_Dataset_of_Inflation_2.csv')

columns_to_plot = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
columns_to_plot_existing = [col for col in columns_to_plot if col in df.columns]

df_mean = df[columns_to_plot_existing].mean().reset_index()
df_mean.columns = ['Year', 'Average Inflation Rate']

# Plot rata-rata tingkat inflasi per tahun
fig1 = px.bar(df_mean, x='Year', y='Average Inflation Rate', title='Rata-Rata Tingkat Inflasi per Tahun')
fig1.update_xaxes(title='Tahun')
fig1.update_yaxes(title='Tingkat Inflasi')

# Plot tingkat inflasi berdasarkan benua
fig2 = px.line(df, x='year', y=columns_to_plot_existing, 
             labels={'variable': 'Benua', 'value': 'Tingkat Inflasi dalam %', 'year': 'Tahun'},
             title='Tingkat Inflasi Berdasarkan Benua',
             template='plotly',
             markers=True)

# Plot penurunan inflasi di tahun 2022
final = df[['country', 'difference', 'continent']][df['2022'] > 100]
fig3 = px.bar(final, x='country', y='difference', color='continent', 
            labels={'continent': 'Benua', 'difference': 'Penurunan Tingkat Inflasi', 'country': 'Negara'}, 
            title='Penurunan Inflasi di Tahun 2022', 
            template='plotly')

# Plot top-10 negara dengan tingkat inflasi yang meningkat
inflation = df[['country', 'difference', 'continent']][df['2022'] > 100].nlargest(10, 'difference')
fig4 = px.bar(inflation, x='country', y='difference', color='continent',
            title='Top-10 Negara dengan Tingkat Inflasi yang Meningkat',
            labels={'continent': 'Benua', 'difference': 'Increasing Rate'})

# Menampilkan plot di Streamlit
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)
