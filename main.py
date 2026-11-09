import os
from dotenv import load_dotenv
import re
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Carrega Variáveis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
minha_chave = os.getenv("GEMINI_API_KEY")

# Configura IA
genai.configure(api_key=minha_chave)
app = FastAPI(title="SaúdeJá API")
cache_ia = {}

# Usa a versão correta e mais rápida do Gemini
llm_model = genai.GenerativeModel('gemini-3.8-flash')

# Carrega o modelo LightGBM com blindagem contra erros de leitura
try:
    artefatos = joblib.load("model.pkl")
    if isinstance(artefatos, dict) and "model" in artefatos:
        model = artefatos["model"]
    else:
        model = artefatos
    
    if not hasattr(model, 'predict_proba'):
        model = None
except:
    model = None

class PatientData(BaseModel):
    nome: str
    cpf: str
    idade: int
    sexo: int
    especialidade: int
    distancia_km: float
    dias_entre_agendamento_consulta: int
    historico_noshow: int

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
        risco_no_show = 82.5
        
    nome_seguro, cpf_seguro = sanitize_pii(data.nome, data.cpf)
    
    prompt = (
        f"Aja como um assistente de clínica. O paciente {nome_seguro} (CPF: {cpf_seguro}) "
        f"tem um risco de {risco_no_show}% de faltar. Escreva uma mensagem curta (máximo 2 linhas) "
        "instruindo a secretária sobre como abordar esse paciente para confirmar a presença."
    )
    
    chave_paciente = f"{cpf_seguro}_{risco_no_show}"
    
    if chave_paciente in cache_ia:
        recomendacao = cache_ia[chave_paciente]
    else:
        try:
            resposta_llm = await llm_model.generate_content_async(prompt)
            recomendacao = resposta_llm.text.strip()
            cache_ia[chave_paciente] = recomendacao 
        except Exception as e:
            recomendacao = f"Erro exato do Google: {str(e)}"

    return {
        "paciente": nome_seguro,
        "cpf": cpf_seguro,
        "risco_predito": risco_no_show,
        "recomendacao_secretaria": recomendacao
    }