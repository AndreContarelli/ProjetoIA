# GrafitoIA: Predição de Risco de Inadimplência em Empréstimos a Pequenos Negócios com Machine Learning

**Universidade Presbiteriana Mackenzie**  
**Faculdade de Computação e Informática (FCI)**  
**Disciplina:** Inteligência Artificial – 7ºK SI – Noite | **Docente:** Prof. Dr. Leandro Zerbinatti  
**Ano:** 2026[cite: 3]

---

## Membros da Equipe
* **André Contarelli Lima** — RA: 10410280 — `10410280@mackenzista.com.br`
* **Lucas Bittencourt de Oliveira** — RA: 10409476 — `10409476@mackenzista.com.br`
* **Fernando Paiva** — RA: 10416680 — `10416680@mackenzista.com.br`
* **Alexandre Ribeiro de Souza** — RA: 10417845 — `10417845@mackenzista.com.br`

---

## Visão Geral do Projeto
O **GrafitoIA** propõe o desenvolvimento de um modelo preditivo baseado em aprendizado de máquina supervisionado para estimar o risco de inadimplência em operações de crédito para pequenos negócios. O projeto atua como frente analítica exploratória conectada ao **Grafito**, aplicativo móvel iOS desenvolvido pelo grupo como Trabalho de Conclusão de Curso focado na gestão financeira e controle de estoque de Microempreendedores Individuais (MEI).

Como base empírica, adota-se o *SBA National Dataset* (*U.S. Small Business Administration*), contendo cerca de 899 mil registros reais de concessão de crédito a pequenas empresas[cite: 2].

---

## Estrutura do Repositório

```text
├── docs/
│   └── Relatorio_GrafitoIA_N1.pdf        # Relatório formal da N1 no padrão do template de TCC da FCI
├── data/
│   └── README.md                          # Metadados, dicionário de variáveis e instruções de download do dataset
├── src/
│   └── 01_carga_e_analise_exploratoria.py # Script com cabeçalho padronizado, limpeza, tratamento e plots da EDA
├── .gitignore                             # Filtro para ignorar arquivos pesados (*.csv, *.zip, caches)
└── README.md                              # Documentação principal do projeto
