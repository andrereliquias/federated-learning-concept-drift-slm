# Federated Learning for Time Series under Concept Drift - mapeamento sistemático (material externo)

**Autor:** André R S Minari - ICMC/USP, disciplina SSC5905 (Revisão Sistemática em Engenharia de Software).

Material externo do mapeamento sistemático, ainda em andamento, de estudos primários que investigam desvio de conceito ao aplicar Aprendizado Federado a séries temporais (rodada EM01; dados de 17/11/2026).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `PROTOCOLO.md` | Protocolo completo da rodada EM01, histórico de versões, amostra da RQ1 e declaração de uso de LLM. |
| `estudos-em01.csv` | Os 529 estudos únicos, com metadados, decisão, fase, critérios e justificativa resumida. |
| `buscas-em01.csv` | Todas as execuções de busca registradas (rodada anterior e EM01), com string, campos, filtros, data e hora, contagens e URL. |
| `formulario-extracao.md` | Versão final do formulário de extração e regras de registro. |
| `extracao-rq1.csv` | Extração dos 7 campos da RQ1 nos 10 estudos analisados, com origem, localizador e status de cada valor. |
| `contagens.json` | Todas as contagens usadas no artigo, geradas pelo script. |
| `scripts/gerar_materiais.py` | Gera os CSVs, as contagens, as tabelas, as figuras e a bibliografia dos estudos. |

## Legenda de `estudos-em01.csv`

| Coluna | Significado |
|---|---|
| `study_id` | Identificador estável do estudo único na coleção EM01. |
| `titulo`, `autores`, `ano`, `veiculo`, `tipo_publicacao`, `doi`, `url` | Metadados do registro representativo da exportação. |
| `bases` | Bases em que o estudo foi recuperado (`SCOPUS`, `IEEE`, `ACM`, separadas por `;`). |
| `situacao` | Estado atual do estudo na seleção (valores abaixo). |
| `fase_decisao` | `titulo_resumo` ou `texto_completo`; vazio sem decisão. `texto_completo` indica decisão baseada em análise do texto completo intermediada por LLM (ver `PROTOCOLO.md`, seção 12). |
| `criterios_inclusao_atendidos` | Critérios que fundamentam a inclusão preliminar (CI1, CI2, CI6). Não equivale a inclusão final. |
| `criterio_exclusao` | Critérios de exclusão aprovados (CE1–CE7). |
| `criterios_pendentes` | Critérios ainda em dúvida. |
| `justificativa` | Justificativa da decisão, resumida sem mudar o sentido; vazia sem decisão. |
| `situacao_acesso` | `texto_fornecido_a_llm_pelo_pesquisador`, `pendente_acesso`, `texto_completo_local_disponivel` ou `nao_informado`. |
| `usado_na_rq1` | `sim` para os 10 estudos da amostra da RQ1. |

Valores de `situacao`:

- `incluir_preliminar`: decisão do pesquisador de avançar o estudo; inclusão final ainda não confirmada.
- `excluir`: decisão do pesquisador de excluir, com critério registrado.
- `incerto`: decisão do pesquisador de manter a dúvida; ver `criterios_pendentes`.
- `pretriagem_aguardando_validacao`: há proposta de pré-triagem, sem decisão do pesquisador.
- `nao_avaliado`: sem proposta nem decisão.

Campo vazio significa que nada foi registrado, e não que o estudo careça da característica. Por questões de direitos autorais, os resumos ficaram de fora.

## Como reproduzir figuras e tabelas

Execute na raiz do repositório de origem, onde as entradas ficam em `docs/mapeamento/`:

```sh
python3 -m pip install matplotlib
python3 projetos-final/projeto-5/scripts/gerar_materiais.py
sh projetos-final/projeto-5/artigo/build.sh   # pdflatex + bibtex + pdflatex x2
```

Além de recalcular a amostra da RQ1, o script falha quando `extracao-rq1.csv` não corresponde a ela. As contagens citadas no artigo saem todas de `artigo/contagens.tex`, que o mesmo script gera.
