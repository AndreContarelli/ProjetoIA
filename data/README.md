# SBA National Dataset — Documentação dos Dados

## 1. Identificação e Fonte
* **Nome do Dataset:** SBA National Dataset (*Should This Loan be Approved or Denied?*)
* **Origem:** *U.S. Small Business Administration* (SBA)
* **Disponibilização Pública:** Kaggle (curadoria por Mirbek Toktogaraev)
* **Link para Download Oficial:** [Kaggle - Should This Loan be Approved or Denied?](https://www.kaggle.com/datasets/mirbektoktogaraev/should-this-loan-be-approved-or-denied)
* **Referência Acadêmica:** LI, M.; MICKEL, A.; TAYLOR, S. *"Should This Loan be Approved or Denied?": A Large Dataset with Class Assignment Guidelines*. Journal of Statistics Education, v. 26, n. 1, p. 55-66, 2018.

## 2. Dimensões e Período
* **Total de Observações:** 899.164 registros históricos.
* **Quantidade de Atributos:** 27 variáveis cadastrais, temporais e financeiras.
* **Janela Temporal:** Empréstimos concedidos entre os anos de 1987 e 2014.

## 3. Variável-Alvo
* **Coluna Original:** `MIS_Status`
  * `PIF` (*Paid In Full*): Empréstimo quitado integralmente pelo tomador.
  * `CHGOFF` (*Charged Off*): Baixa contábil decorrente de inadimplência/perda financeira.
* **Variável Binária no Projeto (`Default`):**
  * `0`: Operação quitada (`PIF`)
  * `1`: Ocorrência de inadimplência (`CHGOFF`)

## 4. Instruções de Reprodução
Devido às restrições de tamanho de arquivo do GitHub (o CSV descompactado possui mais de 250 MB), o arquivo bruto não é versionado no repositório. Para executar os scripts:
1. Acesse o link do Kaggle acima e faça o download do arquivo compactado.
2. Extraia o arquivo `SBAnational.csv`.
3. Salve o arquivo nesta pasta (`data/`) ou na raiz do projeto.
