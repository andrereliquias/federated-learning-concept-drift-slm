# Protocolo do mapeamento sistemático - rodada EM01

**Tema:** Aprendizado Federado (FL) aplicado a séries temporais com desvio de conceito.
**Versões vigentes:** protocolo EM01-PROT-1.0-RC1; critérios E05-EM01-1.0; estratégia de busca EM01-BUSCA-1.0; adendo operacional de seleção E12-EM01-OP-1.1.
**Estado dos dados:** 17/11/2026. As contagens deste documento saem de `scripts/gerar_materiais.py` e de `contagens.json`.

Aqui estão o protocolo completo da rodada EM01 e o histórico das versões que a antecederam. O artigo trata só da configuração final; as mudanças, suas datas e seus motivos estão registrados nas seções 13 e 14.

## 1. Objetivo

Mapear estudos primários sobre Aprendizado Federado aplicado a séries temporais que investiguem desvio de conceito, caracterizando cenários de aplicação, tipos de desvio, estratégias de detecção e adaptação, heterogeneidade entre clientes, mecanismos de coordenação e procedimentos de avaliação, para identificar tendências e lacunas no conjunto analisado.

## 2. Questões de pesquisa

| ID | Questão | Motivação |
|---|---|---|
| RQ1 - aplicações | Em quais tarefas e domínios são investigadas abordagens de Aprendizado Federado para séries temporais com desvio de conceito? | Delimitar o espaço de aplicação e as famílias de abordagem. |
| RQ2 - heterogeneidade | Quais tipos de desvio de conceito e formas de heterogeneidade entre clientes são considerados, e como são caracterizados? | Separar mudança temporal de heterogeneidade estática (non-IID). |
| RQ3 - tratamento de drift | Quais estratégias são utilizadas para detectar e/ou adaptar os modelos ao desvio de conceito em séries temporais federadas? | Mapear mecanismos de detecção e adaptação. |
| RQ4 - avaliação | Como as abordagens são avaliadas quanto ao desvio de conceito (datasets, construção dos cenários de drift, métricas, comparação)? | Entender como a evidência sobre drift é produzida. |
| RQ5 - organização federada | Quais mecanismos de agrupamento de clientes, coordenação e agregação são empregados, e que relação os estudos reportam com o tratamento do drift? | Relacionar o desenho da federação ao drift. |
| RQ6 - distribuição das evidências | Como os estudos se distribuem ao longo dos anos, tarefas, domínios e tipos de desvio, e quais concentrações e lacunas aparecem? | Identificar tendências e lacunas no conjunto analisado. |

As lacunas referem-se ao conjunto analisado; não sustentam alegações de ausência fora das fontes consultadas.

## 3. População e escopo

- **População:** estudos primários que propõem, aplicam ou avaliam FL em dados de séries temporais e investigam desvio de conceito.
- **Tarefas:** todas em que a dimensão temporal seja central (previsão, classificação, detecção de anomalias, outras).
- **Dados:** séries univariadas ou multivariadas, reais ou sintéticas; qualquer domínio e configuração federada.
- **Publicação:** artigos completos de periódico ou conferência aceitos após revisão por pares, em inglês.
- **Período:** 2020–2026; ano editorial 2027 admitido quando o aceite após revisão por pares já existia na data da busca correspondente.
- **Dimensões de classificação, não de entrada:** heterogeneidade, agrupamento de clientes e sincronismo.

## 4. Conjunto de controle e calibração

Um pesquisador da área definiu o conjunto de controle com base em estudos de referência do domínio. A rodada anterior usava quatro controles (FLAMES2Graph, TIME-FFM, FedST e FedTime), que não passaram para a EM01: a evidência disponível não mostrava que eles investigassem drift (CI6).

