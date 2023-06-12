import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import plotly.express as px

st.set_page_config(
    page_title="Inflation Prediction",
)

# load dataset
df = pd.read_csv('Global_Dataset_of_Inflation_2.csv')

# Memilih kolom yang diperlukan untuk prediksi
features = ['2016', '2017', '2018', '2019', '2020', '2021']
target = '2022'

# Menghapus baris yang memiliki nilai kosong
df_clean = df.dropna(subset=features + [target])

# Memisahkan data menjadi data training dan data testing
X = df_clean[features]
y = df_clean[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Membuat model Random Forest Regression
model = RandomForestRegressor()

# Melakukan fitting model pada data training
model.fit(X_train, y_train)

# Memprediksi tingkat inflasi untuk tahun berikutnya menggunakan data testing
prediksi = model.predict(X_test)

# Menghitung mean squared error (MSE) sebagai evaluasi model
mse = mean_squared_error(y_test, prediksi)
print(f"Mean Squared Error: {mse}")

# Membuat dataframe untuk hasil prediksi
df_prediksi = pd.DataFrame({'Aktual': y_test.values, 'Prediksi': prediksi})

# Visualisasi hasil prediksi menggunakan Plotly
fig = px.line(df_prediksi, title='Prediksi Tingkat Inflasi')
fig.update_layout(xaxis_title='Index Data', yaxis_title='Tingkat Inflasi')

# Menampilkan plot di Streamlit
st.plotly_chart(fig)
