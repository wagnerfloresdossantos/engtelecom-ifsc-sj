from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from carregador import RAIZ_PROTOTIPO, ler_json


# Identificadores dos especialistas, sem incluir a triagem.
AREAS = {
    "first_contact",
    "commercial",
    "ombudsman",
    "support",
}


# Mantém compatibilidade com nomes de rotas escritos em português.
MAPA_AGENTES = {
    "primeiro_atendimento": "first_contact",
    "comercial": "commercial",
    "ouvidoria": "ombudsman",
    "suporte": "support",
    "agente_unico": "agente_unico",
    "triagem": "triagem",
}


# Verificações parciais de expressões inadequadas.
# Não substituem a avaliação semântica ou a revisão manual.
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
    """Converte a rota textual em uma lista de chamadas."""
    partes = [parte.strip() for parte in rota.split("->")]

    return [
        MAPA_AGENTES.get(parte, parte)
        for parte in partes
    ]


def localizar_expressoes_proibidas(texto: str) -> list[str]:
    """Localiza categorias com expressões suspeitas na resposta."""
    ocorrencias = []

    for categoria, expressoes in EXPRESSOES_PROIBIDAS.items():
        if any(
            re.search(expressao, texto, flags=re.IGNORECASE)
            for expressao in expressoes
        ):
            ocorrencias.append(categoria)

    return ocorrencias


def avaliar_turno(
    turno_resultado: dict[str, Any],
    turno_cenario: dict[str, Any],
    rota_esperada: str,
    arquitetura: str,
) -> dict[str, Any]:
    chamadas = turno_resultado["calls"]

    if not chamadas:
        raise ValueError(
            f"Turno {turno_resultado['turn_id']} sem chamadas registradas."
        )

    # A última chamada deve produzir a resposta final do turno.
    chamada_final = chamadas[-1]
    saida_final = chamada_final["output"]

    # No agente único, a área é declarada na saída estruturada.
    # No multiagente, corresponde ao especialista que respondeu.
    if arquitetura == "single":
        area_observada = saida_final["active_area"]
    else:
        area_observada = chamada_final["agent"]

    area_esperada = turno_cenario["expected_area"]
    intencao_esperada = turno_cenario["expected_intent"]
    acao_esperada = turno_cenario["expected_action"]
    destino_esperado = turno_cenario["expected_handoff_target"]

    intencao_observada = saida_final["intent"]
    acao_observada = saida_final["action"]
    destino_observado = saida_final["handoff_target"]

    rota_observada = [
        chamada["agent"] for chamada in chamadas
    ]
    rota_normalizada = normalizar_rota(rota_esperada)

    resposta = turno_resultado["assistant_response"]
    expressoes = localizar_expressoes_proibidas(resposta)

    # Avalia tanto encaminhamentos necessários quanto indevidos.
    encaminhamento_correto = (
        (acao_observada == "handoff_human")
        == (acao_esperada == "handoff_human")
        and destino_observado == destino_esperado
    )

    # Confere se a resposta salva corresponde à saída final.
    resposta_consistente = (
        isinstance(resposta, str)
        and bool(resposta.strip())
        and resposta == saida_final.get("response")
    )

    return {
        "turn_id": turno_resultado["turn_id"],
        "expected_intent": intencao_esperada,
        "observed_intent": intencao_observada,
        "intent_correct": (
            intencao_observada == intencao_esperada
        ),
        "expected_area": area_esperada,
        "observed_area": area_observada,
        "area_correct": area_observada == area_esperada,
        "expected_action": acao_esperada,
        "observed_action": acao_observada,
        "action_correct": acao_observada == acao_esperada,
        "expected_handoff_target": destino_esperado,
        "observed_handoff_target": destino_observado,
        "human_handoff_correct": encaminhamento_correto,
        "expected_route": rota_normalizada,
        "observed_route": rota_observada,
        "route_correct": rota_observada == rota_normalizada,
        "response_consistent": resposta_consistente,

        # Ausência de correspondência não comprova ausência
        # de todos os comportamentos proibidos.
        "flagged_expression_categories": expressoes,
        "no_flagged_expressions": not expressoes,
    }


