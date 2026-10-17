from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from uuid import uuid4
import json

from dotenv import load_dotenv
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ConversationalStylingConfig


PASTA_EXPERIMENTO = Path(__file__).resolve().parent
RAIZ_PROTOTIPOS = PASTA_EXPERIMENTO.parent.parent

load_dotenv(RAIZ_PROTOTIPOS / ".env")

MODELO = "gpt-4.1-mini"

caminho_contexto = (
    PASTA_EXPERIMENTO
    / "contextos"
    / "suporte-sem-conexao.md"
)

contexto = caminho_contexto.read_text(encoding="utf-8")

estilo = ConversationalStylingConfig(
    scenario_context=(
        "Atendimento textual de suporte de um provedor fictício. "
        "Utilizar somente a situação e as regras do contexto fornecido."
    ),
    conversational_task=(
        "Definir um cenário de avaliação de suporte sem conexão, "
        "com informações apresentadas gradualmente e persistência "
        "da falha após reinicialização relatada pelo usuário."
    ),
    participant_roles=(
        "Usuário fictício, cliente do provedor, e assistente de suporte. "
        "O usuário utiliza português brasileiro cotidiano."
    ),
    scenario_format=(
        "Descrição em português brasileiro contendo situação inicial, "
        "objetivo do usuário e informações a revelar progressivamente. "
        "Não escrever diálogo completo nem respostas do assistente."
    ),
    expected_outcome_format=(
        "Desfecho esperado em português brasileiro, verificável "
        "e compatível com as regras fornecidas. "
        "Não afirmar realização de operações externas."
    ),
)

synthesizer = Synthesizer(
    model=MODELO,
    async_mode=False,
    max_concurrent=1,
    conversational_styling_config=estilo,
)

inicio = datetime.now(timezone.utc)

candidatos = (
    synthesizer.generate_conversational_goldens_from_contexts(
        contexts=[[contexto]],
        include_expected_outcome=True,
        max_goldens_per_context=1,
    )
)

registro = {
    "generation_id": uuid4().hex,
    "experiment_id": "geracao-exploratoria-suporte-001",
    "deepeval_version": version("deepeval"),
    "generator_model": MODELO,
    "started_at_utc": inicio.isoformat(),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "source_file": str(
        caminho_contexto.relative_to(RAIZ_PROTOTIPOS)
    ),
    "source_context": contexto,
    "styling": {
        "scenario_context": estilo.scenario_context,
        "conversational_task": estilo.conversational_task,
        "participant_roles": estilo.participant_roles,
        "scenario_format": estilo.scenario_format,
        "expected_outcome_format": estilo.expected_outcome_format,
    },
    "max_goldens_per_context": 1,
    "candidate_count": len(candidatos),
    "review_status": "pending",
    "candidates": [
        candidato.model_dump(mode="json")
        for candidato in candidatos
    ],
}

pasta_saida = PASTA_EXPERIMENTO / "gerados"
pasta_saida.mkdir(parents=True, exist_ok=True)

destino = pasta_saida / (
    f"candidato-suporte-{registro['generation_id']}.json"
)

with destino.open("x", encoding="utf-8") as arquivo:
    json.dump(
        registro,
        arquivo,
        ensure_ascii=False,
        indent=2,
    )

print(f"\nCandidatos gerados: {len(candidatos)}")
print(f"Resultado salvo em: {destino}")

for numero, candidato in enumerate(registro["candidates"], start=1):
    print(f"\nCandidato {numero}:")
    print(json.dumps(candidato, ensure_ascii=False, indent=2))
    