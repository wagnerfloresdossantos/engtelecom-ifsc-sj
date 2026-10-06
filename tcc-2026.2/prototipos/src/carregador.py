from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RAIZ_PROTOTIPO = Path(__file__).resolve().parents[1]


def ler_texto(caminho_relativo: str) -> str:
    caminho = RAIZ_PROTOTIPO / caminho_relativo
    return caminho.read_text(encoding="utf-8")


def ler_json(caminho_relativo: str) -> dict[str, Any]:
    caminho = RAIZ_PROTOTIPO / caminho_relativo
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def renderizar_prompt(
    nome_arquivo: str,
    base_conhecimento: str,
    historico: list[dict[str, str]],
    mensagem_usuario: str,
    solicitacao_reencaminhamento: dict[str, Any] | None = None,
) -> str:
    prompt = ler_texto(f"prompts/{nome_arquivo}")
    substituicoes = {
        "{{base_conhecimento}}": base_conhecimento,
        "{{base_comum}}": base_conhecimento,
        "{{historico}}": json.dumps(historico, ensure_ascii=False, indent=2),
        "{{mensagem_usuario}}": mensagem_usuario,
        "{{solicitacao_reencaminhamento}}": json.dumps(
            solicitacao_reencaminhamento, ensure_ascii=False, indent=2
        ),
    }
    for marcador, valor in substituicoes.items():
        prompt = prompt.replace(marcador, valor)
    return prompt