O controle positivo confirmado da EM01 é o **Fed-DCL** (*A Federated Dual-Continual Learning Framework for Adaptive Electric Power Load Forecasting Under Concept Drift*, DOI 10.1109/ICNEPE67923.2025.11384325). Ele foi adotado em 27/10/2026, depois da leitura do PDF (seções II–IV, pp. 224–227) e da conferência editorial. O FedConD continua como candidato, pois sua versão e seu enquadramento editorial ainda estão em verificação. Na coleção, o Fed-DCL corresponde a EM01-S0227 e tem, por ora, inclusão preliminar.

| Execução (Scopus, 27/10/2026) | Conceitos exigidos | Exibidos | Controle |
|---|---|---:|---|
| S4 - 12h55 | FL, séries temporais e drift | 11 | 0/1 |
| Diagnóstico DOI - 12h49 | DOI do controle | 1 | 1/1 |
| Diagnóstico DOI + filtros - 12h59 | DOI e filtros de S4 | 1 | 1/1 |
| Diagnóstico DOI + FL + drift - 13h01 | DOI, FL e drift, filtros de S4 | 1 | 1/1 |
| S5 - 13h15 | FL e drift | 235 | 1/1 |

Pelos diagnósticos, a perda do controle se deveu ao bloco de séries temporais. Sem esse bloco, S5 recuperou o controle e também os 11 DOIs de S4, e a centralidade temporal passou a ser exigida na seleção (CI2/CE2). Houve depois um relato de 2.251 resultados para o núcleo FL AND drift sem filtros, mas, como campos e horário não foram documentados, esse número não é usado como contagem. Com um único controle, não é possível estimar a sensibilidade global.

## 5. Strings por base

String conceitual final (S5): `"federated learning" AND "concept drift"`.

| Base | Consulta e campos | Filtros | Data e hora (UTC−3) | Exibidos | Exportados |
|---|---|---|---|---:|---:|
| Scopus | `TITLE-ABS-KEY ( "federated learning" AND "concept drift" ) AND PUBYEAR > 2019 AND PUBYEAR < 2028 AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) ) AND ( LIMIT-TO ( LANGUAGE , "English" ) )` | 2020–2027; Article/Conference Paper; inglês; sem filtro de estágio final | 27/10/2026 13h15 | 235 | 235 |
| IEEE Xplore | `(("Document Title":"federated learning" OR "Abstract":"federated learning" OR "Index Terms":"federated learning") AND ("Document Title":"concept drift" OR "Abstract":"concept drift" OR "Index Terms":"concept drift"))` | 2020–2027; Conferences, Journals, Early Access Articles; idioma não confirmado | 27/10/2026 13h32 | 396 | 396 |
| ACM DL | `(Title:("federated learning") OR Abstract:("federated learning") OR Keyword:("federated learning")) AND (Title:("concept drift") OR Abstract:("concept drift") OR Keyword:("concept drift"))` | ACM Content: DL; Research Article; sem filtro de data (a interface não oferecia 2027) | 27/10/2026 14h07 | 8 | 8 |

Ao todo, foram exportadas 639 ocorrências. O arquivo `buscas-em01.csv` guarda as URLs de cada execução, os nomes dos arquivos exportados e as observações. A integridade dos três arquivos ficou registrada por SHA-256 no manifesto da coleção. Dos 396 registros da IEEE, 395 trazem resumo. Na ACM, mesmo com o filtro, dois registros indicam workshop; eles foram mantidos para a seleção.

## 6. Critérios de inclusão e exclusão (E05-EM01-1.0)

Inclusão final exige todos os CI.

