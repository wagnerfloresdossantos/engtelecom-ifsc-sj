from __future__ import annotations

import argparse
import inspect
import json
import os
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv

from carregador import RAIZ_PROTOTIPO, ler_json


def validar_resultado(
    resultado: dict[str, Any],
    cenario: dict[str, Any],
) -> None:
    """Confere se a conversa corresponde ao cenário selecionado."""
    if resultado["scenario_id"] != cenario["scenario_id"]:
        raise ValueError(
            "O resultado e o cenário possuem identificadores diferentes."
        )

    if resultado["scenario_version"] != cenario["version"]:
        raise ValueError(
            "O resultado e o cenário possuem versões diferentes."
        )

    turnos = resultado["turns"]
    esperados = cenario["turns"]

    if not esperados:
        raise ValueError("O cenário não contém turnos.")

    ids_esperados = [
        turno["turn_id"] for turno in esperados
    ]
    ids_observados = [
        turno["turn_id"] for turno in turnos
    ]

    if (
        len(set(ids_esperados)) != len(ids_esperados)
        or ids_observados != ids_esperados
    ):
        raise ValueError(
            "Os turnos estão ausentes, duplicados ou fora da ordem esperada."
        )

    for observado, esperado in zip(turnos, esperados):
        if observado["user_message"] != esperado["user_message"]:
            raise ValueError(
                f"Mensagem diferente no turno {esperado['turn_id']}."
            )

        resposta = observado["assistant_response"]

        if not isinstance(resposta, str) or not resposta.strip():
            raise ValueError(
                f"Resposta vazia no turno {esperado['turn_id']}."
            )


def criar_caso_conversacional(
    resultado: dict[str, Any],
    cenario: dict[str, Any],
):
    from deepeval.test_case import ConversationalTestCase, Turn

    # O avaliador recebe a conversa apresentada ao usuário.
    # As chamadas internas à triagem não são respostas do chatbot.
    turnos = []

    for turno in resultado["turns"]:
        turnos.append(
            Turn(
                role="user",
                content=turno["user_message"],
            )
        )
        turnos.append(
            Turn(
                role="assistant",
                content=turno["assistant_response"],
            )
        )

    return ConversationalTestCase(
        name=(
            f"{resultado['scenario_id']}-"
            f"{resultado['architecture']}-"
            f"{resultado.get('execution_id', 'sem-id')}"
        ),
        scenario=cenario["description"],

        # Documenta o desfecho esperado no caso de teste.
        # Isso não garante que todas as métricas utilizem este campo.
        expected_outcome="; ".join(
            cenario["task_completion"]["criteria"]
        ),
        chatbot_role=(
            "Atendente textual de um provedor de Internet fictício, "
            "responsável por primeiro atendimento, comercial, ouvidoria "
            "e suporte técnico. Deve preservar o contexto e indicar "
            "atendimento humano quando necessário, sem afirmar que "
            "executou operações em sistemas externos."
        ),
        turns=turnos,
    )


def criar_metricas(modelo: str, limiar: float):
    from deepeval.metrics import (
        ConversationCompletenessMetric,
        KnowledgeRetentionMetric,
        TurnRelevancyMetric,
    )

    classes = (
        TurnRelevancyMetric,
        KnowledgeRetentionMetric,
        ConversationCompletenessMetric,
    )

    metricas = []

    for classe in classes:
        parametros = {
            "threshold": limiar,
            "model": modelo,
            "include_reason": True,
            "strict_mode": False,
        }

        # Algumas versões ou métricas possuem parâmetros diferentes.
        # Acrescenta somente as opções disponíveis no construtor.
        assinatura = inspect.signature(classe)

        if "async_mode" in assinatura.parameters:
            parametros["async_mode"] = False

        # Nas versões com modos de avaliação, fixa LLM-as-a-judge.
        if "eval_mode" in assinatura.parameters:
            parametros["eval_mode"] = "llm"

        metricas.append(classe(**parametros))

    return metricas


