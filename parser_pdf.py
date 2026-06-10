import pdfplumber
import pandas as pd
import re
from datetime import datetime

def extrair_transcricao_segura(caminho_pdf):
    import pdfplumber
    import pandas as pd
    import re

    linhas = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                linhas.extend(texto.splitlines())

    mensagens = []
    buffer = {}

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            continue

        # ✅ identifica DATA
        if re.search(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", linha):

            if buffer:
                mensagens.append(buffer)

            buffer = {
                "DATAHORA": linha,
                "ATOR": "",
                "TEXTO": ""
            }

        else:
            # ✅ heurística: ator = linha curta sem números longos
            if not buffer.get("ATOR") and len(linha) < 40:
                buffer["ATOR"] = linha

            else:
                buffer["TEXTO"] += " " + linha

    if buffer:
        mensagens.append(buffer)

    df = pd.DataFrame(mensagens)

    print(f"[INFO] Transcricao extraida: {len(df)} mensagens")

    return df

