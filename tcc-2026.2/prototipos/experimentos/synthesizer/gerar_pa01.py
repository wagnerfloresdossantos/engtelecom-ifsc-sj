import json
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import (
    ConversationalStylingConfig,
    EvolutionConfig,
)


PASTA = Path(__file__).resolve().parent
RAIZ_PROTOTIPOS = PASTA.parent.parent

load_dotenv(RAIZ_PROTOTIPOS / ".env")

MODELO = "gpt-4.1-mini"
ARQUIVO_CONTEXTO = PASTA / "contextos" / "pa-01-informacoes-gerais.md"

contexto = ARQUIVO_CONTEXTO.read_text(encoding="utf-8")

configuracao_estilo = {
    "scenario_context": (
        "Atendimento textual do Provedor Alfa, organização fictícia "
        "que oferece Internet por fibra óptica. "
        "Utilizar somente as informações do contexto fornecido."
    ),
    "conversational_task": (
        "Propor um cenário PA-01 com dois turnos do usuário: "
        "primeiro um pedido genérico de ajuda; depois uma pergunta "
        "sobre o tipo de serviço oferecido pelo provedor."
    ),
    "participant_roles": (
        "Usuário fictício e assistente de primeiro atendimento. "
        "Utilizar português brasileiro cotidiano."
    ),
    "scenario_format": (
        "Descrever a situação inicial e a informação revelada "
        "em cada um dos dois turnos. Não escrever respostas "
        "do assistente nem diálogo completo. Não antecipar "
        "a pergunta sobre serviços no primeiro turno."
    ),
    "expected_outcome_format": (
        "Descrever em português brasileiro um desfecho verificável: "
        "o usuário recebe informação sobre Internet por fibra óptica, "
        "sem coleta de dados cadastrais ou encaminhamento desnecessário. "
        "Não copiar estas instruções como introdução do desfecho."
    ),
}

synthesizer = Synthesizer(
    model=MODELO,
    async_mode=False,
    max_concurrent=1,
    evolution_config=EvolutionConfig(
        num_evolutions=0,
    ),
    conversational_styling_config=ConversationalStylingConfig(
        **configuracao_estilo
    ),
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
    "experiment_id": "geracao-exploratoria-pa01-001",
    "situation_id": "PA-01",
    "script_version": "0.1.1",
    "deepeval_version": version("deepeval"),
    "generator_model": MODELO,
    "started_at_utc": inicio.isoformat(),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "source_file": str(
        ARQUIVO_CONTEXTO.relative_to(RAIZ_PROTOTIPOS)
    ),
    "source_context": contexto,
    "styling": configuracao_estilo,
    "generation_settings": {
        "async_mode": False,
        "max_concurrent": 1,
        "num_evolutions": 0,
        "include_expected_outcome": True,
        "max_goldens_per_context": 1,
    },
    "candidate_count": len(candidatos),
    "review_status": "pending",
    "candidates": [
        candidato.model_dump(mode="json")
        for candidato in candidatos
    ],
}

pasta_saida = PASTA / "gerados"
pasta_saida.mkdir(parents=True, exist_ok=True)

destino = pasta_saida / (
    f"candidato-pa01-{registro['generation_id']}.json"
)

with destino.open("x", encoding="utf-8") as arquivo:
    json.dump(
        registro,
        arquivo,
        ensure_ascii=False,
        indent=2,
    )

print(f"Candidatos gerados: {len(candidatos)}")
print(f"Resultado salvo em: {destino}")