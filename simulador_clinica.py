import requests
import pandas as pd
import time

# O endereço público da sua API no Render
API_URL = "https://ai-factory-saudeja.onrender.com/predict"

# Simulando dados extraídos do banco de dados da clínica para as consultas de amanhã
pacientes_amanha = [
    {"id_paciente": "João Silva", "idade": 25, "sexo": 1, "especialidade": 1, "distancia_km": 15.3, "dias_entre_agendamento_consulta": 45, "historico_noshow": 3},
    {"id_paciente": "Maria Souza", "idade": 60, "sexo": 0, "especialidade": 3, "distancia_km": 2.1, "dias_entre_agendamento_consulta": 2, "historico_noshow": 0},
    {"id_paciente": "Carlos Gomes", "idade": 19, "sexo": 1, "especialidade": 2, "distancia_km": 25.0, "dias_entre_agendamento_consulta": 60, "historico_noshow": 1},
    {"id_paciente": "Ana Costa", "idade": 45, "sexo": 0, "especialidade": 1, "distancia_km": 5.5, "dias_entre_agendamento_consulta": 10, "historico_noshow": 0},
    {"id_paciente": "Lucas Pereira", "idade": 32, "sexo": 1, "especialidade": 3, "distancia_km": 8.0, "dias_entre_agendamento_consulta": 5, "historico_noshow": 1}
]

resultados = []

print("Iniciando varredura de risco para os pacientes de amanhã...\n")

for p in pacientes_amanha:
    # Removemos o nome/id antes de enviar para a API (mantendo o anonimato/LGPD no tráfego)
    payload = {k: v for k, v in p.items() if k != "id_paciente"}
    
    try:
        # Dispara os dados para a nuvem
        resposta = requests.post(API_URL, json=payload)
        resposta.raise_for_status() 
        
        dados_api = resposta.json()
        
        # Junta a resposta da IA com o nome do paciente
        resultados.append({
            "Paciente": p["id_paciente"],
            "Risco (%)": round(dados_api["probabilidade_falta"] * 100, 1),
            "Alerta": dados_api["alerta"]
        })
        print(f"{p['id_paciente']} processado.")
        
    except Exception as e:
        print(f"Erro ao analisar {p['id_paciente']}: {e}")
        
    # Pausa de meio segundo para não sobrecarregar o nosso servidor gratuito no Render
    time.sleep(0.5)

# 3. Formata os resultados num DataFrame e exporta
df_relatorio = pd.DataFrame(resultados)

print("\n" + "="*45)
print(" RELATÓRIO DIÁRIO DE PREVENÇÃO DE NO-SHOW")
print("="*45)
print(df_relatorio.to_string(index=False))
print("="*45)

df_relatorio.to_csv("relatorio_risco_amanha.csv", index=False)
print("\nFicheiro 'relatorio_risco_amanha.csv' gerado para a equipa de atendimento!")