| ID | Critério | Interpretação |
|---|---|---|
| CI1 | Estudo primário que propõe, aplica ou avalia FL. | FL descentralizado (P2P, gossip) é admitido quando há treinamento colaborativo com dados locais e troca de parâmetros ou estatísticas. |
| CI2 | Contribuição ou avaliação relevante trata explicitamente dados em sequência temporal. | Mera coleta ao longo do tempo não basta. Fluxo ordenado que estrutura método ou avaliação é admitido; não se exige autocorrelação, lags ou termo literal "time series". Basta uma avaliação temporal relevante. |
| CI3 | Artigo completo de periódico ou conferência aceito após revisão por pares. | Versão final, publicação antecipada ou manuscrito aceito verificável. |
| CI4 | Texto em inglês. | |
| CI5 | Ano editorial 2020–2026, ou 2027 com aceite na data da busca. | |
| CI6 | Investiga mudanças ao longo do tempo na distribuição dos dados ou na relação entrada–saída em séries temporais federadas, por caracterização, detecção, adaptação ou avaliação do efeito do drift. | Menções restritas à introdução ou a trabalhos futuros não bastam. Heterogeneidade estática não satisfaz CI6 sozinha. Detector explícito não é exigido. |
| CE1 | Não propõe, aplica nem avalia FL. | |
| CE2 | Séries temporais não são centrais. | |
| CE3 | Estudo secundário, survey, revisão ou mapeamento. | |
| CE4 | Workshop, short paper, resumo, pôster, editorial, capítulo, tese, literatura cinzenta ou preprint sem aceite. | Manuscrito aceito elegível não é excluído só por estar em repositório. |
| CE5 | Fora do período ou do idioma. | Registrar o motivo específico. |
| CE6 | Ocorrência duplicada da mesma publicação. | Aplicado na deduplicação; mantém-se um registro por publicação. |
| CE7 | Não investiga drift no contexto de FL em séries temporais, conforme CI6. | |

Qualidade metodológica serve à caracterização e não é critério de exclusão.

## 7. Regras de decisão D1–D3

- **D1 - aceite e tipo:** verificar primeiro metadados, veículo e estágio editorial; casos ambíguos, manuscritos em repositório e registros de 2027 exigem conferência da página oficial ou da versão aceita. DOI e indexação, sozinhos, não comprovam elegibilidade.
- **D2 - data de referência:** a elegibilidade temporal considera a data real da busca que recuperou o estudo; ano editorial, data online e aceite são registrados separadamente quando divergem.
- **D3 - acesso:** texto completo não obtido fica `pendente_acesso`, sem exclusão automática; não se exige acesso aberto.

## 8. Deduplicação

Todo registro exportado ganhou um identificador estável e localizadores de origem (arquivo e posição). Como a exportação da Scopus repete chaves, a chave BibTeX não serve de identidade. Pela regra automática, registros se agrupavam quando tinham DOI normalizado e título normalizado coincidentes, autoria compatível e no máximo um ano de diferença. Essa regra formou 105 grupos (103 pares e dois trios). Outros três pares (DynaGraph, FedGuard, FTWERF), que diferiam em abreviações ou grafia, foram confirmados na conferência. O resultado foi de 108 grupos, 110 ocorrências redundantes e **529 estudos únicos**. Oito registros não têm DOI e um não tem resumo, e nenhum deles foi excluído por esse motivo. Os 37 vínculos por DOI com a rodada anterior existem apenas para rastreabilidade; nenhuma decisão foi reaproveitada.

| Combinação de bases | Estudos |
|---|---:|
| Somente IEEE Xplore | 293 |
| Somente Scopus | 127 |
| Scopus e IEEE Xplore | 101 |
| Scopus e ACM DL | 5 |
| As três bases | 2 |
| Somente ACM DL | 1 |
| **Total** | **529** |

## 9. Procedimento de seleção

1. Lotes de dez estudos em ordem de identificador.
2. Primeira passagem por título, resumo e metadados. Exclusão só com evidência suficiente; dúvida vira `incerto`.
3. Avanços preliminares e dúvidas seguem ao texto completo, onde se verificam centralidade temporal, investigação de drift, contribuição federada e condições editoriais.
4. Cada decisão registra estudo, fase, critérios, justificativa, evidência localizável, responsável e data. A última decisão aprovada por ID é a vigente; eventos anteriores ficam preservados.
5. Um único pesquisador decide. Não há segundo revisor nem medida de concordância.

**Estado em 17/11/2026** (calculado de `estudos-em01.csv`):

