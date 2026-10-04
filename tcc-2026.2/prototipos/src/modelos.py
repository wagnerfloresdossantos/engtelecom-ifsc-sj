from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel


Intent = Literal[
    "comercial_planos",
    "comercial_consulta_cobertura",
    "suporte_sem_conexao",
    "suporte_falha_optica",
]


class SaidaAgenteUnico(BaseModel):
    response: str
    intent: Intent
    active_area: Literal["commercial", "support"]
    action: Literal["respond", "handoff_human"]
    handoff_target: Literal["technical_human"] | None
    context_facts: list[str]


class SaidaTriagem(BaseModel):
    destination: Literal["commercial", "support"]
    intent: Intent
    reason: str
    context_to_forward: list[str]


class SaidaComercial(BaseModel):
    response: str | None
    intent: Intent
    action: Literal["respond", "request_reroute"]
    suggested_destination: Literal["support"] | None
    context_facts: list[str]


class SaidaSuporte(BaseModel):
    response: str | None
    intent: Intent
    action: Literal["respond", "handoff_human", "request_reroute"]
    suggested_destination: Literal["commercial", "technical_human"] | None
    context_facts: list[str]


@dataclass
class MedicaoChamada:
    agente: str
    latencia_ms: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    saida: BaseModel
