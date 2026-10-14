from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from agente_unico import ArquiteturaAgenteUnico
from carregador import RAIZ_PROTOTIPO, ler_json, ler_texto
from cliente_llm import criar_cliente
from modelos import MedicaoChamada
from multiagente import ArquiteturaMultiagente


# Identificam a nova versão em preparação.
# Não indicam que o experimento definitivo já foi validado.
VERSAO_PROTOTIPO = "0.3.1"
VERSAO_PROMPTS = "0.3.5"
VERSAO_BASES = "0.3.3"

# Ordem fixa para reunir as bases na arquitetura de agente único.
AREAS = (
    "first_contact",
    "commercial",
    "ombudsman",
    "support",
)


def serializar_chamada(chamada: MedicaoChamada) -> dict:
    """Converte o registro de uma chamada para armazenamento em JSON."""
    return {
        "agent": chamada.agente,
        "latency_ms": round(chamada.latencia_ms, 3),
        "input_tokens": chamada.input_tokens,
        "output_tokens": chamada.output_tokens,
        "total_tokens": chamada.total_tokens,
        "output": chamada.saida.model_dump(),
    }


def carregar_bases() -> dict[str, str]:
    """Carrega os documentos utilizados pelas duas arquiteturas."""
    return {
        "common": ler_texto(
            "base-conhecimento/base-comum.md"
        ),
        "triage": ler_texto(
            "base-conhecimento/base-triagem.md"
        ),
        "first_contact": ler_texto(
            "base-conhecimento/base-primeiro-atendimento.md"
        ),
        "commercial": ler_texto(
            "base-conhecimento/base-comercial.md"
        ),
        "ombudsman": ler_texto(
            "base-conhecimento/base-ouvidoria.md"
        ),
        "support": ler_texto(
            "base-conhecimento/base-suporte.md"
        ),
    }


def executar(
    arquitetura_nome: str,
    modo: str,
    cenario: dict,
    bases: dict[str, str],
    lote_id: str,
) -> dict:
    # Cada execução recebe um cliente e um estado novos.
    # Não há compartilhamento de histórico entre arquiteturas.
    cliente = criar_cliente(modo)

    # Identificador exclusivo desta conversa.
    execucao_id = uuid4().hex

    # Data de início registrada em UTC.
    inicio = datetime.now(timezone.utc)

    if arquitetura_nome == "single":
        # O agente único recebe a parte comum e as quatro áreas.
        base_unica = "\n\n".join(
            [bases["common"]]
            + [bases[area] for area in AREAS]
        )

        arquitetura = ArquiteturaAgenteUnico(
            cliente,
            base_unica,
        )

    elif arquitetura_nome == "multi":
        # A triagem recebe as regras comuns e de classificação.
        bases_multi = {
            "triage": "\n\n".join(
                [bases["common"], bases["triage"]]
            )
        }

        # Cada especialista recebe a parte comum e sua área.
        bases_multi.update(
            {
                area: "\n\n".join(
                    [bases["common"], bases[area]]
                )
                for area in AREAS
            }
        )

        arquitetura = ArquiteturaMultiagente(
            cliente,
            bases_multi,
        )

    else:
        raise ValueError(
            f"Arquitetura desconhecida: {arquitetura_nome}."
        )

    turnos_executados = []

    # Executa as mensagens na ordem definida no cenário.
    # Os critérios esperados não são enviados aos agentes.
    for turno in cenario["turns"]:
        resposta, chamadas = arquitetura.processar(
            turno["user_message"]
        )

        turnos_executados.append(
            {
                "turn_id": turno["turn_id"],
                "user_message": turno["user_message"],
                "assistant_response": resposta,
                "expected_intent": turno.get("expected_intent"),
                "calls": [
                    serializar_chamada(chamada)
                    for chamada in chamadas
                ],
            }
        )

    return {
        # O lote relaciona as execuções iniciadas pelo mesmo comando.
        "batch_id": lote_id,
        "execution_id": execucao_id,
        "scenario_id": cenario["scenario_id"],
        "architecture": arquitetura_nome,
        "mode": modo,
        "model": (
            cliente.modelo
            if modo == "openai"
            else "mock"
        ),
        "prototype_version": VERSAO_PROTOTIPO,
        "prompt_version": VERSAO_PROMPTS,
        "knowledge_base_version": VERSAO_BASES,
        "scenario_version": cenario["version"],
        "executed_at_utc": inicio.isoformat(),
        "completed_at_utc": (
            datetime.now(timezone.utc).isoformat()
        ),
        "turns": turnos_executados,
    }


def main() -> None:
    # Carrega as configurações locais antes de criar o cliente.
    load_dotenv(RAIZ_PROTOTIPO / ".env")

    parser = argparse.ArgumentParser(
        description="Executa um cenário conversacional do TCC."
    )

    parser.add_argument(
        "--mode",
        choices=["mock", "openai"],
        default=os.getenv("TCC_LLM_MODE", "mock"),
        help="Cliente simulado ou chamadas reais à OpenAI.",
    )

    parser.add_argument(
        "--architecture",
        choices=["single", "multi", "both"],
        default="both",
        help="Arquitetura que será executada.",
    )

    parser.add_argument(
        "--scenario",
        default="cenarios/cenario-piloto-001.json",
        help="Caminho do cenário em relação à raiz do protótipo.",
    )

    args = parser.parse_args()

    cenario = ler_json(args.scenario)

    if not cenario.get("turns"):
        raise ValueError(
            "O cenário deve conter pelo menos um turno."
        )

    bases = carregar_bases()

    nomes = (
        ["single", "multi"]
        if args.architecture == "both"
        else [args.architecture]
    )

    # Identifica este lote de execução.
    lote_id = uuid4().hex

    pasta_resultados = RAIZ_PROTOTIPO / "resultados"
    pasta_resultados.mkdir(parents=True, exist_ok=True)

    # Cada cenário é executado uma vez por arquitetura selecionada.
    for nome in nomes:
        resultado = executar(
            nome,
            args.mode,
            cenario,
            bases,
            lote_id,
        )

        # O UUID evita substituir os resultados de execuções anteriores.
        # O nome não depende do identificador informado no cenário.
        destino: Path = pasta_resultados / (
            f"execucao-v{VERSAO_PROTOTIPO}-"
            f"{nome}-{args.mode}-"
            f"{resultado['execution_id']}.json"
        )

        # O modo "x" também impede sobrescrita caso o arquivo já exista.
        with destino.open("x", encoding="utf-8") as arquivo:
            json.dump(
                resultado,
                arquivo,
                ensure_ascii=False,
                indent=2,
            )

        print(f"Resultado salvo em: {destino}")


if __name__ == "__main__":
    main()