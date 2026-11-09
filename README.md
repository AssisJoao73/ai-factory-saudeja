SaúdeJá - Motor Preditivo de No-show

O SaúdeJá é uma API inteligente construída para o setor de Healthtech, focada em prever o
risco de ausência (no-show) de pacientes em consultas médicas e gerar recomendações de
abordagem estratégica para as secretárias das clínicas.
Este documento documenta a transição de um modelo de Machine Learning em ambiente de
pesquisa (Jupyter Notebook) para um produto de engenharia de software em produção,
escalável e em estrita conformidade com as leis de proteção de dados (LGPD).
Arquitetura e Stack Tecnológica
O sistema foi desenhado para ser leve, assíncrono e de baixo custo operacional
(infraestrutura serverless).
Backend / API: Python 3.11 com FastAPI (arquitetura assíncrona).
Machine Learning: LightGBM (Modelo de classificação binária herdado e produtizado
via joblib).
LLM / GenAI: API do Google Gemini (gemini-3.8-flash) para recomendações contextuais.
Frontend: Streamlit com layout em colunas simulando a interface de recepção da clínica.
Deploy e Infraestrutura: Render (Backend) e Streamlit Cloud (Frontend) integrados via
GitHub Actions (CI/CD).
Conformidade LGPD e Segurança
Os dados de saúde são considerados sensíveis (Art. 5º, II e Art. 11 da LGPD). O sistema
implementa controlos rigorosos de privacidade:
Sanitização de PII (Backend): O sistema aplica uma máscara no Nome e no CPF do
paciente antes de qualquer chamada externa. Os dados reais não alimentam a rede
externa.

Gestão de Segredos: A chave da API (GEMINI_API_KEY) nunca é enviada no código-fonte,
sendo injetada exclusivamente via variáveis de ambiente no deploy em nuvem.
Como Rodar Localmente
1. 1. Clone o repositório e crie o ambiente virtual
2. 2. Instale as dependências com versões pinadas (pip install -r requirements.txt)
3. 3. Configure as variáveis de ambiente (.env com a GEMINI_API_KEY)
4. 4. Inicie a API (Backend) com uvicorn main:app --reload
5. 5. Inicie o Frontend com streamlit run frontend.py
Limitações Conhecidas
Cold Start: Por estar hospedado na camada free-tier do Render, o servidor de backend
adormece após 15 minutos de inatividade. A primeira requisição após esse período
pode sofrer um atraso (cold start) de cerca de 50 a 60 segundos.
Memória Volátil: O cache de respostas da IA atualmente utiliza um dicionário em
memória RAM. Quando o contêiner do Render reinicia, o cache é zerado. No roadmap
futuro (v1.1), isso será migrado para um banco Redis.
Troubleshooting (Resolução de Problemas)
Problema Sintoma Causa Raiz e Solução
Timeout da IA / Render Erro 504 Deadline expired
before operation could
complete. O Streamlit fica
carregando infinitamente.

Causa: Sobrecarga na API
gratuita do Google ou
latência excessiva de rede.
Solução: A API foi atualizada
com um bloco try/except de
contingência. Se o Gemini
estourar o tempo limite, o
sistema aciona um fallback
inteligente.

Modelo Descontinuado Erro 404 models/gemini-
1.5-flash is not found
retornado no payload.

Causa: O pacote google-
generativeai descontinuou
rotas antigas.
Solução: Refatorado para
utilizar estritamente a
versão gemini-3.8-flash.

Falha de Build (Render) O processo de build trava
por &gt;15 minutos instalando
pandas e scikit-learn.

Causa: Incompatibilidade de
wheels pré-compilados.
Solução: A versão do
interpretador foi fixada em
PYTHON_VERSION=3.11
nas variáveis de ambiente
do Render.

Quota Esgotada Erro HTTP 429 Too Many Causa: Limite diário da

Requests. chave de API excedido.
Solução: Trocar a
GEMINI_API_KEY por uma
nova gerada em um projeto
limpo.

Links do Projeto
Aplicação em Produção (Frontend): https://ai-factory-saudeja-pmkz42gsvwheegzztciblx.streamlit.app/
API Swagger UI (Backend): https://ai-factory-saudeja.onrender.com/docs#/