| Situação | Título/resumo | Texto completo | Sem decisão | Total |
|---|---:|---:|---:|---:|
| `incluir_preliminar` | 33 | 37 | 0 | 70 |
| `excluir` | 63 | 114 | 0 | 177 |
| `incerto` | 21 | 32 | 0 | 53 |
| `pretriagem_aguardando_validacao` | 0 | 0 | 10 | 10 |
| `nao_avaliado` | 0 | 0 | 219 | 219 |
| **Total** | 117 | 183 | 229 | 529 |

Nenhum estudo chegou à inclusão final, e doze estão com acesso pendente.

**Amostra da RQ1.** Dado o prazo da entrega, a RQ1 foi respondida com dados de dez inclusões preliminares, escolhidas por regra fixa aplicada nesta ordem: (a) decisão na fase de texto completo (37 estudos); (b) evidência registrada sustentando CI1, CI2 e CI6, sem critério pendente e sem acesso pendente (28 estudos); (c) menores `study_id` até completar dez. A amostra resultante é S0070, S0090, S0104, S0106, S0111, S0123, S0124, S0136, S0138 e S0150. A lista foi confirmada pelo pesquisador em 17/11/2026, antes da extração. Os identificadores seguem a ordem da coleção, que começa pela exportação da Scopus; por isso os dez estão indexados na Scopus, e nenhum dos seis estudos com "forecasting" no título entrou na amostra.

## 10. Formulário de extração

A versão final está em `formulario-extracao.md`. Para cada valor, registram-se estudo, campo, valor, fonte, localizador, trecho de evidência, status (`reported`, `interpreted`, `not_reported`, `unclear`, `not_applicable`), revisor, data e aprovação. Quando o estudo é omisso, isso não é registrado como ausência. Até agora, o formulário foi aplicado a sete campos da RQ1 nos dez estudos da amostra (`extracao-rq1.csv`).

## 11. Síntese

A síntese usa codificação categórica, contagem de frequências, tabelas cruzadas (estudo × dimensões, família × representação temporal × topologia) e gráfico de bolhas tarefa × domínio. Segue-se a orientação de destacar semelhanças e diferenças em tabelas e de usar gráficos para os dados quantitativos. Toda afirmação de lacuna vale apenas para o conjunto analisado.

## 12. Uso de LLM

**Pré-triagem por título e resumo.** Um assistente baseado em LLM preparou, para cada lote, uma proposta por estudo (incluir preliminarmente, excluir ou incerto), com critérios e justificativa, a partir de título, resumo, palavras-chave e metadados. Isso ocorreu para 310 estudos. As propostas ficam registradas separadamente das decisões e não contam como decisão.

**Análise do texto completo.** O pesquisador submeteu o PDF de cada estudo encaminhado ao texto completo a outra LLM e repassou a resposta, que relatava evidências, páginas e seções para CI1, CI2, CI6 e condições editoriais. Isso vale para 222 estudos (`situacao_acesso = texto_fornecido_a_llm_pelo_pesquisador`). Até 29/10/2026 essas respostas foram recebidas como relatos do pesquisador; o esclarecimento de que vinham de outra LLM foi registrado nesse dia, e o fluxo foi formalizado no adendo E12-EM01-OP-1.1, aprovado na mesma data.

**Decisão.** Todas as decisões de seleção foram tomadas pelo pesquisador, que aprovou, alterou ou manteve como incerta cada proposta. Aprovação de decisão, acesso ao PDF, resposta de LLM e conferência humana são registrados como eventos distintos. Duas LLMs não equivalem a dois revisores.

**Limite.** A conferência dos trechos citados pelas análises de LLM contra os PDFs não foi feita para todos os casos. Por isso, "texto completo" na coluna `fase_decisao` significa decisão baseada em leitura do texto completo intermediada por LLM, e a inclusão final de qualquer estudo depende dessa conferência.

**Extração da RQ1.** Os 70 valores de `extracao-rq1.csv` foram codificados a partir dos resumos (29 valores) e das análises de LLM registradas na seleção (41 valores). Nenhum valor foi conferido no PDF; por isso `reviewed_by` está vazio e `review_approval = nao_revisado`.

