# SaúdeJá - Classificador de No-show

Notebook com classificador LightGBM pra prever no-show de paciente em consulta.

**Acurácia 78% no test set (split 80/20, random_state=42).**
**F1 classe positiva (no-show=1): 0.65**
**ROC-AUC: 0.81**

## Features usadas

- `idade` — idade do paciente (int)
- `sexo` — F/M (binarizado 0/1)
- `especialidade` — label encoding (cardiologia, dermato, ginecologia, ortopedia, oftalmo, clínica geral, pediatria)
- `distancia_km` — distância casa-clínica
- `dias_entre_agendamento_consulta` — quanto antes o paciente agendou
- `historico_noshow` — quantas vezes esse paciente já faltou

Target: `no_show` (0 = compareceu, 1 = faltou).

## Como rodar

```
jupyter notebook
```

Abre `notebook.ipynb` e roda tudo (Run All). Treino leva uns 30s no meu macbook.

Salva `model.pkl` na raiz.

## Modelo

LightGBM com:
- n_estimators=200
- learning_rate=0.05
- max_depth=6
- num_leaves=31

Tunei na mão olhando F1. Não rodei GridSearch ainda (TODO).

## TODO

- precisamos transformar isso em API pra integrar com sistema das clínicas — vou abrir ticket no Jira (SAUDEJA-241)
- SHAP pra explicabilidade (liderança médica vai pedir)
- oversampling SMOTE? classe positiva tá em ~30%, dá pra melhorar F1
- pipeline de re-treino mensal — hoje é manual
- testes? lol

---

*Camila S. — Data Science*


## Arquitetura e Decisões de Stack

### 1. Matriz de Decisão

**Critérios de Avaliação e Pesos (1 a 3):**
* **Custo de Operação (Peso 3):** O orçamento máximo é de 100 USD/mês. Soluções gratuitas ou de custo marginal (Serverless/PaaS) ganham vantagem.
* **Velocidade de Desenvolvimento (Peso 3):** Necessidade de criar uma API funcional rapidamente na Etapa 1.
* **Integração com Machine Learning (Peso 2):** Facilidade em carregar ficheiros `.pkl` (joblib) e lidar com dataframes ou matrizes.
* **Geração de Documentação (Peso 2):** Como a API será consumida pelo sistema de gestão das clínicas, ter a documentação da API gerada automaticamente poupa tempo.

| Alternativa (API) | Custo (x3) | Velocidade (x3) | ML/Data (x2) | Docs (x2) | **Total** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FastAPI** | 3 (9) | 3 (9) | 3 (6) | 3 (6) | **30** |
| **Flask** | 3 (9) | 2 (6) | 3 (6) | 1 (2) | **23** |
| **Django REST**| 2 (6) | 1 (3) | 2 (4) | 2 (4) | **17** |
