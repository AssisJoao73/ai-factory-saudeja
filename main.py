import os
from dotenv import load_dotenv

# 1. Força a procurar o .env exatamente na mesma pasta onde este script está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 2. Verifica se a chave foi carregada com sucesso
minha_chave = os.getenv("GEMINI_API_KEY")
print("\n" + "="*30)
print(f"DEBUG DA CHAVE: {minha_chave}")
print("="*30 + "\n")

# 3. Importa o resto e configura a IA
import re
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 4. Passa a variável de forma explícita para o Gemini
genai.configure(api_key=minha_chave)

app = FastAPI(title="SaúdeJá API - Etapa 2")
# Cache global para armazenar respostas da IA e economizar tempo/dinheiro
cache_ia = {}
# ... resto do código continua igual ...
llm_model = genai.GenerativeModel('gemini-3.8-flash')

# Carrega o modelo LightGBM treinado na Etapa 1
try:
    model = joblib.load("model.pkl")
except:
    model = None

# Modelo de entrada unificado (Dados ML + PII)
class PatientData(BaseModel):
    nome: str
    cpf: str
    idade: int
    sexo: int
    especialidade: int
    distancia_km: float
    dias_entre_agendamento_consulta: int
    historico_noshow: int

# Função de Sanitização (Requisito LGPD)
def sanitize_pii(nome: str, cpf: str):
    partes = nome.split()
    nome_mascarado = partes[0]
    if len(partes) > 1:
        nome_mascarado += f" {partes[1][0]}***"
    
    cpf_limpo = re.sub(r'\D', '', cpf)
    if len(cpf_limpo) == 11:
        cpf_mascarado = f"{cpf_limpo[:3]}.***.***-{cpf_limpo[-2:]}"
    else:
        cpf_mascarado = "***.***.***-**"
        
    return nome_mascarado, cpf_mascarado

@app.post("/predict")
async def predict_no_show(data: PatientData):
    # 1. Predição de Risco (Seu modelo real da etapa 1)
    if model:
        df = pd.DataFrame([{
            "idade": data.idade,
            "sexo": data.sexo,
            "especialidade": data.especialidade,
            "distancia_km": data.distancia_km,
            "dias_entre_agendamento_consulta": data.dias_entre_agendamento_consulta,
            "historico_noshow": data.historico_noshow
        }])
        probabilidade = model.predict_proba(df)[0][1] * 100
        risco_no_show = round(probabilidade, 2)
    else:
        risco_no_show = 82.5 # Valor fixo caso o modelo não esteja na pasta
        
    # 2. Sanitização (LGPD em ação)
    nome_seguro, cpf_seguro = sanitize_pii(data.nome, data.cpf)
    
    # 3. Chamada ao LLM apenas com os dados limpos
    prompt = (
        f"Aja como um assistente de clínica. O paciente {nome_seguro} (CPF: {cpf_seguro}) "
        f"tem um risco de {risco_no_show}% de faltar. Escreva uma mensagem curta (máximo 2 linhas) "
        "instruindo a secretária sobre como abordar esse paciente para confirmar a presença."
    )
    
    # Cria uma chave única para este paciente e este nível de risco
    chave_paciente = f"{cpf_seguro}_{risco_no_show}"
    
    # 1. Verifica se a resposta já está no cache
    if chave_paciente in cache_ia:
        recomendacao = cache_ia[chave_paciente]
        print("\n⚡ [CACHE] Resposta instantânea! Poupou ida ao Google.\n")
    
    # 2. Se não estiver, vai ao Google pedir a geração
    else:
        try:
            print("\n☁️ [API] Indo buscar no Google...\n")
            # Adicione 'await' no início e '_async' no final do método
            resposta_llm = await llm_model.generate_content_async(prompt)
            recomendacao = resposta_llm.text.strip()
            
            # 3. Salva a resposta nova no cache para a próxima vez!
            cache_ia[chave_paciente] = recomendacao 
            
        except Exception as e:
            print(f"========== ERRO DA API: {e} ==========")
            recomendacao = "Erro na IA. Por favor, ligue e confirme manualmente a consulta."

    return {
        "paciente": nome_seguro,
        "cpf": cpf_seguro,
        "risco_predito": risco_no_show,
        "recomendacao_secretaria": recomendacao
    }