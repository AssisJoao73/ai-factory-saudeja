# Relatório de Incidente (Post-Mortem) - Projeto SaúdeJá

* **Data do Incidente:** 04 de Outubro de 2026
* **Status:** Resolvido / Em Produção
* **Impacto:** Indisponibilidade temporária no tempo de *build* do serviço na nuvem (Render) durante a primeira implantação.

## 1. Descrição do Incidente
Durante o primeiro *deploy* da API FastAPI no Render, o processo de compilação (*build*) ultrapassou o limite operacional esperado, travando por mais de 20 minutos na etapa de preparação de metadados das bibliotecas de ciência de dados (`pandas` e `scikit-learn`). 

## 2. Causa Raiz
O ambiente de nuvem selecionou por padrão uma versão muito recente do interpretador Python (versão 3.14). Para esta versão recente, pacotes complexos de C/C++ embutidos no ecossistema de machine learning careciam de instaladores pré-compilados (*wheels*), forçando a infraestrutura gratuita (com recursos limitados de CPU e RAM) a compilar o código-fonte do zero.

## 3. Ações de Resolução
1. **Identificação do Gargalo:** Análise detalhada dos logs de erro do servidor em nuvem.
2. **Ajuste de Versão:** Fixação explícita do interpretador para a versão **Python 3.11.9** através de variáveis de ambiente no Render, garantindo a compatibilidade com *wheels* estáveis.
3. **Limpeza de Cache:** Execução de um *Clear Build Cache & Deploy* para limpar os artefatos corrompidos anteriores.
4. **Validação:** O tempo de *build* caiu de mais de 20 minutos para menos de 2 minutos, estabilizando o serviço de forma bem-sucedida.

## 4. Lições Aprendidas
* **Paridade de Ambiente:** É fundamental declarar explicitamente a versão do Python no ecossistema de produção (`PYTHON_VERSION`) para evitar comportamentos inesperados causados por atualizações automáticas de ambiente.
* **Arquitetura Build-Time:** Manter a geração dinâmica do modelo `.pkl` no comando de *build* provou ser eficiente, desde que as dependências base estejam ancoradas em versões estáveis.