def avaliar_arquivo(
    caminho: Path,
    cenario: dict[str, Any],
    modelo_avaliador: str,
    limiar: float,
) -> dict[str, Any]:
    resultado = json.loads(
        caminho.read_text(encoding="utf-8")
    )

    validar_resultado(resultado, cenario)

    caso = criar_caso_conversacional(resultado, cenario)
    metricas = criar_metricas(modelo_avaliador, limiar)

    resultados_metricas = []

    # Cada métrica pode realizar chamadas próprias ao modelo avaliador.
    # Esse consumo é separado do consumo dos agentes de atendimento.
    for metrica in metricas:
        metrica.measure(caso)

        if metrica.score is None:
            raise RuntimeError(
                f"A métrica {metrica.__class__.__name__} "
                "não produziu uma pontuação."
            )

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
        # Uma conversa pode ser avaliada mais de uma vez.
        # Cada avaliação recebe seu próprio identificador.
        "evaluation_id": uuid4().hex,
        "execution_id": resultado.get("execution_id"),
        "batch_id": resultado.get("batch_id"),
        "scenario_id": resultado["scenario_id"],
        "architecture": resultado["architecture"],
        "mode": resultado["mode"],
        "evaluated_model": resultado["model"],
        "evaluator_model": modelo_avaliador,
        "deepeval_version": version("deepeval"),
        "evaluated_at_utc": (
            datetime.now(timezone.utc).isoformat()
        ),
        "prototype_version": resultado.get("prototype_version"),
        "scenario_version": resultado["scenario_version"],
        "threshold": limiar,
        "threshold_status": "exploratory",
        "all_metrics_passed": all(
            item["passed"] for item in resultados_metricas
        ),
        "metrics": resultados_metricas,

        # Mantém os critérios disponíveis para revisão,
        # sem declarar que foram todos verificados pelas métricas.
        "scenario_completion_criteria": (
            cenario["task_completion"]["criteria"]
        ),
        "scenario_criteria_individually_assessed": False,
        "method_note": (
            "Avaliação conversacional de relevância, retenção e "
            "completude. Passar nas métricas não comprova conformidade "
            "integral com a base de conhecimento ou com todos os "
            "critérios do cenário. Área, ação, destino humano e rota "
            "são verificados pelo script determinístico. Os demais "
            "critérios exigem avaliação específica ou revisão manual."
        ),
    }


def main() -> None:
    load_dotenv(RAIZ_PROTOTIPO / ".env")

    parser = argparse.ArgumentParser(
        description="Executa métricas conversacionais do DeepEval."
    )

    parser.add_argument(
        "resultados",
        nargs="+",
        help="Arquivos JSON de resultado.",
    )
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
        help="Limiar exploratório entre 0 e 1. Padrão: 0.5.",
    )

    args = parser.parse_args()

    if not 0 <= args.threshold <= 1:
        parser.error("--threshold deve estar entre 0 e 1.")

    modelo_avaliador = os.getenv(
        "TCC_DEEPEVAL_MODEL",
        "gpt-4.1-mini",
    ).strip()

    if not modelo_avaliador:
        parser.error("Defina um modelo avaliador válido.")

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

        # Preserva avaliações anteriores da mesma conversa.
        destino = pasta_saida / (
            f"deepeval-{caminho.stem}-"
            f"{avaliacao['evaluation_id']}.json"
        )

        with destino.open("x", encoding="utf-8") as arquivo:
            json.dump(
                avaliacao,
                arquivo,
                ensure_ascii=False,
                indent=2,
            )

        estado = (
            "ATINGIU OS LIMIARES"
            if avaliacao["all_metrics_passed"]
            else "NÃO ATINGIU TODOS OS LIMIARES"
        )

        print(f"{estado}: {caminho.name}")

        for metrica in avaliacao["metrics"]:
            print(
                f"  {metrica['metric']}: {metrica['score']}"
            )

        print(f"Avaliação salva em: {destino}")


if __name__ == "__main__":
    main()