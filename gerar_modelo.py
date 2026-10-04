import pandas as pd
import lightgbm as lgb
import joblib
import numpy as np

print("A gerar modelo V2 com 1.000 registos sintéticos...")

# Semente para garantir que os resultados aleatórios são sempre iguais
np.random.seed(42)
n_pacientes = 1000

# 1. Gerar dados aleatórios para 1.000 consultas
idade = np.random.randint(18, 80, n_pacientes)
sexo = np.random.randint(0, 2, n_pacientes)
especialidade = np.random.randint(1, 5, n_pacientes)
distancia_km = np.random.uniform(1.0, 50.0, n_pacientes)
dias_espera = np.random.randint(1, 90, n_pacientes)
historico_noshow = np.random.randint(0, 5, n_pacientes)

# 2. Lógica de risco (Padrão oculto que o LightGBM vai ter de descobrir)
# Quanto maior a distância, a espera e o histórico de faltas, maior a probabilidade matemática
probabilidade_matematica = (distancia_km / 100) + (dias_espera / 150) + (historico_noshow * 0.20)
# Adicionamos um pouco de "ruído" para simular a imprevisibilidade humana
probabilidade_matematica += np.random.normal(0, 0.1, n_pacientes)

# Se a probabilidade matemática for maior que 0.6, o paciente faltou (1). Senão, compareceu (0).
y_treino = (probabilidade_matematica > 0.6).astype(int)

X_treino = pd.DataFrame({
    'idade': idade,
    'sexo': sexo,
    'especialidade': especialidade,
    'distancia_km': distancia_km,
    'dias_entre_agendamento_consulta': dias_espera,
    'historico_noshow': historico_noshow
})

# 3. Treinar o modelo robusto
print("A treinar o LightGBM...")
modelo = lgb.LGBMClassifier(n_estimators=50, random_state=42)
modelo.fit(X_treino, y_treino)

# 4. Guardar o novo binário
joblib.dump(modelo, 'model.pkl')
print("model.pkl V2 criado com sucesso! Padrões complexos aprendidos.")