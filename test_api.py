from fastapi.testclient import TestClient
from main import app

# Cria um cliente de teste que simula um navegador/sistema acessando a API
client = TestClient(app)

# Teste 1: Verifica se a API está online (Healthcheck)
def test_api_online():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "API SaúdeJá operante."

# Teste 2: Verifica se o modelo consegue fazer uma predição com dados corretos
def test_predicao_com_sucesso():
    payload = {
        "idade": 30,
        "sexo": 1,
        "especialidade": 1,
        "distancia_km": 10.5,
        "dias_entre_agendamento_consulta": 5,
        "historico_noshow": 0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "probabilidade_falta" in response.json()
    assert "alerta" in response.json()

# Teste 3: Verifica se a API bloqueia dados inválidos (Proteção/Validação)
def test_predicao_dados_incompletos():
    payload_incompleto = {
        "idade": 30
        # Faltam todos os outros campos obrigatórios
    }
    response = client.post("/predict", json=payload_incompleto)
    assert response.status_code == 422  # 422 Unprocessable Entity (Erro padrão do FastAPI para dados inválidos)