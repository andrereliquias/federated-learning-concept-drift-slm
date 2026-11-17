#!/usr/bin/env python3
"""Gera os materiais do Projeto 5 a partir dos registros do mapeamento EM01.

Entradas (somente leitura, caminhos relativos à raiz do repositório):
  docs/mapeamento/dados/em01/acompanhamento-estudos-em01.csv
  docs/mapeamento/dados/em01/colecao-em01-v1.csv
  docs/mapeamento/buscas.csv
  projetos-final/projeto-5/extracao-rq1.csv

Saídas (em projetos-final/projeto-5/):
  estudos-em01.csv, buscas-em01.csv, contagens.json
  artigo/contagens.tex, artigo/tabelas/*.tex, artigo/figuras/*.pdf,
  artigo/referencias-estudos.bib

Uso, a partir da raiz do repositório:
  python3 projetos-final/projeto-5/scripts/gerar_materiais.py
Requer matplotlib (pip install matplotlib).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "projetos-final" / "projeto-5"
ART = OUT / "artigo"
TAB = ART / "tabelas"
FIG = ART / "figuras"

ACOMP = ROOT / "docs/mapeamento/dados/em01/acompanhamento-estudos-em01.csv"
COLECAO = ROOT / "docs/mapeamento/dados/em01/colecao-em01-v1.csv"
BUSCAS = ROOT / "docs/mapeamento/buscas.csv"
EXTRACAO = OUT / "extracao-rq1.csv"

# Amostra da RQ1 (critério registrado no PROTOCOLO.md, seção 9) - recalculada abaixo e conferida.
N_AMOSTRA = 10

# Execuções que compõem a coleção EM01 (registro de buscas).
BUSCAS_ADOTADAS = {
    "SCOPUS-S5-PILOTO-20261027-1315": "Scopus",
    "IEEE-S5-20261027-1332": "IEEE Xplore",
    "ACM-S5-SEM-DATA-20261027-01": "ACM DL",
}

SITUACOES = ["incluir_preliminar", "excluir", "incerto",
             "pretriagem_aguardando_validacao", "nao_avaliado"]

PERIODICO = {"Article", "IEEE Journals", "IEEE Early Access Articles", "TUP Journals"}
CONFERENCIA = {"Conference paper", "IEEE Conferences", "inproceedings",
               "Additional Conference Content Conferences"}

# Rótulos de exibição (com acentos) para os valores da extração.
ROTULO = {
    "classificacao": "Classification",
    "deteccao de intrusao": "Intrusion detection",
    "deteccao de anomalias": "Anomaly detection",
    "outra (predicao de sobrevivencia)": "Other (survival)",
    "nao identificada": "Not identified",
    "previsao": "Forecasting",
    "benchmarks de fluxo (sem dominio unico)": "Stream benchmarks",
    "redes e seguranca (IoT)": "Networks and security",
    "redes e seguranca (trafego de borda)": "Networks and security",
    "redes e seguranca (fog/IoT)": "Networks and security",
    "computacao de borda (multiplos datasets)": "Edge computing",
    "reconhecimento de atividades humanas": "Human activity",
    "sensoriamento industrial (WSN)": "Industrial sensing",
    "saude": "Healthcare",
    "fluxo de dados ordenado": "Ordered stream",
    "sequencia/serie explicita": "Explicit sequence",
    "multivariada": "Multivariate",
    "nao identificado nas fontes consultadas": "Not identified",
    "centralizada (servidor)": "Server",
    "centralizada com agrupamento de clientes": "Server + groups",
    "por comunidades de clientes": "Communities",
    "descentralizada (P2P/gossip)": "P2P/gossip",
    "horizontal": "Horizontal",
    "prototipos": "Prototypes",
    "rede recorrente": "Recurrent network",
    "aprendizado continuo com replay": "Continual learning with replay",
    "rede neural com atencao (semissupervisionada)": "Attention network",
    "estimacao de densidade (sketch)": "Density sketch",
    "topologia P2P adaptativa": "Adaptive P2P topology",
    "aprendizado por reforco (bandit)": "Reinforcement learning (bandit)",
}

TAREFAS_ORDEM = ["Forecasting", "Classification", "Anomaly detection",
                 "Intrusion detection", "Other (survival)", "Not identified"]
DOMINIOS_ORDEM = ["Stream benchmarks", "Edge computing", "Networks and security",
                  "Industrial sensing", "Human activity", "Healthcare"]


def ler_csv(caminho: Path) -> list[dict]:
    with caminho.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def escrever_csv(caminho: Path, linhas: list[dict], campos: list[str]) -> None:
    with caminho.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)


def tex(s: str) -> str:
    """Escapa caracteres especiais do LaTeX."""
    rep = {"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "$": r"\$"}
    return "".join(rep.get(c, c) for c in s)


def fmt(n: int) -> str:
    """Separador de milhar em inglês."""
    return f"{n:,}"


def pct(a: int, b: int) -> str:
    return f"{100 * a / b:.1f}"


def tipo_veiculo(tipo: str) -> str:
    if tipo in PERIODICO:
        return "periodico"
    if tipo in CONFERENCIA:
        return "conferencia"
    raise ValueError(f"tipo de publicação não mapeado: {tipo!r}")


def encurtar(texto: str, limite: int = 420) -> str:
    texto = re.sub(r"^EM01-PROT-1\.0-RC1(; E12-EM01-OP-1\.1)?\.\s*", "", texto.strip())
    texto = re.sub(r"\S*docs/\S+", "", texto)  # nenhum caminho interno
    texto = re.sub(r"\s+", " ", texto).strip()
    if len(texto) <= limite:
        return texto
    corte = texto[:limite]
    ponto = corte.rfind(". ")
    return (corte[: ponto + 1] if ponto > 150 else corte.rstrip() + " [...]")


def selecionar_amostra(estudos: list[dict]) -> list[str]:
    """Critério (a) texto completo, (b) sem critério pendente nem acesso pendente, (c) menor ID."""
    elegiveis = [
        e for e in estudos
        if e["situacao_atual"] == "incluir_preliminar"
        and e["fase_decisao"] == "texto_completo"
        and not e["criterios_pendentes"].strip()
        and e["situacao_acesso"] != "pendente_acesso"
    ]
    return sorted(e["study_id"] for e in elegiveis)[:N_AMOSTRA], len(elegiveis)


def main() -> int:
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)

    estudos = ler_csv(ACOMP)
    colecao = ler_csv(COLECAO)
    buscas = ler_csv(BUSCAS)
    extracao = ler_csv(EXTRACAO)
    por_id = {e["study_id"]: e for e in estudos}

    amostra, n_elegiveis_amostra = selecionar_amostra(estudos)
    ids_extracao = sorted({x["study_id"] for x in extracao})
    if ids_extracao != amostra:
        print("ERRO: extracao-rq1.csv não corresponde à amostra recalculada", ids_extracao, amostra)
        return 1

    # ------------------------------------------------------------------ contagens
    c = OrderedDict()
    c["unicos"] = len(estudos)
    c["unicos_colecao"] = len(colecao)
    ocorr = Counter()
    for reg in colecao:
        for loc in json.loads(reg["source_locators"]):
            ocorr[loc["id"].split("-")[1]] += 1
    c["ocorr_scopus"], c["ocorr_ieee"], c["ocorr_acm"] = ocorr["SCOPUS"], ocorr["IEEE"], ocorr["ACM"]
    c["ocorrencias"] = sum(ocorr.values())
    c["redundantes"] = c["ocorrencias"] - c["unicos"]
    sit = Counter(e["situacao_atual"] for e in estudos)
    for s in SITUACOES:
        c[s] = sit.get(s, 0)
    c["decisoes"] = c["incluir_preliminar"] + c["excluir"] + c["incerto"]
    c["pre_analisados"] = c["decisoes"] + c["pretriagem_aguardando_validacao"]
    fase = Counter(e["fase_decisao"] for e in estudos if e["decisao_pesquisador"])
    c["fase_titulo_resumo"], c["fase_texto_completo"] = fase["titulo_resumo"], fase["texto_completo"]
    c["acesso_llm"] = sum(e["situacao_acesso"] == "texto_fornecido_a_llm_pelo_pesquisador" for e in estudos)
    c["acesso_pendente"] = sum(e["situacao_acesso"] == "pendente_acesso" for e in estudos)
    c["com_recomendacao_inicial"] = sum(bool(e["recomendacao_inicial_assistente"]) for e in estudos)
    inc = [e for e in estudos if e["situacao_atual"] == "incluir_preliminar"]
    c["inc_texto_completo"] = sum(e["fase_decisao"] == "texto_completo" for e in inc)
    c["inc_titulo_resumo"] = sum(e["fase_decisao"] == "titulo_resumo" for e in inc)
    c["inc_elegiveis_amostra"] = n_elegiveis_amostra
    c["amostra"] = len(amostra)
    c["inc_periodico"] = sum(tipo_veiculo(e["tipo_publicacao"]) == "periodico" for e in inc)
    c["inc_conferencia"] = len(inc) - c["inc_periodico"]
    am = [por_id[i] for i in amostra]
    c["am_periodico"] = sum(tipo_veiculo(e["tipo_publicacao"]) == "periodico" for e in am)
    c["am_conferencia"] = len(am) - c["am_periodico"]
    c["inc_2025_2026"] = sum(e["ano"] in ("2025", "2026") for e in inc)
    c["unicos_2025_2026"] = sum(e["ano"] in ("2025", "2026") for e in estudos)
    c["inc_multibase"] = sum(";" in e["bases"] for e in inc)
    # Indicador lexical simples, usado só para discutir o efeito da regra de amostragem.
    prev = [e for e in inc if "forecast" in e["titulo"].lower()]
    c["inc_titulo_forecast"] = len(prev)
    c["inc_titulo_forecast_tc"] = sum(e["fase_decisao"] == "texto_completo" for e in prev)
    c["inc_titulo_forecast_ids"] = [e["study_id"] for e in prev]
    combos = Counter(e["bases"] for e in estudos)
    c["combos"] = dict(combos)

    # Fed-DCL (controle positivo) na coleção.
    fed = [e for e in estudos if e["doi"].lower() == "10.1109/icnepe67923.2025.11384325"]
    c["controle_id"] = fed[0]["study_id"] if fed else ""
    c["controle_situacao"] = fed[0]["situacao_atual"] if fed else "nao_encontrado"

    # Exclusões por critério.
    excl = [e for e in estudos if e["situacao_atual"] == "excluir"]
    por_crit, unico, fase_crit = Counter(), Counter(), Counter()
    for e in excl:
        crits = [x for x in e["criterios_exclusao"].split(";") if x]
        for k in crits:
            por_crit[k] += 1
            fase_crit[(k, e["fase_decisao"])] += 1
        if len(crits) == 1:
            unico[crits[0]] += 1
    c["excl_multicriterio"] = sum(len([x for x in e["criterios_exclusao"].split(";") if x]) > 1 for e in excl)
    c["excl_sem_criterio"] = sum(not e["criterios_exclusao"] for e in excl)
    c["excl_por_criterio"] = dict(por_crit)

    # Situação × fase.
    sit_fase = Counter((e["situacao_atual"], e["fase_decisao"]) for e in estudos)

    # ------------------------------------------------------------------ estudos-em01.csv
    campos = ["study_id", "titulo", "autores", "ano", "veiculo", "tipo_publicacao", "doi", "url",
              "bases", "situacao", "fase_decisao", "criterios_inclusao_atendidos", "criterio_exclusao",
              "criterios_pendentes", "justificativa", "situacao_acesso", "usado_na_rq1"]
    linhas = []
    for e in sorted(estudos, key=lambda x: x["study_id"]):
        linhas.append({
            "study_id": e["study_id"], "titulo": e["titulo"], "autores": e["autores"], "ano": e["ano"],
            "veiculo": e["veiculo"], "tipo_publicacao": e["tipo_publicacao"], "doi": e["doi"],
            "url": e["url"], "bases": e["bases"], "situacao": e["situacao_atual"],
            "fase_decisao": e["fase_decisao"], "criterios_inclusao_atendidos": e["criterios_inclusao"],
            "criterio_exclusao": e["criterios_exclusao"], "criterios_pendentes": e["criterios_pendentes"],
            "justificativa": encurtar(e["justificativa_decisao"]), "situacao_acesso": e["situacao_acesso"],
            "usado_na_rq1": "sim" if e["study_id"] in amostra else "nao",
        })
    escrever_csv(OUT / "estudos-em01.csv", linhas, campos)

    # ------------------------------------------------------------------ buscas-em01.csv
    campos_b = ["search_id", "rodada", "adotada_na_colecao_em01", "database", "query_version",
                "query_exact", "search_fields", "filters", "executed_at_with_timezone",
                "results_shown", "records_exported", "export_file", "url", "notes", "validated_by_researcher"]
    linhas_b = []
    for b in buscas:
        rodada = "EM01" if "20261027" in b["search_id"] or "EM01" in b["search_id"] or "S5" in b["search_id"] or "S4" in b["search_id"] else "anterior (S0-S3)"
        linhas_b.append({
            **{k: b[k] for k in b if k in campos_b},
            "rodada": rodada,
            "adotada_na_colecao_em01": "sim" if b["search_id"] in BUSCAS_ADOTADAS else "nao",
            "export_file": Path(b["export_file"]).name if b["export_file"] else "",
        })
    escrever_csv(OUT / "buscas-em01.csv", linhas_b, campos_b)
    adotadas = {b["search_id"]: b for b in buscas if b["search_id"] in BUSCAS_ADOTADAS}
    for sid, base in BUSCAS_ADOTADAS.items():
        exp = int(adotadas[sid]["records_exported"])
        chave = {"Scopus": "ocorr_scopus", "IEEE Xplore": "ocorr_ieee", "ACM DL": "ocorr_acm"}[base]
        if exp != c[chave]:
            print(f"DIVERGÊNCIA: {base} exportados={exp} ocorrências na coleção={c[chave]}")
    c["exibidos_scopus"] = int(adotadas["SCOPUS-S5-PILOTO-20261027-1315"]["results_shown"])
    c["exibidos_ieee"] = int(adotadas["IEEE-S5-20261027-1332"]["results_shown"])
    c["exibidos_acm"] = int(adotadas["ACM-S5-SEM-DATA-20261027-01"]["results_shown"])

    # ------------------------------------------------------------------ extração RQ1
    ext = {}
    for x in extracao:
        ext.setdefault(x["study_id"], {})[x["field"]] = x
    def val(sid, campo):
        return ROTULO.get(ext[sid][campo]["value"], ext[sid][campo]["value"])
    def st(sid, campo):
        return ext[sid][campo]["status"]
    status_cont = Counter(x["status"] for x in extracao)
    c["ext_registros"] = len(extracao)
    c["ext_reported"] = status_cont["reported"]
    c["ext_interpreted"] = status_cont["interpreted"]
    c["ext_unclear"] = status_cont["unclear"]
    fontes = Counter()
    for x in extracao:
        fontes["llm" if "analise_llm_pdf" in x["source_path"] else "resumo"] += 1
    c["ext_fonte_llm"] = fontes["llm"]
    c["ext_fonte_resumo"] = fontes["resumo"]
    tarefas = Counter(val(s, "ts_task") for s in amostra)
    dominios = Counter(val(s, "application_domain") for s in amostra)
    familias = Counter(val(s, "approach_family") for s in amostra)
    topologias = Counter(val(s, "federated_topology") for s in amostra)
    reps = Counter(val(s, "temporal_representation") for s in amostra)
    dims = Counter(val(s, "series_dimensionality") for s in amostra)
    parts = Counter(val(s, "federated_setting") for s in amostra)
    c["rq1_tarefas"], c["rq1_dominios"], c["rq1_familias"] = dict(tarefas), dict(dominios), dict(familias)
    c["rq1_topologias"], c["rq1_representacao"] = dict(topologias), dict(reps)
    c["rq1_dimensao"], c["rq1_particao"] = dict(dims), dict(parts)
    c["rq1_ci2_interpretado"] = sum("CI2 Interpretado" in por_id[s]["justificativa_decisao"]
                                    or "suporte interpretado" in por_id[s]["justificativa_decisao"]
                                    or "temporalidade Interpretada" in por_id[s]["justificativa_decisao"]
                                    for s in amostra)

    # ------------------------------------------------------------------ contagens.tex
    def macro(nome, valor):
        return f"\\newcommand{{\\{nome}}}{{{valor}}}\n"
    m = "% Gerado por scripts/gerar_materiais.py. Não editar.\n"
    nomes = {
        "nUnicos": c["unicos"], "nOcorrencias": c["ocorrencias"], "nRedundantes": c["redundantes"],
        "nScopus": c["ocorr_scopus"], "nIEEE": c["ocorr_ieee"], "nACM": c["ocorr_acm"],
        "nExibScopus": c["exibidos_scopus"], "nExibIEEE": c["exibidos_ieee"], "nExibACM": c["exibidos_acm"],
        "nInclPrelim": c["incluir_preliminar"], "nExcl": c["excluir"], "nIncerto": c["incerto"],
        "nPretriagem": c["pretriagem_aguardando_validacao"], "nNaoAvaliado": c["nao_avaliado"],
        "nDecisoes": c["decisoes"], "nPreAnalisados": c["pre_analisados"],
        "nFaseTR": c["fase_titulo_resumo"], "nFaseTC": c["fase_texto_completo"],
        "nAcessoLLM": c["acesso_llm"], "nAcessoPend": c["acesso_pendente"],
        "nRecInicial": c["com_recomendacao_inicial"],
        "nIncTC": c["inc_texto_completo"], "nIncTR": c["inc_titulo_resumo"],
        "nIncElegAmostra": c["inc_elegiveis_amostra"], "nAmostra": c["amostra"],
        "nIncPer": c["inc_periodico"], "nIncConf": c["inc_conferencia"],
        "nAmPer": c["am_periodico"], "nAmConf": c["am_conferencia"],
        "nIncertoTempDrift": sum(("CI2" in e["criterios_pendentes"] or "CI6" in e["criterios_pendentes"])
                                 for e in estudos if e["situacao_atual"] == "incerto"),
        "nIncertoTC": sit_fase[("incerto", "texto_completo")],
        "nAmScopus": sum("SCOPUS" in por_id[s]["bases"] for s in amostra),
        "nIncRecentes": c["inc_2025_2026"], "nUnicosRecentes": c["unicos_2025_2026"],
        "nIncMultibase": c["inc_multibase"],
        "nIncForecast": c["inc_titulo_forecast"], "nIncForecastTC": c["inc_titulo_forecast_tc"],
        "pctIncMultibase": pct(c["inc_multibase"], c["incluir_preliminar"]),
        "nMultibase": sum(v for k, v in combos.items() if ";" in k),
        "nExclMulti": c["excl_multicriterio"],
        "nExtRegistros": c["ext_registros"], "nExtReported": c["ext_reported"],
        "nExtInterpreted": c["ext_interpreted"], "nExtUnclear": c["ext_unclear"],
        "nExtFonteLLM": c["ext_fonte_llm"], "nExtFonteResumo": c["ext_fonte_resumo"],
        "nCIIInterp": c["rq1_ci2_interpretado"],
        "pctPreAnalisados": pct(c["pre_analisados"], c["unicos"]),
        "pctNaoAvaliado": pct(c["nao_avaliado"], c["unicos"]),
        "pctInclDecisoes": pct(c["incluir_preliminar"], c["decisoes"]),
        "pctExclDecisoes": pct(c["excluir"], c["decisoes"]),
        "pctIncertoDecisoes": pct(c["incerto"], c["decisoes"]),
        "pctRedundantes": pct(c["redundantes"], c["ocorrencias"]),
        "pctIncRecentes": pct(c["inc_2025_2026"], c["incluir_preliminar"]),
        "pctUnicosRecentes": pct(c["unicos_2025_2026"], c["unicos"]),
        "pctExtUnclear": pct(c["ext_unclear"], c["ext_registros"]),
        "pctExtInterpreted": pct(c["ext_interpreted"], c["ext_registros"]),
        "pctExtFonteLLM": pct(c["ext_fonte_llm"], c["ext_registros"]),
        "nCEUm": por_crit.get("CE1", 0), "nCEDois": por_crit.get("CE2", 0), "nCETres": por_crit.get("CE3", 0),
        "nCEQuatro": por_crit.get("CE4", 0), "nCECinco": por_crit.get("CE5", 0), "nCESete": por_crit.get("CE7", 0),
        "nCombScopusIEEE": combos.get("IEEE;SCOPUS", 0), "nCombTres": combos.get("ACM;IEEE;SCOPUS", 0),
        "nSoIEEE": combos.get("IEEE", 0), "nSoScopus": combos.get("SCOPUS", 0),
        "nSoACM": combos.get("ACM", 0), "nCombACMScopus": combos.get("ACM;SCOPUS", 0),
        "controleID": c["controle_id"].replace("EM01-", ""),
    }
    for k, v in nomes.items():
        m += macro(k, fmt(v) if isinstance(v, int) else v)
    (ART / "contagens.tex").write_text(m, encoding="utf-8")

    # ------------------------------------------------------------------ tabelas
    # Buscas por base.
    t = ["\\begin{tabular}{@{}lrrr@{}}", "\\toprule",
         "Database & Shown & Exported & Share of occurrences (\\%) \\\\", "\\midrule"]
    for nome, exib, chave in [("Scopus", c["exibidos_scopus"], "ocorr_scopus"),
                              ("IEEE Xplore", c["exibidos_ieee"], "ocorr_ieee"),
                              ("ACM DL", c["exibidos_acm"], "ocorr_acm")]:
        t.append(f"{nome} & {fmt(exib)} & {fmt(c[chave])} & {pct(c[chave], c['ocorrencias'])} \\\\")
    t += ["\\midrule", f"Total occurrences & & {fmt(c['ocorrencias'])} & 100.0 \\\\",
          f"Redundant occurrences removed & & {fmt(c['redundantes'])} & {pct(c['redundantes'], c['ocorrencias'])} \\\\",
          f"Unique studies & & {fmt(c['unicos'])} & \\\\", "\\bottomrule", "\\end{tabular}"]
    (TAB / "buscas.tex").write_text("\n".join(t) + "\n", encoding="utf-8")

    # Exclusões por critério × fase.
    desc = {"CE1": "No federated learning", "CE2": "Time series not central",
            "CE3": "Secondary study", "CE4": "Not a full peer-reviewed paper",
            "CE5": "Out of period or language", "CE7": "Drift not investigated (CI6)"}
    t = ["\\begin{tabular}{@{}llrrrr@{}}", "\\toprule",
         "Criterion & Description & Title/abstract & Full text & Total & Sole criterion \\\\", "\\midrule"]
    for k in ["CE1", "CE2", "CE3", "CE4", "CE5", "CE7"]:
        if por_crit.get(k, 0) == 0 and k == "CE5":
            t.append(f"{k} & {desc[k]} & 0 & 0 & 0 & 0 \\\\")
            continue
        t.append(f"{k} & {desc[k]} & {fase_crit[(k, 'titulo_resumo')]} & {fase_crit[(k, 'texto_completo')]} & "
                 f"{por_crit[k]} & {unico.get(k, 0)} \\\\")
    excl_tr = sum(1 for e in excl if e["fase_decisao"] == "titulo_resumo")
    excl_tc = sum(1 for e in excl if e["fase_decisao"] == "texto_completo")
    t += ["\\midrule", f"\\multicolumn{{2}}{{@{{}}l}}{{Excluded studies}} & {excl_tr} & {excl_tc} & {len(excl)} & \\\\",
          "\\bottomrule", "\\end{tabular}"]
    (TAB / "exclusoes.tex").write_text("\n".join(t) + "\n", encoding="utf-8")

    # Situação × fase.
    rot_sit = {"incluir_preliminar": "Preliminary inclusion", "excluir": "Excluded", "incerto": "Uncertain",
               "pretriagem_aguardando_validacao": "Pre-screened, awaiting decision", "nao_avaliado": "Not assessed"}
    t = ["\\begin{tabular}{@{}lrrrr@{}}", "\\toprule",
         "Status & Title/abstract & Full text & No decision & Total (\\%) \\\\", "\\midrule"]
    for s in SITUACOES:
        tr, tc_, nd = sit_fase[(s, "titulo_resumo")], sit_fase[(s, "texto_completo")], sit_fase[(s, "")]
        t.append(f"{rot_sit[s]} & {tr} & {tc_} & {nd} & {sit[s]} ({pct(sit[s], c['unicos'])}) \\\\")
    t += ["\\midrule", f"Total & {c['fase_titulo_resumo']} & {c['fase_texto_completo']} & "
          f"{sit_fase[('pretriagem_aguardando_validacao', '')] + sit_fase[('nao_avaliado', '')]} & {c['unicos']} (100.0) \\\\",
          "\\bottomrule", "\\end{tabular}"]
    (TAB / "situacao.tex").write_text("\n".join(t) + "\n", encoding="utf-8")

    # Tabela dos 10 estudos.
    t = ["\\begin{tabular}{@{}llrP{6.2cm}l@{}}", "\\toprule",
         "ID & Reference & Year & Venue & Type \\\\", "\\midrule"]
    for s in amostra:
        e = por_id[s]
        tipo = "J" if tipo_veiculo(e["tipo_publicacao"]) == "periodico" else "C"
        t.append(f"{s.replace('EM01-', '')} & \\cite{{{s.replace('-', '')}}} & {e['ano']} & "
                 f"{tex(e['veiculo'])} & {tipo} \\\\")
    t += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "estudos-rq1.tex").write_text("\n".join(t) + "\n", encoding="utf-8")

    # Matriz estudo × dimensões (RQ1).
    def marca(sid, campo):
        v = val(sid, campo)
        s_ = st(sid, campo)
        suf = "" if s_ == "reported" else ("$^{i}$" if s_ == "interpreted" else "$^{?}$")
        return tex(v) + suf
    t = ["\\begin{tabular}{@{}lP{2.0cm}P{2.0cm}P{1.75cm}P{1.6cm}P{1.6cm}P{2.25cm}@{}}", "\\toprule",
         "ID & Task & Domain & Temporal data & Dim. & Federation & Approach family \\\\", "\\midrule"]
    for s in amostra:
        fed_ = marca(s, "federated_topology") + "; " + marca(s, "federated_setting")
        t.append(" & ".join([s.replace("EM01-", ""), marca(s, "ts_task"), marca(s, "application_domain"),
                             marca(s, "temporal_representation"), marca(s, "series_dimensionality"),
                             fed_, marca(s, "approach_family")]) + " \\\\")
    t += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "rq1-matriz.tex").write_text("\n".join(t) + "\n", encoding="utf-8")

    # Cruzamento família × representação temporal × topologia.
    fams = [f for f, _ in familias.most_common()]
    t = ["\\begin{tabular}{@{}P{4.1cm}P{2.8cm}P{3.4cm}P{3.2cm}@{}}", "\\toprule",
         "Approach family & Studies & Temporal data & Federation topology \\\\", "\\midrule"]
    for f in fams:
        ss = [s for s in amostra if val(s, "approach_family") == f]
        rr = ", ".join(sorted({val(s, "temporal_representation") for s in ss}))
        tt = ", ".join(sorted({val(s, "federated_topology") for s in ss}))
        ids = ", ".join(x.replace("EM01-", "") for x in ss)
        t.append(f"{tex(f)} & {len(ss)} ({ids}) & {tex(rr)} & {tex(tt)} \\\\")
    t += ["\\bottomrule", "\\end{tabular}"]
    (TAB / "familias.tex").write_text("\n".join(t) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------ figuras
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
                         "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42})
    AZUL, CINZA, ESCURO = "#2b5d8a", "#b9c4cf", "#1f2933"

    # Sobreposição entre bases.
    rot_comb = {"IEEE": "IEEE only", "SCOPUS": "Scopus only", "IEEE;SCOPUS": "Scopus + IEEE",
                "ACM;SCOPUS": "Scopus + ACM", "ACM;IEEE;SCOPUS": "All three", "ACM": "ACM only"}
    ordem = sorted(combos, key=lambda k: combos[k])
    fig, ax = plt.subplots(figsize=(4.6, 1.9))
    ax.barh([rot_comb[k] for k in ordem], [combos[k] for k in ordem], color=AZUL, height=0.6)
    for i, k in enumerate(ordem):
        ax.text(combos[k] + 3, i, str(combos[k]), va="center", fontsize=8, color=ESCURO)
    ax.set_xlabel("Unique studies")
    ax.set_xlim(0, max(combos.values()) * 1.15)
    fig.tight_layout()
    fig.savefig(FIG / "sobreposicao.pdf")
    plt.close(fig)

    # Anos: preliminares × amostra.
    anos = sorted({e["ano"] for e in inc})
    n_inc = [sum(e["ano"] == a for e in inc) for a in anos]
    n_am = [sum(por_id[s]["ano"] == a for s in amostra) for a in anos]
    fig, ax = plt.subplots(figsize=(4.6, 2.0))
    x = range(len(anos))
    ax.bar(x, [a - b for a, b in zip(n_inc, n_am)], bottom=n_am, color=CINZA, label="Other preliminary inclusions")
    ax.bar(x, n_am, color=AZUL, label="Analysed for RQ1")
    for i, v in enumerate(n_inc):
        ax.text(i, v + 0.6, str(v), ha="center", fontsize=8, color=ESCURO)
    ax.set_xticks(list(x), anos)
    ax.set_ylabel("Studies")
    ax.set_ylim(0, max(n_inc) * 1.2)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "anos.pdf")
    plt.close(fig)

    # Bolhas tarefa × domínio.
    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    for yi, tarefa in enumerate(TAREFAS_ORDEM):
        for xi, dom in enumerate(DOMINIOS_ORDEM):
            ss = [s for s in amostra if val(s, "ts_task") == tarefa and val(s, "application_domain") == dom]
            if ss:
                ax.scatter(xi, yi, s=260 * len(ss), color=AZUL, alpha=0.75, edgecolors="white", zorder=3)
                ax.text(xi, yi, str(len(ss)), ha="center", va="center", color="white", fontsize=8, zorder=4)
                ax.text(xi + 0.16 + 0.05 * len(ss), yi, "\n".join(x.replace("EM01-", "") for x in ss),
                        va="center", fontsize=6.5, color=ESCURO, zorder=4)
    ax.set_xticks(range(len(DOMINIOS_ORDEM)), [d.replace(" ", "\n", 1) for d in DOMINIOS_ORDEM], fontsize=7.5)
    ax.set_yticks(range(len(TAREFAS_ORDEM)), TAREFAS_ORDEM, fontsize=7.5)
    ax.set_xlim(-0.5, len(DOMINIOS_ORDEM) - 0.3)
    ax.set_ylim(-0.6, len(TAREFAS_ORDEM) - 0.4)
    ax.grid(True, color="#e5e7eb", zorder=0)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(FIG / "bolhas-rq1.pdf")
    plt.close(fig)

    # Frequência por família.
    fam_ord = sorted(familias, key=lambda f: (familias[f], f))
    fig, ax = plt.subplots(figsize=(4.6, 2.0))
    ax.barh(fam_ord, [familias[f] for f in fam_ord], color=AZUL, height=0.6)
    for i, f in enumerate(fam_ord):
        ss = [x.replace("EM01-", "") for x in amostra if val(x, "approach_family") == f]
        ax.text(familias[f] + 0.05, i, ", ".join(ss), va="center", fontsize=7, color=ESCURO)
    ax.set_xlabel("Studies")
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xlim(0, 3.4)
    ax.tick_params(axis="y", labelsize=7.5)
    fig.tight_layout()
    fig.savefig(FIG / "familias-rq1.pdf")
    plt.close(fig)

    # ------------------------------------------------------------------ bib dos estudos
    bib = ["% Gerado por scripts/gerar_materiais.py a partir dos metadados de acompanhamento-estudos-em01.csv.",
           "% Paginação não consta da exportação consolidada e não foi acrescentada.", ""]
    for s in amostra + ([c["controle_id"]] if c["controle_id"] else []):
        e = por_id[s]
        chave = s.replace("-", "")
        tipo = tipo_veiculo(e["tipo_publicacao"])
        campo_v = "journal" if tipo == "periodico" else "booktitle"
        bib.append(f"@{'article' if tipo == 'periodico' else 'inproceedings'}{{{chave},")
        bib.append(f"  author = {{{tex(e['autores'])}}},")
        bib.append(f"  title = {{{{{tex(e['titulo'])}}}}},")
        bib.append(f"  {campo_v} = {{{tex(e['veiculo'])}}},")
        bib.append(f"  year = {{{e['ano']}}},")
        if e["doi"]:
            bib.append(f"  doi = {{{e['doi']}}},")
        bib.append("}\n")
    (ART / "referencias-estudos.bib").write_text("\n".join(bib), encoding="utf-8")

    (OUT / "contagens.json").write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in c.items() if not isinstance(v, dict)}, ensure_ascii=False))
    print("amostra:", amostra)
    return 0


if __name__ == "__main__":
    sys.exit(main())
