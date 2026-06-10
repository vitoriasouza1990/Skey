import os
import pandas as pd
from config import PASTA_SAIDA_DADOS

# =========================================================
# PATH HELPER
# =========================================================
def _p(*names):
    os.makedirs(PASTA_SAIDA_DADOS, exist_ok=True)
    return os.path.join(PASTA_SAIDA_DADOS, *names)

# =========================================================
# APPEND CSV
# =========================================================
def _append_csv(df: pd.DataFrame, caminho: str):
    if df is None or df.empty:
        print("[WARN] CSV vazio ->", caminho)
        return

    print("\n[SALVANDO CSV]:", caminho)
    print(df, "\n")

    if os.path.exists(caminho):
        df.to_csv(caminho, mode="a", header=False, index=False)
    else:
        df.to_csv(caminho, mode="w", header=True, index=False)

# =========================================================
# NORMALIZA SIM/NAO
# =========================================================
def _simnao(v):
    if v is None:
        return ""

    s = str(v).strip().lower()

    if s in {"sim", "s", "yes", "y", "true", "1"}:
        return "Sim"

    if s in {"não", "nao", "n", "no", "false", "0"}:
        return "Não"

    return s.capitalize()

# =========================================================
# =========================================================
# EXPORTACOES
# =========================================================
# =========================================================

def exp_resumo(resultado, id):
    df = pd.DataFrame([{
        "RESUMO": resultado.get("LLM_RESUMO_ATENDIMENTO", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__resumo.csv"))


def exp_nps(resultado, id):
    df = pd.DataFrame([{
        "NOTA": resultado.get("LLM_NPS", ""),
        "JUSTIFICATIVA": resultado.get("JUSTIFICATIVA_LLM_NPS", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__nps.csv"))


def exp_ouvidoria(resultado, id):
    df = pd.DataFrame([{
        "RISCO_OUVIDORIA": _simnao(resultado.get("LLM_RISCO_OUVIDORIA")),
        "JUSTIFICATIVA": resultado.get("JUSTIFICATIVA_LLM_RISCO_OUVIDORIA", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__risco_ouvidoria.csv"))


def exp_acao_judicial(resultado, id):
    df = pd.DataFrame([{
        "RISCO_ACAO_JUDICIAL": _simnao(resultado.get("LLM_RISCO_JUDICIAL")),
        "JUSTIFICATIVA": resultado.get("JUSTIFICATIVA_LLM_RISCO_JUDICIAL", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__acao_judicial.csv"))


def exp_churn(resultado, id):
    df = pd.DataFrame([{
        "RESPOSTA": _simnao(resultado.get("LLM_RISCO_CHURN")),
        "ORGÃO": "",
        "JUSTIFICATIVA": resultado.get("JUSTIFICATIVA_LLM_RISCO_CHURN", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__risco_churn.csv"))


def exp_orgao(resultado, id):
    df = pd.DataFrame([{
        "RESPOSTA": _simnao(resultado.get("LLM_ACIONAR_ORGAOS_SUPERIORES")),
        "ORGÃO": resultado.get("LLM_ORGAO_SUPERIOR", ""),
        "JUSTIFICATIVA": resultado.get("JUSTIFICATIVA_LLM_ACIONAR_ORGAOS_SUPERIORES", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__acionar_orgaos_superiores.csv"))


def exp_encerramento(resultado, id):
    df = pd.DataFrame([{
        "RESPOSTA": _simnao(resultado.get("LLM_ENCERRAMENTO_INATIVIDADE")),
        "ORGÃO": "",
        "JUSTIFICATIVA": resultado.get("JUSTIFICATIVA_LLM_ENCERRAMENTO_INATIVIDADE", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__encerramento_inatividade.csv"))


def exp_tabulacao(resultado, id):
    df = pd.DataFrame([{
        "TABULACAO": resultado.get("LLM_TABULACAO", ""),
        "JUSTIFICATIVA": resultado.get("JUSTIFICATIVA_LLM_TABULACAO", ""),
        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__tabulacao.csv"))


def exp_sentimento(resultado, id):
    df = pd.DataFrame([{
        "HOUVE_IRRITACAO": _simnao(resultado.get("LLM_HOUVE_IRRITACAO")),
        "JUSTIFICATIVA_IRRITACAO": resultado.get("JUSTIFICATIVA_LLM_HOUVE_IRRITACAO", ""),

        "HOUVE_FRUSTRACAO": _simnao(resultado.get("LLM_HOUVE_FRUSTRACAO")),
        "JUSTIFICATIVA_FRUSTRACAO": resultado.get("JUSTIFICATIVA_LLM_HOUVE_FRUSTRACAO", ""),

        "HOUVE_NEUTRALIDADE": _simnao(resultado.get("LLM_HOUVE_NEUTRALIDADE")),
        "JUSTIFICATIVA_NEUTRALIDADE": resultado.get("JUSTIFICATIVA_LLM_HOUVE_NEUTRALIDADE", ""),

        "HOUVE_PREOCUPACAO": _simnao(resultado.get("LLM_HOUVE_PREOCUPACAO")),
        "JUSTIFICATIVA_PREOCUPACAO": resultado.get("JUSTIFICATIVA_LLM_HOUVE_PREOCUPACAO", ""),

        "HOUVE_SATISFACAO": _simnao(resultado.get("LLM_HOUVE_SATISFACAO")),
        "JUSTIFICATIVA_SATISFACAO": resultado.get("JUSTIFICATIVA_LLM_HOUVE_SATISFACAO", ""),

        "ID": id
    }])

    _append_csv(df, _p("atendimento_llm__sentimento.csv"))


# =========================================================
# FUNCAO CENTRAL
# =========================================================
def exportar_todos(
    resultado_dict: dict,
    id_infografico: str,
    df_transcricao=None,
    df_cabecalho=None
):
    print("\n==============================")
    print("EXPORTANDO CSVs")
    print("==============================")

    print("CHAVES RECEBIDAS:", resultado_dict.keys())

    exp_resumo(resultado_dict, id_infografico)
    exp_nps(resultado_dict, id_infografico)
    exp_ouvidoria(resultado_dict, id_infografico)
    exp_acao_judicial(resultado_dict, id_infografico)
    exp_churn(resultado_dict, id_infografico)
    exp_orgao(resultado_dict, id_infografico)
    exp_encerramento(resultado_dict, id_infografico)
    exp_tabulacao(resultado_dict, id_infografico)
    exp_sentimento(resultado_dict, id_infografico)

    print("==============================\n")

