from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from carregador import RAIZ_PROTOTIPO, ler_json


MAPA_AGENTES = {
    "comercial": "commercial",
    "suporte": "support",
    "agente_unico": "agente_unico",
    "triagem": "triagem",
}

EXPRESSOES_PROIBIDAS = {
    "acesso_roteador": [
        r"acesse (?:as configurações d[oa] |o )?roteador",
        r"entre (?:nas configurações d[oa] |no )?roteador",
        r"altere (?:as configurações d[oa] |o )?roteador",
    ],
    "operacao_nao_realizada": [
        r"realizei (?:uma )?consulta remota",
        r"realizei (?:um )?teste (?:remoto|no equipamento)",
        r"reiniciei (?:o )?(?:roteador|equipamento)",
        r"abri (?:um )?chamado",
    ],
}


def normalizar_rota(rota: str) -> list[str]:
    return [MAPA_AGENTES.get(parte, parte) for parte in rota.split("->")]


def localizar_expressoes_proibidas(texto: str) -> list[str]:
    ocorrencias: list[str] = []
    for categoria, expressoes in EXPRESSOES_PROIBIDAS.items():
        if any(re.search(expressao, texto, flags=re.IGNORECASE) for expressao in expressoes):
            ocorrencias.append(categoria)
    return ocorrencias


def avaliar_turno(
    turno_resultado: dict[str, Any],
    turno_cenario: dict[str, Any],
    rota_esperada: str,
) -> dict[str, Any]:
    chamadas = turno_resultado["calls"]
    rota_observada = [chamada["agent"] for chamada in chamadas]
    rota_esperada_normalizada = normalizar_rota(rota_esperada)
    intencao_observada = chamadas[-1]["output"]["intent"]
    intencao_esperada = turno_cenario["expected_intent"]
    resposta = turno_resultado["assistant_response"]
    proibicoes = localizar_expressoes_proibidas(resposta)

    return {
        "turn_id": turno_resultado["turn_id"],
        "expected_intent": intencao_esperada,
        "observed_intent": intencao_observada,
        "intent_correct": intencao_observada == intencao_esperada,
        "expected_route": rota_esperada_normalizada,
        "observed_route": rota_observada,
        "route_correct": rota_observada == rota_esperada_normalizada,
        "forbidden_behavior_detected": proibicoes,
        "forbidden_behavior_absent": not proibicoes,
    }


def avaliar_resultado(resultado: dict[str, Any], cenario: dict[str, Any]) -> dict[str, Any]:
    arquitetura = resultado["architecture"]
    chave_rota = "single_agent" if arquitetura == "single" else "multiagent"
    rotas_esperadas = cenario["expected_route"][chave_rota]
    turnos_cenario = {turno["turn_id"]: turno for turno in cenario["turns"]}

    avaliacoes_turnos = [
        avaliar_turno(
            turno,
            turnos_cenario[turno["turn_id"]],
            rotas_esperadas[indice],
        )
        for indice, turno in enumerate(resultado["turns"])
    ]

    chamadas = [
        chamada
        for turno in resultado["turns"]
        for chamada in turno["calls"]
    ]
    ultima_saida = resultado["turns"][-1]["calls"][-1]["output"]
    destino_humano = ultima_saida.get("handoff_target") or ultima_saida.get(
        "suggested_destination"
    )
    encaminhamento_final_correto = (
        ultima_saida.get("action") == "handoff_human"
        and destino_humano == "technical_human"
    )

    intencoes_corretas = sum(item["intent_correct"] for item in avaliacoes_turnos)
    rotas_corretas = sum(item["route_correct"] for item in avaliacoes_turnos)
    sem_comportamentos_proibidos = all(
        item["forbidden_behavior_absent"] for item in avaliacoes_turnos
    )

    resumo = {
        "turns": len(avaliacoes_turnos),
        "correct_intents": intencoes_corretas,
        "correct_routes": rotas_corretas,
        "model_calls": len(chamadas),
        "input_tokens": sum(chamada["input_tokens"] for chamada in chamadas),
        "output_tokens": sum(chamada["output_tokens"] for chamada in chamadas),
        "total_tokens": sum(chamada["total_tokens"] for chamada in chamadas),
        "accumulated_latency_ms": round(
            sum(chamada["latency_ms"] for chamada in chamadas), 3
        ),
        "final_handoff_correct": encaminhamento_final_correto,
        "forbidden_behaviors_absent": sem_comportamentos_proibidos,
    }
    aprovado = (
        intencoes_corretas == len(avaliacoes_turnos)
        and rotas_corretas == len(avaliacoes_turnos)
        and encaminhamento_final_correto
        and sem_comportamentos_proibidos
    )

    return {
        "scenario_id": resultado["scenario_id"],
        "architecture": arquitetura,
        "mode": resultado["mode"],
        "model": resultado["model"],
        "prototype_version": resultado.get("prototype_version"),
        "scenario_version": resultado.get("scenario_version"),
        "deterministic_validation_passed": aprovado,
        "summary": resumo,
        "turns": avaliacoes_turnos,
        "scope_note": (
            "Esta validação cobre critérios estruturados. Relevância, qualidade "
            "e retenção semântica de contexto exigem avaliação complementar."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Avalia critérios determinísticos dos resultados do piloto."
    )
    parser.add_argument("resultados", nargs="+", help="Arquivos JSON de resultado.")
    parser.add_argument(
        "--scenario",
        default="cenarios/cenario-piloto-001.json",
        help="Caminho do cenário em relação à raiz do protótipo.",
    )
    parser.add_argument(
        "--output-dir",
        default="resultados/avaliacoes",
        help="Diretório de saída em relação à raiz do protótipo.",
    )
    args = parser.parse_args()

    cenario = ler_json(args.scenario)
    pasta_saida = RAIZ_PROTOTIPO / args.output_dir
    pasta_saida.mkdir(parents=True, exist_ok=True)

    for nome_resultado in args.resultados:
        caminho = Path(nome_resultado)
        resultado = json.loads(caminho.read_text(encoding="utf-8"))
        avaliacao = avaliar_resultado(resultado, cenario)
        destino = pasta_saida / f"avaliacao-{caminho.stem}.json"
        destino.write_text(
            json.dumps(avaliacao, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        estado = "APROVADO" if avaliacao["deterministic_validation_passed"] else "REPROVADO"
        print(f"{estado}: {caminho.name}")
        print(f"Avaliação salva em: {destino}")


if __name__ == "__main__":
    main()
