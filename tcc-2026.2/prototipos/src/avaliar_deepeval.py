from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from carregador import RAIZ_PROTOTIPO, ler_json


def criar_caso_conversacional(resultado: dict[str, Any], cenario: dict[str, Any]):
    from deepeval.test_case import ConversationalTestCase, Turn

    turnos: list[Turn] = []
    for turno in resultado["turns"]:
        turnos.append(Turn(role="user", content=turno["user_message"]))
        turnos.append(
            Turn(role="assistant", content=turno["assistant_response"])
        )

    resultado_esperado = "; ".join(
        cenario["task_completion"]["criteria"]
    )
    return ConversationalTestCase(
        name=f"{resultado['scenario_id']}-{resultado['architecture']}",
        scenario=cenario["description"],
        expected_outcome=resultado_esperado,
        chatbot_role=(
            "Atendente textual de um provedor de Internet fictício, responsável "
            "por responder de forma direta, preservar o contexto e encaminhar "
            "corretamente solicitações comerciais e técnicas."
        ),
        turns=turnos,
    )


def criar_metricas(modelo: str, limiar: float):
    from deepeval.metrics import (
        ConversationCompletenessMetric,
        KnowledgeRetentionMetric,
        TurnRelevancyMetric,
    )

    parametros = {
        "threshold": limiar,
        "model": modelo,
        "include_reason": True,
        "async_mode": False,
    }
    return [
        TurnRelevancyMetric(**parametros),
        KnowledgeRetentionMetric(**parametros),
        ConversationCompletenessMetric(**parametros),
    ]


def avaliar_arquivo(
    caminho: Path,
    cenario: dict[str, Any],
    modelo_avaliador: str,
    limiar: float,
) -> dict[str, Any]:
    resultado = json.loads(caminho.read_text(encoding="utf-8"))
    caso = criar_caso_conversacional(resultado, cenario)
    metricas = criar_metricas(modelo_avaliador, limiar)

    resultados_metricas = []
    for metrica in metricas:
        metrica.measure(caso)
        resultados_metricas.append(
            {
                "metric": metrica.__class__.__name__,
                "score": metrica.score,
                "threshold": metrica.threshold,
                "passed": bool(metrica.is_successful()),
                "reason": metrica.reason,
            }
        )

    return {
        "scenario_id": resultado["scenario_id"],
        "architecture": resultado["architecture"],
        "evaluated_model": resultado["model"],
        "evaluator_model": modelo_avaliador,
        "prototype_version": resultado.get("prototype_version"),
        "scenario_version": resultado.get("scenario_version"),
        "threshold": limiar,
        "all_metrics_passed": all(
            metrica["passed"] for metrica in resultados_metricas
        ),
        "metrics": resultados_metricas,
        "method_note": (
            "Avaliação semântica LLM-as-a-judge. Os critérios determinísticos "
            "de intenção, rota e comportamentos proibidos são avaliados em "
            "arquivo separado."
        ),
    }


def main() -> None:
    load_dotenv(RAIZ_PROTOTIPO / ".env")

    parser = argparse.ArgumentParser(
        description="Executa métricas conversacionais do DeepEval."
    )
    parser.add_argument("resultados", nargs="+", help="Arquivos JSON de resultado.")
    parser.add_argument(
        "--scenario",
        default="cenarios/cenario-piloto-001.json",
        help="Caminho do cenário em relação à raiz do protótipo.",
    )
    parser.add_argument(
        "--output-dir",
        default="resultados/avaliacoes-deepeval",
        help="Diretório de saída em relação à raiz do protótipo.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Limiar exploratório aplicado às métricas. Padrão: 0.5.",
    )
    args = parser.parse_args()

    modelo_avaliador = os.getenv("TCC_DEEPEVAL_MODEL", "gpt-4.1-mini")
    cenario = ler_json(args.scenario)
    pasta_saida = RAIZ_PROTOTIPO / args.output_dir
    pasta_saida.mkdir(parents=True, exist_ok=True)

    for nome_resultado in args.resultados:
        caminho = Path(nome_resultado)
        avaliacao = avaliar_arquivo(
            caminho,
            cenario,
            modelo_avaliador,
            args.threshold,
        )
        destino = pasta_saida / f"deepeval-{caminho.stem}.json"
        destino.write_text(
            json.dumps(avaliacao, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        estado = "APROVADO" if avaliacao["all_metrics_passed"] else "REPROVADO"
        print(f"{estado}: {caminho.name}")
        for metrica in avaliacao["metrics"]:
            print(f"  {metrica['metric']}: {metrica['score']}")
        print(f"Avaliação salva em: {destino}")


if __name__ == "__main__":
    main()