def contar_trocas_especialistas(chamadas: list[dict]) -> int:
    """
    Conta mudanças entre especialistas na conversa completa.

    A seleção inicial não é uma troca.
    Chamadas à triagem não são contadas como especialistas.
    """
    especialistas = [
        chamada["agent"]
        for chamada in chamadas
        if chamada["agent"] in AREAS
    ]

    return sum(
        anterior != atual
        for anterior, atual in zip(
            especialistas,
            especialistas[1:],
        )
    )


def avaliar_resultado(
    resultado: dict[str, Any],
    cenario: dict[str, Any],
) -> dict[str, Any]:
    arquitetura = resultado["architecture"]

    if arquitetura not in {"single", "multi"}:
        raise ValueError(
            f"Arquitetura desconhecida: {arquitetura}."
        )

    # Evita avaliar um resultado com o cenário errado.
    if resultado["scenario_id"] != cenario["scenario_id"]:
        raise ValueError(
            "O resultado e o cenário possuem identificadores diferentes."
        )

    if resultado["scenario_version"] != cenario["version"]:
        raise ValueError(
            "O resultado e o cenário possuem versões diferentes."
        )

    turnos_resultado = resultado["turns"]
    turnos_cenario = cenario["turns"]

    # Uma conversa incompleta não deve receber aprovação.
    ids_resultado = [
        turno["turn_id"] for turno in turnos_resultado
    ]
    ids_cenario = [
        turno["turn_id"] for turno in turnos_cenario
    ]

    if (
        not ids_cenario
        or len(set(ids_cenario)) != len(ids_cenario)
        or ids_resultado != ids_cenario
    ):
        raise ValueError(
            "Os turnos estão ausentes, duplicados ou fora da ordem esperada."
        )

    # Confere se as mensagens executadas são as do cenário.
    for observado, esperado in zip(
        turnos_resultado,
        turnos_cenario,
    ):
        if observado["user_message"] != esperado["user_message"]:
            raise ValueError(
                f"Mensagem diferente no turno {esperado['turn_id']}."
            )

    chave_rota = (
        "single_agent"
        if arquitetura == "single"
        else "multiagent"
    )
    rotas_esperadas = cenario["expected_route"][chave_rota]

    if len(rotas_esperadas) != len(turnos_cenario):
        raise ValueError(
            "A quantidade de rotas não corresponde à quantidade de turnos."
        )

    avaliacoes = [
        avaliar_turno(
            observado,
            esperado,
            rota,
            arquitetura,
        )
        for observado, esperado, rota in zip(
            turnos_resultado,
            turnos_cenario,
            rotas_esperadas,
        )
    ]

    chamadas = [
        chamada
        for turno in turnos_resultado
        for chamada in turno["calls"]
    ]

    total_turnos = len(avaliacoes)

    intencoes_corretas = sum(
        item["intent_correct"] for item in avaliacoes
    )
    areas_corretas = sum(
        item["area_correct"] for item in avaliacoes
    )
    acoes_corretas = sum(
        item["action_correct"] for item in avaliacoes
    )
    rotas_corretas = sum(
        item["route_correct"] for item in avaliacoes
    )
    encaminhamentos_corretos = sum(
        item["human_handoff_correct"] for item in avaliacoes
    )

    # Acurácia por área: usa os turnos cuja área esperada
    # corresponde à categoria avaliada.
    por_area = {}

    for area in sorted(AREAS):
        itens = [
            item
            for item in avaliacoes
            if item["expected_area"] == area
        ]
        acertos = sum(item["area_correct"] for item in itens)

        por_area[area] = {
            "turns": len(itens),
            "correct": acertos,
            "accuracy": acertos / len(itens) if itens else None,
        }

    criterios_estruturados = (
        "intent_correct",
        "area_correct",
        "action_correct",
        "human_handoff_correct",
        "route_correct",
        "response_consistent",
    )

    aprovado_estruturado = all(
        all(item[chave] for chave in criterios_estruturados)
        for item in avaliacoes
    )

    sem_expressoes_suspeitas = all(
        item["no_flagged_expressions"]
        for item in avaliacoes
    )

    resumo = {
        "turns": total_turnos,
        "correct_intents": intencoes_corretas,
        "correct_areas": areas_corretas,
        "area_accuracy": areas_corretas / total_turnos,
        "area_accuracy_by_area": por_area,
        "correct_actions": acoes_corretas,
        "correct_routes": rotas_corretas,

        # Inclui acertos de presença e de ausência de encaminhamento.
        "correct_human_handoff_decisions": encaminhamentos_corretos,
        "human_handoff_accuracy": (
            encaminhamentos_corretos / total_turnos
        ),

        # None significa que a medida não se aplica ao agente único.
        "internal_agent_transfers": (
            contar_trocas_especialistas(chamadas)
            if arquitetura == "multi"
            else None
        ),
        "model_calls": len(chamadas),
        "input_tokens": sum(
            chamada["input_tokens"] for chamada in chamadas
        ),
        "output_tokens": sum(
            chamada["output_tokens"] for chamada in chamadas
        ),
        "total_tokens": sum(
            chamada["total_tokens"] for chamada in chamadas
        ),

        # Mantido como registro auxiliar de latência das chamadas.
        "accumulated_latency_ms": round(
            sum(chamada["latency_ms"] for chamada in chamadas),
            3,
        ),
        "no_flagged_expressions": sem_expressoes_suspeitas,
    }

    return {
        "execution_id": resultado.get("execution_id"),
        "batch_id": resultado.get("batch_id"),
        "scenario_id": resultado["scenario_id"],
        "architecture": arquitetura,
        "mode": resultado["mode"],
        "model": resultado["model"],
        "prototype_version": resultado.get("prototype_version"),
        "scenario_version": resultado["scenario_version"],
        "structured_checks_passed": aprovado_estruturado,
        "deterministic_validation_passed": (
            aprovado_estruturado
            and sem_expressoes_suspeitas
        ),
        "task_completion_assessed": False,
        "summary": resumo,
        "turns": avaliacoes,
        "scope_note": (
            "Esta avaliação cobre campos estruturados e buscas parciais "
            "por expressões. Não verifica integralmente required_behavior, "
            "required_context_after_turn, forbidden_behavior ou os critérios "
            "de task_completion. A conclusão da tarefa e a qualidade "
            "semântica exigem avaliação complementar."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Avalia critérios estruturados das conversas do TCC."
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
        default="resultados/avaliacoes",
        help="Diretório de saída em relação à raiz do protótipo.",
    )

    args = parser.parse_args()

    cenario = ler_json(args.scenario)
    pasta_saida = RAIZ_PROTOTIPO / args.output_dir
    pasta_saida.mkdir(parents=True, exist_ok=True)

    for nome_resultado in args.resultados:
        caminho = Path(nome_resultado)

        resultado = json.loads(
            caminho.read_text(encoding="utf-8")
        )
        avaliacao = avaliar_resultado(resultado, cenario)

        destino = pasta_saida / f"avaliacao-{caminho.stem}.json"

        destino.write_text(
            json.dumps(
                avaliacao,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        estado = (
            "PASSOU NAS VERIFICAÇÕES DETERMINÍSTICAS"
            if avaliacao["deterministic_validation_passed"]
            else "FALHOU NAS VERIFICAÇÕES DETERMINÍSTICAS"
        )

        print(f"{estado}: {caminho.name}")
        print(
            "A conclusão da tarefa ainda exige avaliação complementar."
        )
        print(f"Avaliação salva em: {destino}")


if __name__ == "__main__":
    main()