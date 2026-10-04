# ADR 001: Escolha do Framework Web para a API de Inferência

## Contexto e Problema
O classificador de risco de no-show atual reside exclusivamente em um Jupyter Notebook (`notebook.ipynb`). Para que o modelo (`model.pkl`) possa ser integrado no sistema de gestão das clínicas, precisamos encapsular a inferência em uma API REST robusta, capaz de higienizar dados de entrada para evitar violações da LGPD (dados sensíveis de saúde).

## Alternativas Consideradas
* **FastAPI:** Framework moderno, assíncrono, fortemente tipado (Pydantic).
* **Flask:** Microframework clássico, flexível, mas sem documentação de API nativa e validação de dados embutida.
* **Django REST Framework:** Framework completo e maduro, porém excessivamente pesado e complexo para um microsserviço focado apenas em inferência de ML.

## Decisão
Escolhemos o **FastAPI**.

## Consequências
* **Positivas:** A validação de dados com Pydantic garante que o *payload* do paciente (idade, sexo, especialidade, etc.) chega com os tipos corretos antes de ir para o modelo LightGBM. A documentação OpenAPI (Swagger) é gerada automaticamente, facilitando a integração pelas clínicas.
* **Negativas:** Exige um rigor maior na tipagem do código em comparação com o Flask, o que aumenta ligeiramente o tempo de configuração dos schemas de dados.