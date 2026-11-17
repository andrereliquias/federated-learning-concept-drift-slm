# Formulário de extração - versão final da rodada EM01

Esta é a versão usada na síntese de 17/11/2026. Ela parte do formulário inicial do Projeto 4 (execução v2) e difere dele em duas mudanças: os campos da RQ1 passaram a ter valores codificados, e entraram "representação temporal" e "topologia federada", que apareceram durante a codificação dos dez estudos da amostra. Os campos marcados com ✱ já foram aplicados (`extracao-rq1.csv`); os demais aguardam a extração completa.

## Campos

| Campo (`field`) | Valores ou conteúdo | RQ |
|---|---|---|
| Identificação | ID, título, autores, DOI, veículo, tipo, bases de origem, versão consultada | RQ6 |
| Datas e aceite | ano editorial, data online, evidência de aceite e busca correspondente | RQ6 |
| `ts_task` ✱ | `previsao`, `classificacao`, `deteccao de anomalias`, `deteccao de intrusao`, `outra (...)`, `nao identificada` | RQ1, RQ6 |
| `application_domain` ✱ | domínio nos termos dos autores; agrupado depois (benchmarks de fluxo, redes e segurança, saúde, sensoriamento industrial, atividades humanas, computação de borda, outros) | RQ1, RQ6 |
| `temporal_representation` ✱ | `sequencia/serie explicita` (janelas, lags, estado recorrente) ou `fluxo de dados ordenado` (ordem de chegada, avaliação prequencial ou por rodada) | RQ1 |
| `series_dimensionality` ✱ | `univariada`, `multivariada`, `nao identificado nas fontes consultadas` | RQ1, RQ4 |
| `federated_topology` ✱ | `centralizada (servidor)`, `centralizada com agrupamento de clientes`, `por comunidades de clientes`, `descentralizada (P2P/gossip)` | RQ1, RQ5 |
| `federated_setting` ✱ | `horizontal`, `vertical`, `outra`, `nao identificada` | RQ1, RQ5 |
| `approach_family` ✱ | família do modelo-base ou do mecanismo de aprendizado (protótipos, rede recorrente, aprendizado contínuo com replay etc.) | RQ1 |
| Caracterização do drift | definição adotada, distribuição ou relação alterada, momento e alcance entre clientes; tipo (abrupto, gradual, recorrente, incremental) só quando sustentado | RQ2 |
| Heterogeneidade | formas de non-IID, construção das partições, distinção entre diferença estática e mudança temporal | RQ2 |
| Detecção | método, sinal monitorado, janela, limiar, frequência e local da detecção | RQ3 |
| Adaptação | mecanismo, gatilho, alcance local ou global, relação com o drift | RQ3 |
| Cenário de drift | natural ou induzido, regra de geração, intensidade, frequência, clientes atingidos | RQ4 |
| Protocolo de avaliação | divisão temporal, treino/teste, disponibilidade de rótulos, repetições, controle de vazamento temporal | RQ4 |
| Métricas e comparações | métricas preditivas e de drift, custos de comunicação/computação, baselines, ablações | RQ4 |
| Resultados reportados | valores e condições das comparações, variabilidade, limitações declaradas | RQ3, RQ4 |
| Agrupamento | uso de grupos, método, similaridade, atualização dos grupos, relação com drift | RQ5 |
| Coordenação e agregação | sincronismo, agregação, ponderação, tratamento de atualizações defasadas | RQ5 |

## Registro de cada valor

Uma linha por valor, no formato `study_id, field, value, source_path, locator, evidence_excerpt, status, reviewed_by, review_date, review_approval`.

- `source_path`: origem do dado, que pode ser `resumo` (metadados da exportação), `analise_llm_pdf` (análise de outra LLM ao PDF, registrada na seleção) ou `pdf_lido_pelo_pesquisador`.
- `locator`: seção, página, tabela, figura ou equação.
- `evidence_excerpt`: trecho curto ou paráfrase da evidência; citações literais entre aspas.
- `status`: `reported` (declarado pelo estudo), `interpreted` (classificação apoiada em evidência, com justificativa), `not_reported` (campo aplicável sem informação no estudo), `unclear` (fontes consultadas não decidem), `not_applicable`.
- `reviewed_by`, `review_date`, `review_approval`: preenchidos quando a conferência no PDF for feita.

Regras: silêncio do estudo não é ausência; não inferir detector, tipo de drift, heterogeneidade ou assincronismo sem trecho localizável; preservar divergências internas do estudo sem escolher uma versão como verdadeira.