**Redação.** Os textos do artigo e deste material externo, as tabelas e as figuras foram redigidos e gerados com apoio de LLM a partir dos registros do mapeamento (protocolo, planilhas de busca, seleção e extração). Os dados, os critérios e as decisões de seleção vêm desses registros e são do pesquisador. A versão final é de responsabilidade do autor.

## 13. Histórico de versões

| Data | Versão / evento | O que mudou | Motivo | Efeito nas contagens |
|---|---|---|---|---|
| 13/10/2026 | Protocolo v1 (Projeto 1) | População: FL em séries temporais desde 2016; drift, heterogeneidade, agrupamento e sincronismo como dimensões. Strings S0 (ampla), S1 (equilibrada), S2 (diagnóstica). | Escopo inicial aprovado. | S1 Scopus: 1.005 exibidos; S2: 300. |
| 13/10/2026 | Controle e calibração (E07/E08) | Quatro controles; S1 recuperou 2/4. S3 trocou as frases de FL por `federated`. | TIME-FFM e FedTime não usavam as frases exatas de FL. | S3 Scopus: 1.070 exibidos, 4/4 controles (+65 em relação a S1). |
| 13/10/2026 | Protocolo v2 / execução v1 (Projetos 2 e 3) | S3 executada em Scopus (1.070), IEEE Xplore (887) e ACM DL (29). | String final da rodada anterior. | 1.986 ocorrências; 370 redundantes; 1.616 únicos; 33 decisões por título/resumo. |
| 27/10/2026 | Emenda EM01 | Drift passou a ser condição de entrada (CI6/CE7); período principal 2020–2026, exceção editorial 2027; RQs reformuladas (avaliação na RQ4, agrupamento na RQ5); critérios E05-EM01-1.0. | Revisão do escopo com a orientadora após a primeira rodada. | Nova coleção; nenhuma decisão anterior transferida. |
| 27/10/2026 | Controle EM01 e S4 | Fed-DCL como controle positivo; S4 = FL AND séries temporais AND drift. | Testar o recorte com os três conceitos. | S4 Scopus: 11 exibidos, 0/1 controle. |
| 27/10/2026 | S5 final (EM01-BUSCA-1.0) | Bloco de séries temporais removido da busca e transferido à seleção (CI2). | Perda do controle atribuída ao bloco temporal pelos diagnósticos por DOI. | Scopus 235, IEEE 396, ACM 8: 639 ocorrências; 110 redundantes; 529 únicos. |
| 27/10/2026 | ACM: correções de sintaxe | Tentativas com campos incompletos (7 resultados) e com filtro 2023–2026 (8) não adotadas; adotada execução sem filtro de data (8). | Interface não aceitava `Keywords` nem 2027. | Sem efeito no total adotado. |
| 29/10/2026 | Adendo E12-EM01-OP-1.1 | Origem das análises de texto completo esclarecida (outra LLM); fluxo de seleção assistida formalizado. | Registrar com transparência a origem das evidências. | Nenhum efeito nas buscas; decisões anteriores preservadas. |
| 29/10–17/11/2026 | Seleção EM01 | 31 lotes preparados; 30 avaliados. | Execução do protocolo. | 300 decisões; 10 propostas pendentes; 219 não avaliados. |

## 14. Rodada anterior (preservada, fora do artigo)

Na rodada anterior, a string adotada foi S3 (`TITLE-ABS-KEY ( federated AND ( "time series" OR "time-series" ) )` com 2016–2026, estágio final, Article/Conference Paper e inglês), e suas execuções constam de `buscas-em01.csv` com `rodada = anterior (S0-S3)`. As 1.616 publicações únicas e as 33 decisões daquela rodada não integram a coleção EM01. O artigo não as utiliza porque escopo, período e consulta mudaram, e as duas coleções não são comparáveis como medida de precisão.
