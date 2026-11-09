import streamlit as st
import requests

st.set_page_config(page_title="SaúdeJá", page_icon="🏥", layout="centered")

st.title("🏥 SaúdeJá - Previsão de Faltas")
st.markdown("Preencha os dados do agendamento para analisar o risco de no-show.")

# Criando colunas para deixar o layout mais bonito e organizado
col1, col2 = st.columns(2)

with col1:
    nome_paciente = st.text_input("Nome do Paciente")
    cpf_paciente = st.text_input("CPF (apenas números)", max_chars=11)
    idade_paciente = st.number_input("Idade", min_value=0, max_value=120, value=0)
    sexo_paciente = st.selectbox("Sexo", options=[0, 1], format_func=lambda x: "Feminino" if x == 0 else "Masculino")

with col2:
    especialidade = st.selectbox(
        "Especialidade", 
        options=[0, 1, 2, 3, 4, 5, 6], 
        format_func=lambda x: ["Cardiologia", "Clínica Geral", "Dermatologia", "Ginecologia", "Oftalmologia", "Ortopedia", "Pediatria"][x]
    )
    distancia_km = st.number_input("Distância até a clínica (km)", min_value=0.0, max_value=200.0, value=10.0, step=0.5)
    dias_espera = st.number_input("Dias de espera (agendamento até consulta)", min_value=0, max_value=365, value=5)
    historico_noshow = st.number_input("Histórico de Faltas (Quantidade)", min_value=0, max_value=50, value=0)

st.markdown("---")

if st.button("Analisar Paciente", type="primary", use_container_width=True):
    payload = {
        "nome": nome_paciente,
        "cpf": cpf_paciente,
        "idade": idade_paciente,
        "sexo": sexo_paciente, 
        "especialidade": especialidade, 
        "distancia_km": distancia_km,
        "dias_entre_agendamento_consulta": dias_espera,
        "historico_noshow": historico_noshow
    }
    
    url_api = "https://ai-factory-saudeja.onrender.com/predict"
    
    try:
        with st.spinner('A analisar o risco e gerar recomendação...'):
            resposta = requests.post(url_api, json=payload)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                st.success("Análise concluída com sucesso!")
                
                # Exibe os resultados em caixas de destaque
                res_col1, res_col2 = st.columns(2)
                res_col1.metric("Risco Predito", f"{dados.get('risco_predito', 'N/A')}%")
                res_col2.metric("Paciente", dados.get('paciente', 'N/A'))
                
                st.info(f"**Recomendação para a Secretária:**\n\n{dados.get('recomendacao_secretaria', 'Erro ao carregar recomendação.')}")
                
            else:
                st.error(f"Erro na API (Status {resposta.status_code}): Servidor ainda reiniciando ou falha na chave.")
                
    except requests.exceptions.JSONDecodeError:
        st.error("Erro de leitura. O servidor no Render ainda está reiniciando, tente novamente em 1 minuto.")
    except requests.exceptions.RequestException as e:
        st.error(f"Falha de conexão com a API: {e}")