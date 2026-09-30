1.Arquitetura e Disponibilidade
  Problema: O modelo de classificação do risco de no-show encontra-se acoplado a um Jupyter Notebook (notebook.ipynb) e nunca foi colocado em produção.
  Impacto: O sistema atual não possui uma API, não tem interface para os utilizadores, não tem deploy, monitorização, nem pipeline automático para o re-treino. Existe apenas um script (train.py) descrito como "meio-pronto".
  Ação Necessária: Desenvolver uma API REST (ex: FastAPI) para encapsular o ficheiro model.pkl e separar o ambiente de inferência do ambiente de treino.

2.Segurança e Conformidade (LGPD)
  Problema: O modelo consome dados que, num cenário real, são considerados dados sensíveis de saúde ao abrigo da LGPD (Art. 5º, II e Art. 11).
  Impacto: O ambiente atual de exploração de dados (Notebooks) propicia a exposição acidental de dataframes. O briefing define como restrição absoluta que nunca podem existir dados pessoais (PII) impressos em logs.
  Ação Necessária: Garantir que a nova API higienize os payloads de entrada e saída e que os logs da aplicação não registem atributos identificáveis dos pacientes.

3.Qualidade de Código e Testes
  Problema: A ausência total de testes de código, confirmada pela anotação "testes? lol" no README.
  Impacto: Qualquer alteração no código atual ou atualização de bibliotecas pode quebrar o modelo em silêncio.
  Ação Necessária: Implementar os smoke tests exigidos pela rubrica da disciplina para validar a saúde e a disponibilidade da API.

4.Engenharia do Modelo (Dívida Técnica de Data Science)
  Problema: O ajuste de hiperparâmetros (n_estimators, learning_rate, max_depth, num_leaves) foi feito manualmente.   
  Impacto: Falta robustez na otimização do modelo. Além disso, existe um desbalanceamento (a classe positiva representa apenas ~30%), para o qual não foram aplicadas técnicas como o SMOTE.
  Ação Necessária: O re-treino mensal acordado com o produto é atualmente manual. Será necessário deixar um pipeline executável preparado.