# ADR 002: Plataforma de Hospedagem (Deploy)

## Contexto e Problema
A solução necessita estar acessível via internet por uma URL pública estável, suportar a execução de código Python (inferência do modelo) e manter os custos de infraestrutura estritamente abaixo do orçamento de US$ 100/mês definido pelo briefing. É também necessário separar ambientes de *dev* e *prod* com gestão de *secrets* isoladas.

## Alternativas Consideradas
* **Render (Plataforma como Serviço - PaaS):** Oferece *deploy* automatizado diretamente do GitHub, com um plano *Free* e um plano *Hobby* muito econômicos.
* **Hugging Face Spaces:** Excelente para demonstrações de Machine Learning, mas possui limitações na arquitetura de APIs REST puras que devem operar de forma invisível em um backend B2B.
* **AWS EC2 (IaaS):** Controle total da máquina virtual, mas requer configuração manual do sistema operacional, servidores web (Nginx) e certificados SSL, aumentando muito a complexidade da Etapa 1.

## Decisão
Escolhemos o **Render** (podendo adaptar para Railway caso haja indisponibilidade).

## Consequências
* **Positivas:** O pipeline de CI/CD pode ser configurado com extrema facilidade, bastando conectar o repositório do GitHub. O custo ficará em $0 (tier gratuito) ou em um valor marginal, poupando a totalidade do orçamento mensal.
* **Negativas:** Nos planos gratuitos, o servidor adormece após períodos de inatividade, o que causa lentidão (*cold start*) na primeira requisição do dia. Para efeitos da entrega acadêmica, esse fator é tolerável.