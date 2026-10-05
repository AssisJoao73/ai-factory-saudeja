# Changelog

## [v1.0.0] - 2026-10-05
### Adicionado
- API de predição de no-show construída com FastAPI.
- Modelo LightGBM gerado dinamicamente no processo de *build* para conformidade com a LGPD.
- Pipeline de CI/CD automatizado via GitHub Actions com Smoke Tests.
- Script simulador de consumo em lote para a clínica (`simulador_clinica.py`).
- Documentação de arquitetura (ADRs, Matriz de Decisão, Diagrama C4) e Manual de Integração.
- Documento de Post-mortem de infraestrutura.

## [v0.5] (Camila)
- Notebook completo com EDA + treino LightGBM
- Modelo serializado em model.pkl
- Acurácia 78%, F1 da classe positiva 0.65

## [v0.4] (Camila)
- Adicionada feature distancia_km

## [v0.3] (Camila)
- Primeira versão LightGBM substituindo regressão logística