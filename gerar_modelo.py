import pandas as pd
import lightgbm as lgb
import joblib

print("A gerar modelo de teste...")

# Dados fictícios apenas para ensinar a estrutura ao modelo
X_treino = pd.DataFrame({
    'idade': [25, 45, 60, 19, 30, 55],
    'sexo': [0, 1, 0, 1, 0, 1],
    'especialidade': [1, 2, 3, 1, 2, 3],
    'distancia_km': [5.5, 12.0, 2.1, 15.3, 1.5, 20.0],
    'dias_entre_agendamento_consulta': [10, 2, 30, 5, 1, 60],
    'historico_noshow': [0, 1, 0, 3, 0, 5]
})
y_treino = [0, 0, 0, 1, 0, 1]  # 0 = Compareceu, 1 = Faltou

# Treina o modelo LightGBM
modelo = lgb.LGBMClassifier(n_estimators=10)
modelo.fit(X_treino, y_treino)

# Salva o binário na raiz
joblib.dump(modelo, 'model.pkl')
print("✅ model.pkl criado com sucesso na raiz do projeto!")