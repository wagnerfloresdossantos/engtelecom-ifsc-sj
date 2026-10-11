from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


# Localiza a pasta prototipos a partir deste arquivo:
# prototipos/src/carregador.py
RAIZ_PROTOTIPO = Path(__file__).resolve().parents[1]


def ler_texto(caminho_relativo: str) -> str:
    """Lê um arquivo de texto a partir da raiz do protótipo."""
    caminho = RAIZ_PROTOTIPO / caminho_relativo

    return caminho.read_text(encoding="utf-8")


def ler_json(caminho_relativo: str) -> dict[str, Any]:
    """Lê um cenário ou outro documento JSON."""
    caminho = RAIZ_PROTOTIPO / caminho_relativo

    with caminho.open(encoding="utf-8") as arquivo:
        conteudo = json.load(arquivo)

    # Os documentos utilizados aqui devem possuir um objeto
    # na raiz, e não uma lista ou um valor isolado.
    if not isinstance(conteudo, dict):
        raise ValueError(
            f"O arquivo {caminho_relativo} deve conter um objeto JSON."
        )

    return conteudo


def renderizar_prompt(
    nome_arquivo: str,
    base_conhecimento: str,
    historico: list[dict[str, str]],
    mensagem_usuario: str,
    solicitacao_reencaminhamento: dict[str, Any] | None = None,
) -> str:
    """
    Preenche os marcadores do template de prompt.

    Apenas prepara o texto. Não classifica mensagens,
    não escolhe agentes e não realiza chamadas ao modelo.
    """
    template = ler_texto(f"prompts/{nome_arquivo}")

    substituicoes = {
        # A base já chega reunida pelo executor conforme a arquitetura.
        "{{base_conhecimento}}": base_conhecimento,

        # Mantido por compatibilidade com templates anteriores.
        "{{base_comum}}": base_conhecimento,

        # Serializa o histórico e os fatos como texto JSON.
        "{{historico}}": json.dumps(
            historico,
            ensure_ascii=False,
            indent=2,
        ),

        "{{mensagem_usuario}}": mensagem_usuario,

        # None é convertido para null no texto JSON.
        "{{solicitacao_reencaminhamento}}": json.dumps(
            solicitacao_reencaminhamento,
            ensure_ascii=False,
            indent=2,
        ),
    }

    # Reconhece somente os marcadores conhecidos.
    padrao = re.compile(
        "|".join(
            re.escape(marcador)
            for marcador in substituicoes
        )
    )

    # A função de substituição insere cada valor literalmente.
    # O conteúdo inserido não passa por novas substituições.
    return padrao.sub(
        lambda correspondencia: substituicoes[
            correspondencia.group(0)
        ],
        template,
    )