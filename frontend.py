import streamlit as st
import requests

st.title("SaúdeJá - Previsão de Faltas")

nome_paciente = st.text_input("Nome do Paciente")
cpf_paciente = st.text_input("CPF (apenas números)")
idade_paciente = st.number_input("Idade", min_value=0, max_value=120, value=40)

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
        
        if resposta.status_code == 200:
            dados = resposta.json()
            st.success(dados.get("recomendacao_secretaria", "Erro ao carregar recomendação."))
        else:
            st.error(f"Erro na API (Status {resposta.status_code}): Servidor ainda reiniciando ou falha na chave.")
            
    except requests.exceptions.JSONDecodeError:
        st.error("Erro de leitura. O servidor no Render ainda está reiniciando, tente novamente em 1 minuto.")
    except requests.exceptions.RequestException as e:
        st.error(f"Falha de conexão com a API: {e}")