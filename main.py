from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Inicializa a aplicação
app = FastAPI(
    title="SaúdeJá API",
    description="Motor de inferência preditiva para risco de no-show.",
    version="1.0.0"
)

# Carrega o modelo globalmente para não ler o arquivo do zero a cada requisição
try:
    modelo = joblib.load('model.pkl')
except Exception as e:
    modelo = None

# 2. Esquema de dados (Validação LGPD)
class PacientePayload(BaseModel):
    idade: int
    sexo: int  
    especialidade: int
    distancia_km: float
    dias_entre_agendamento_consulta: int
    historico_noshow: int

@app.get("/")
def read_root():
    status_modelo = "Ativo" if modelo else "Falha ao carregar"
    return {"status": "API SaúdeJá operante.", "modelo": status_modelo}

# 4. Rota principal de predição (Agora REAL)
@app.post("/predict")
def predict_risco(paciente: PacientePayload):
    if modelo is None:
        raise HTTPException(status_code=500, detail="Modelo não carregado.")
        
    # Converte os dados validados para DataFrame Pandas
    dados_df = pd.DataFrame([paciente.model_dump()])
    
    # Extrai a probabilidade da classe 1 (Falta)
    probabilidade = modelo.predict_proba(dados_df)[0][1]
    alerta = "Risco Alto" if probabilidade >= 0.70 else "Risco Normal"
    
    return {
        "status": "sucesso",
        "probabilidade_falta": round(float(probabilidade), 4),
        "alerta": alerta
    }