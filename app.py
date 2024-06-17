import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Lasso, Ridge, ElasticNet
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt

# URL do arquivo CSV no GitHub
url = 'https://raw.githubusercontent.com/David1r20/Produ-o-de-energia-el-trica/main/Power_data.csv'
data = pd.read_csv(url)

def main():
    st.title("Previsão de Produção de Energia Elétrica")
    st.write("""
    Este conjunto de dados contém dados operacionais de uma usina de energia, detalhando vários fatores ambientais e operacionais,
    juntamente com a produção líquida de energia elétrica por hora. Será analisado a influência das condições ambientais no
    desempenho da usina e pode ser usado para modelagem preditiva e estudos de otimização.
    
    **Características:**
    - Temperatura média: Temperatura ambiente média (em Celsius).
    - Vácuo de exaustão: Pressão de vácuo do vapor que sai da turbina (em cm Hg).
    - Pressão ambiente: Pressão ambiente (em milibares).
    - Umidade relativa: Umidade relativa (%).
    - Produção líquida de energia elétrica horária: Produção líquida de energia elétrica horária (em MW).
    
    **Uso:**
    Este conjunto de dados será usado para análise de regressão Lasso, Ridge e Elastic net.
    """)
    try:
        st.subheader("Dados do Dataset")
        st.write(data.head())

        # Definir variáveis independentes (X) e dependente (y)
        X = data[['Avg temperature', 'Exhaust vacuum', 'Ambient pressure', 'Relative humidity']]
        y = data['Net hourly electrical energy output']

        # Normalizar os dados
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Dividir os dados em conjuntos de treino e teste (80% treino, 20% teste)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.15, random_state=45)

        # Definir os parâmetros para a busca por grid
        param_grid = {
            'alpha': [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
        }

        # Configurar modelos Lasso, Ridge e ElasticNet
        lasso = Lasso()
        ridge = Ridge()
        elastic = ElasticNet()

        # Realizar busca por grid para Lasso
        grid_search_lasso = GridSearchCV(estimator=lasso, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search_lasso.fit(X_train, y_train)
        best_alpha_lasso = grid_search_lasso.best_params_['alpha']
        best_model_lasso = grid_search_lasso.best_estimator_

        # Realizar busca por grid para Ridge
        grid_search_ridge = GridSearchCV(estimator=ridge, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search_ridge.fit(X_train, y_train)
        best_alpha_ridge = grid_search_ridge.best_params_['alpha']
        best_model_ridge = grid_search_ridge.best_estimator_

        # Realizar busca por grid para ElasticNet
        grid_search_elastic = GridSearchCV(estimator=elastic, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search_elastic.fit(X_train, y_train)
        best_alpha_elastic = grid_search_elastic.best_params_['alpha']
        best_model_elastic = grid_search_elastic.best_estimator_

        # Avaliar os modelos ajustados com os melhores parâmetros
        y_pred_lr = best_model_lasso.predict(X_test)
        y_pred_ridge = best_model_ridge.predict(X_test)
        y_pred_elastic = best_model_elastic.predict(X_test)

        mse_lr = mean_squared_error(y_test, y_pred_lr)
        mse_ridge = mean_squared_error(y_test, y_pred_ridge)
        mse_elastic = mean_squared_error(y_test, y_pred_elastic)

        r2_lr = r2_score(y_test, y_pred_lr)
        r2_ridge = r2_score(y_test, y_pred_ridge)
        r2_elastic = r2_score(y_test, y_pred_elastic)

        st.subheader("Avaliação dos Modelos Ajustados")
        st.write(f"**Modelo Lasso Regression (Alpha: {best_alpha_lasso}):**")
        st.write(f"   Mean Squared Error (MSE): {mse_lr:.2f}")
        st.write(f"   R-squared (R2): {r2_lr:.2f}")

        st.write(f"**Modelo Ridge Regression (Alpha: {best_alpha_ridge}):**")
        st.write(f"   Mean Squared Error (MSE): {mse_ridge:.2f}")
        st.write(f"   R-squared (R2): {r2_ridge:.2f}")

        st.write(f"**Modelo Elastic Net Regression (Alpha: {best_alpha_elastic}):**")
        st.write(f"   Mean Squared Error (MSE): {mse_elastic:.2f}")
        st.write(f"   R-squared (R2): {r2_elastic:.2f}")
        
        # Widgets para entrada de parâmetros de previsão
        st.sidebar.header("Parâmetros de Previsão")
        temperature = st.sidebar.slider("Temperatura Média (°C)", min_value=0, max_value=40, value=25)
        vacuum = st.sidebar.slider("Pressão de Vácuo (cm Hg)", min_value=25, max_value=80, value=55)
        pressure = st.sidebar.slider("Pressão Ambiente (mbar)", min_value=900, max_value=1100, value=1010)
        humidity = st.sidebar.slider("Umidade Relativa (%)", min_value=0, max_value=100, value=50)

        # Criar um dataframe com os dados de entrada
        input_data = pd.DataFrame({
            'Avg temperature': [temperature],
            'Exhaust vacuum': [vacuum],
            'Ambient pressure': [pressure],
            'Relative humidity': [humidity]
        })

        # Normalizar os dados de entrada
        input_data_scaled = scaler.transform(input_data)

        # Fazer previsões com os modelos ajustados com os melhores parâmetros
        predicted_energy_output_lasso = best_model_lasso.predict(input_data_scaled)[0]
        predicted_energy_output_ridge = best_model_ridge.predict(input_data_scaled)[0]
        predicted_energy_output_elastic = best_model_elastic.predict(input_data_scaled)[0]

        st.subheader("Previsões de Produção de Energia")
        st.markdown(f"### **Modelo Lasso Regression**", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>Previsão Lasso: <span style='color: red;'>{predicted_energy_output_lasso:.2f} MW</span></h1>", unsafe_allow_html=True)
        
        st.markdown(f"### **Modelo Ridge Regression**", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>Previsão Ridge: <span style='color: red;'>{predicted_energy_output_ridge:.2f} MW</span></h1>", unsafe_allow_html=True)

        st.markdown(f"### **Modelo Elastic Net Regression**", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>Previsão Elastic Net: <span style='color: red;'>{predicted_energy_output_elastic:.2f} MW</span></h1>", unsafe_allow_html=True)
        st.write("""





            
        """)
        # Previsão mensal com valores aleatórios
        st.subheader("Previsão Mensal com Valores Aleatórios")
        days = np.arange(1, 31)
        temperatures = np.random.uniform(temperature - 5, temperature + 5, size=30)
        vacuums = np.random.uniform(vacuum - 10, vacuum + 10, size=30)
        pressures = np.random.uniform(pressure - 20, pressure + 20, size=30)
        humidities = np.random.uniform(humidity - 20, humidity + 20, size=30)

        monthly_data = pd.DataFrame({
            'Avg temperature': temperatures,
            'Exhaust vacuum': vacuums,
            'Ambient pressure': pressures,
            'Relative humidity': humidities
        })

        monthly_data_scaled = scaler.transform(monthly_data)

        predictions_lasso = lasso.predict(monthly_data_scaled)
        predictions_ridge = ridge.predict(monthly_data_scaled)
        predictions_elastic = elastic.predict(monthly_data_scaled)

        fig, ax = plt.subplots()
        ax.plot(days, predictions_lasso, label='Lasso Regression', color='blue')
        ax.plot(days, predictions_ridge, label='Ridge Regression', color='red')
        ax.plot(days, predictions_elastic, label='Elastic Net Regression', color='grey')
        ax.set_xlabel('Dia do Mês')
        ax.set_ylabel('Produção de Energia (MW)')
        ax.set_title('Previsão de Produção de Energia Elétrica Mensal')
        ax.legend()
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")

if __name__ == "__main__":
    main()
