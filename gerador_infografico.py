import os
import pandas as pd
import re
import unicodedata
import warnings
from html import escape as hescape
from datetime import datetime



# =========================================================
# NORMALIZA CHAVES
# =========================================================
warnings.simplefilter(action="ignore", category=FutureWarning)
def _normalizar_chave(s: str) -> str:
    if not s:
        return ""
    s = s.replace("\u00A0", "")
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ASCII", "ignore").decode("ASCII")
    return s.upper()


# =========================================================
# TRANSCRIÇÃO
# =========================================================
def _gerar_html_transcricao(df_transcricao: pd.DataFrame) -> str:
    if df_transcricao is None or df_transcricao.empty:
        return "<p>Sem mensagens na transcrição.</p>"

    linhas = []
    for _, r in df_transcricao.fillna("").iterrows():
        linhas.append(
            f"""
            <div style="margin-bottom:8px;">
                <b>{hescape(str(r.get("DATAHORA","")))}</b> |
                <b>{hescape(str(r.get("ATOR","")))}</b><br/>
                {hescape(str(r.get("TEXTO","")))}
            </div>
            """
        )

    return "\n".join(linhas)


# =========================================================
# GERADOR PRINCIPAL
# =========================================================
def gerar_infografico(template_path, df_transcricao, df_llm, output_path):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Remove NBSP
    html = html.replace("\u00A0", " ")

    # Transcrição
    html = html.replace(
        "[TRANSCRICAO_ATENDIMENTO]",
        _gerar_html_transcricao(df_transcricao)
    )

    # Monta substituições
    subs = {}

    if df_llm is not None and not df_llm.empty:
        row = df_llm.astype(str).fillna("").iloc[0].to_dict()

        for k, v in row.items():
            kn = _normalizar_chave(k)
            subs[kn] = str(v)

            if kn.startswith("LLM_"):
                subs[kn.replace("LLM_", "")] = str(v)

    subs["DATA_GERACAO"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # ✅ SUBSTITUIÇÃO SEGURA (NUNCA APAGA HTML)
    def substituir(match):
        bruto = match.group(1)
        chave = _normalizar_chave(bruto)

        if chave in subs and subs[chave] != "":
            return subs[chave]

        # 🔒 Se não houver valor, mantém o placeholder
        return match.group(0)

    html = re.sub(r"\[\s*([^\]]+)\s*\]", substituir, html)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Infográfico gerado: {output_path}")
