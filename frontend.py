import streamlit as st
import requests

st.title("SaúdeJá - Previsão de Faltas")
nome_paciente = st.text_input("Nome do Paciente")
cpf_paciente = st.text_input("CPF (apenas números)")
idade_paciente = st.number_input("Idade", min_value=0)
# Crie agora os campos para sexo, especialidade, distancia_km, etc... usando st.number_input
if st.button("Analisar Paciente"):
    # Preencha o resto deste dicionário com as variáveis que criou no Passo 3
    payload = {
        "nome": nome_paciente,
        "cpf": cpf_paciente,
        "idade": idade_paciente,
        "sexo": 0, # Substitua pela sua variável
        "especialidade": 0, # Substitua...
        "distancia_km": 10,
        "dias_entre_agendamento_consulta": 0,
        "historico_noshow": 0
    }
    
    # Bate na porta da sua API
    resposta = requests.post("http://127.0.0.1:8000/predict", json=payload)
    
    # Mostra a mensagem da IA no ecrã com uma caixa verde de sucesso!
    st.success(resposta.json()["recomendacao_secretaria"])