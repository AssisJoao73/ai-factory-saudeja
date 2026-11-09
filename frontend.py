import streamlit as st
import requests

st.title("SaúdeJá - Previsão de Faltas")
nome_paciente = st.text_input("Nome do Paciente")
cpf_paciente = st.text_input("CPF (apenas números)")
idade_paciente = st.number_input("Idade", min_value=0)
# Crie agora os campos para sexo, especialidade, distancia_km, etc... usando st.number_input
if st.button("Analisar Paciente"):
    payload = {
        "nome": nome_paciente,
        "cpf": cpf_paciente,
        "idade": idade_paciente,
        "sexo": 0, 
        "especialidade": 0, 
        "distancia_km": 10,
        "dias_entre_agendamento_consulta": 0,
        "historico_noshow": 0
    }
    
    url_api = "https://ai-factory-saudeja.onrender.com/predict"
    
    try:
        resposta = requests.post(url_api, json=payload)
        
        # Verifica se a API devolveu sucesso (200 OK)
        if resposta.status_code == 200:
            dados = resposta.json()
            st.success(dados["recomendacao_secretaria"])
        else:
            st.error(f"Erro na API (Status {resposta.status_code}): {resposta.text}")
            
    except requests.exceptions.RequestException as e:
         st.error(f"Falha de conexão com a API: {e}")