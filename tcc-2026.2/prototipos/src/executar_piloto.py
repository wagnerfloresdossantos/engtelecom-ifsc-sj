from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs) -> bool:
        return False

from agente_unico import ArquiteturaAgenteUnico
from carregador import RAIZ_PROTOTIPO, ler_json, ler_texto
from cliente_llm import criar_cliente
from multiagente import ArquiteturaMultiagente


def serializar_chamada(chamada) -> dict:
    return {
        "agent": chamada.agente,
        "latency_ms": round(chamada.latencia_ms, 3),
        "input_tokens": chamada.input_tokens,
        "output_tokens": chamada.output_tokens,
        "total_tokens": chamada.total_tokens,
        "output": chamada.saida.model_dump(),
    }


VERSAO_PROTOTIPO = "0.2.0"
VERSAO_PROMPTS = "0.2.0"
VERSAO_BASES = "0.2.0"


def executar(arquitetura_nome: str, modo: str, cenario: dict, bases: dict[str, str]) -> dict:
    cliente = criar_cliente(modo)
    if arquitetura_nome == "single":
        base_unica = "\n\n".join(
            [bases["common"], bases["commercial"], bases["support"]]
        )
        arquitetura = ArquiteturaAgenteUnico(cliente, base_unica)
    else:
        bases_multi = {
            "triage": "\n\n".join([bases["common"], bases["triage"]]),
            "commercial": "\n\n".join([bases["common"], bases["commercial"]]),
            "support": "\n\n".join([bases["common"], bases["support"]]),
        }
        arquitetura = ArquiteturaMultiagente(cliente, bases_multi)

    turnos_executados = []
    for turno in cenario["turns"]:
        resposta, chamadas = arquitetura.processar(turno["user_message"])
        turnos_executados.append(
            {
                "turn_id": turno["turn_id"],
                "user_message": turno["user_message"],
                "assistant_response": resposta,
                "expected_intent": turno["expected_intent"],
                "calls": [serializar_chamada(chamada) for chamada in chamadas],
            }
        )

    return {
        "scenario_id": cenario["scenario_id"],
        "architecture": arquitetura_nome,
        "mode": modo,
        "model": os.getenv("TCC_OPENAI_MODEL") if modo == "openai" else "mock",
        "prototype_version": VERSAO_PROTOTIPO,
        "prompt_version": VERSAO_PROMPTS,
        "knowledge_base_version": VERSAO_BASES,
        "scenario_version": cenario["version"],
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "turns": turnos_executados,
    }


def main() -> None:
    load_dotenv(RAIZ_PROTOTIPO / ".env")
    parser = argparse.ArgumentParser(description="Executa o cenário piloto do TCC.")
    parser.add_argument("--mode", choices=["mock", "openai"], default=os.getenv("TCC_LLM_MODE", "mock"))
    parser.add_argument("--architecture", choices=["single", "multi", "both"], default="both")
    args = parser.parse_args()

    cenario = ler_json("cenarios/cenario-piloto-001.json")
    bases = {
        "common": ler_texto("base-conhecimento/base-comum.md"),
        "triage": ler_texto("base-conhecimento/base-triagem.md"),
        "commercial": ler_texto("base-conhecimento/base-comercial.md"),
        "support": ler_texto("base-conhecimento/base-suporte.md"),
    }
    nomes = ["single", "multi"] if args.architecture == "both" else [args.architecture]

    pasta_resultados = RAIZ_PROTOTIPO / "resultados"
    pasta_resultados.mkdir(parents=True, exist_ok=True)

    for nome in nomes:
        resultado = executar(nome, args.mode, cenario, bases)
        destino: Path = pasta_resultados / f"piloto-001-v0.2-{nome}-{args.mode}.json"
        destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Resultado salvo em: {destino}")


if __name__ == "__main__":
    main()
