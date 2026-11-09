SaúdeJá - Motor Preditivo de No-show
O SaúdeJá é uma API inteligente construída para o setor de Healthtech, focada em prever o
risco de ausência (no-show) de pacientes em consultas médicas e gerar recomendações de
abordagem para as secretárias das clínicas.
Este repositório contém a transição de um modelo de Machine Learning em ambiente de
pesquisa (Jupyter Notebook herdado) para um produto de engenharia de software em
produção, escalável e em conformidade com as leis de proteção de dados.

Arquitetura e Stack Tecnológica
O sistema foi desenhado para ser leve, assíncrono e de baixo custo operacional.
 Backend / API: Python 3.11.9 com FastAPI (arquitetura assíncrona).
 Machine Learning: LightGBM (Modelo de classificação binária herdado e produtizado).
 LLM / GenAI: API do Google Gemini (gemini-3.8-flash) para recomendações contextuais.
 Frontend: Streamlit para simulação visual da interface da clínica.
 Deploy: Infraestrutura PaaS (Render / Railway) com pipeline CI/CD via GitHub Actions.
(Nota: O Diagrama C4 da arquitetura e as ADRs encontram-se na pasta docs/architecture/)

Conformidade LGPD e Segurança
Os dados de saúde são considerados dados sensíveis (Art. 5º, II e Art. 11 da LGPD). O
sistema implementa controlos rigorosos de privacidade:
 Base Legal: Execução de contrato e Legítimo Interesse da clínica na otimização da
agenda.
 Sanitização de PII: O sistema possui uma função de sanitização no backend que mascara
o Nome e o CPF do paciente antes de qualquer chamada externa.
 Transferência Internacional: A geração do texto da recomendação recorre à API do
Google Gemini, consistindo numa transferência internacional de dados (devidamente
anonimizados).
 Gestão de Segredos: A chave da API (GEMINI_API_KEY) nunca é enviada no código,
sendo gerida via ficheiro .env localmente e injetada via variáveis de ambiente no deploy.

Otimizações Implementadas
 Cache em Memória (Dicionário Local): Para evitar chamadas redundantes ao LLM da
Google, implementámos um sistema de cache. Se o mesmo paciente (com o mesmo risco
predito) for consultado novamente, o sistema devolve a resposta instantaneamente,
reduzindo a latência da API e poupando custos operacionais e limites de quota.

 Tratamento de Exceções de Rede: Caso o serviço do Gemini falhe ou a quota exceda
(Erro 429), a API não quebra. Um bloco try...except devolve uma mensagem de
contingência verde para o ecrã da clínica.

Observabilidade e Métricas de Saúde
O sistema está instrumentado para monitorizar cinco métricas vitais no dashboard da
plataforma de deploy (Render):
1. Latência (p95): Tempo de resposta do endpoint /predict.
2. Custo / Quota: Monitorização do consumo gratuito da API Gemini.
3. Erros (HTTP 5xx / 429): Taxa de falhas de comunicação com o LLM ou timeouts.
4. Volume: Quantidade de predições de no-show efetuadas diariamente.
5. Qualidade: Frequência de cache hits vs. chamadas reais à rede.

Como Rodar Localmente
1. Clone o repositório e crie o ambiente virtual:
git clone https://github.com/AssisJoao73/ai-factory-saudeja.git
cd ai-factory-saudeja
python3 -m venv venv
source venv/bin/activate
2. Instale as dependências:
pip install -r requirements.txt
3. Configure as variáveis de ambiente:
Copie o ficheiro .env.example para .env e insira a sua chave real em GEMINI_API_KEY.
4. Treine o modelo atualizado (Opcional):
python3 train.py
5. Inicie o Servidor da API:
uvicorn main:app --reload
6. Inicie o Frontend:
Abra um novo terminal, ative o venv e execute:
streamlit run frontend.py

Troubleshooting (Resolução de Problemas Comuns)
 Erro 429 - Quota Exceeded (Gemini API): O limite do escalão gratuito foi atingido (20
chamadas/dia). O sistema devolve automaticamente a mensagem genérica de erro.
Solução: Aguarde a reinicialização da quota diária ou faça upgrade da conta de faturação
na Google Cloud.

 Timeout no Build do Render (Demora &gt; 15 min): Versões demasiado recentes do Python
(3.12+) podem não possuir wheels pré-compilados para o lightgbm ou scikit-learn.
Solução: Configure a variável de ambiente PYTHON_VERSION=3.11.9 no painel do
Render e execute um Clear Build Cache.
 Erro ao carregar model.pkl (Dicionário vs. Modelo): A versão herdada da API esperava
um objeto de modelo puro. A versão atual espera um dicionário {&quot;model&quot;: modelo,
&quot;mapa_especialidade&quot;: mapa_esp}. Certifique-se de gerar o modelo sempre com python
train.py e nunca com os scripts sintéticos descontinuados.

Links do Projeto
 URL da Aplicação (Frontend): 
 URL da API (Swagger UI): 
 Vídeo de Apresentação (Pitch): 