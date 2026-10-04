from __future__ import annotations

import os
from time import perf_counter
from typing import TypeVar

from pydantic import BaseModel

from modelos import (
    MedicaoChamada,
    SaidaAgenteUnico,
    SaidaComercial,
    SaidaSuporte,
    SaidaTriagem,
)


T = TypeVar("T", bound=BaseModel)


class ClienteLLM:
    def gerar(self, agente: str, prompt: str, esquema: type[T], mensagem: str) -> MedicaoChamada:
        raise NotImplementedError


class ClienteOpenAI(ClienteLLM):
    def __init__(self) -> None:
        from openai import OpenAI

        modelo = os.getenv("TCC_OPENAI_MODEL", "").strip()
        if not modelo:
            raise RuntimeError("Defina TCC_OPENAI_MODEL antes de usar o modo openai.")
        self.modelo = modelo
        self.cliente = OpenAI()

    def gerar(self, agente: str, prompt: str, esquema: type[T], mensagem: str) -> MedicaoChamada:
        inicio = perf_counter()
        resposta = self.cliente.responses.parse(
            model=self.modelo,
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": mensagem},
            ],
            text_format=esquema,
            store=False,
        )
        latencia_ms = (perf_counter() - inicio) * 1000
        saida = resposta.output_parsed
        if saida is None:
            raise RuntimeError(f"O agente {agente} não produziu uma saída estruturada.")

        uso = resposta.usage
        return MedicaoChamada(
            agente=agente,
            latencia_ms=latencia_ms,
            input_tokens=getattr(uso, "input_tokens", 0) or 0,
            output_tokens=getattr(uso, "output_tokens", 0) or 0,
            total_tokens=getattr(uso, "total_tokens", 0) or 0,
            saida=saida,
        )


class ClienteMock(ClienteLLM):
    """Respostas determinísticas para validar a orquestração sem usar API."""

    def gerar(self, agente: str, prompt: str, esquema: type[T], mensagem: str) -> MedicaoChamada:
        inicio = perf_counter()
        texto = mensagem.lower()

        if esquema is SaidaTriagem:
            if any(termo in texto for termo in ("sem internet", "los", "falha")):
                saida = SaidaTriagem(
                    destination="support",
                    intent="suporte_falha_optica" if "los" in texto else "suporte_sem_conexao",
                    reason="A mensagem atual relata falha de conexão.",
                    context_to_forward=[mensagem],
                )
            else:
                saida = SaidaTriagem(
                    destination="commercial",
                    intent="comercial_planos",
                    reason="A mensagem atual solicita informações sobre planos.",
                    context_to_forward=[mensagem],
                )
        elif esquema is SaidaComercial:
            if any(termo in texto for termo in ("sem internet", "los", "falha")):
                saida = SaidaComercial(
                    response=None,
                    intent="suporte_falha_optica" if "los" in texto else "suporte_sem_conexao",
                    action="request_reroute",
                    suggested_destination="support",
                    context_facts=["O usuário informou que já é cliente e está sem Internet."],
                )
            elif "cep" in texto or "88110-000" in texto:
                saida = SaidaComercial(
                    response=(
                        "O CEP 88110-000 está na área atendida. Estão disponíveis "
                        "os planos de 500, 700 e 900 Mbit/s."
                    ),
                    intent="comercial_consulta_cobertura",
                    action="respond",
                    suggested_destination=None,
                    context_facts=["CEP informado: 88110-000"],
                )
            else:
                saida = SaidaComercial(
                    response="Para consultar a disponibilidade, informe seu CEP.",
                    intent="comercial_planos",
                    action="respond",
                    suggested_destination=None,
                    context_facts=["O usuário deseja conhecer os planos."],
                )
        elif esquema is SaidaSuporte:
            if "los" in texto:
                saida = SaidaSuporte(
                    response=(
                        "A luz LOS vermelha pode indicar perda do sinal óptico. "
                        "Vou encaminhar o atendimento para análise técnica."
                    ),
                    intent="suporte_falha_optica",
                    action="handoff_human",
                    suggested_destination="technical_human",
                    context_facts=["Luz LOS vermelha", "Conexão indisponível desde ontem"],
                )
            else:
                saida = SaidaSuporte(
                    response="Qual é o estado das luzes do equipamento de conexão?",
                    intent="suporte_sem_conexao",
                    action="respond",
                    suggested_destination=None,
                    context_facts=["O usuário já é cliente", "Sem Internet desde ontem"],
                )
        elif esquema is SaidaAgenteUnico:
            if "los" in texto:
                saida = SaidaAgenteUnico(
                    response=(
                        "A luz LOS vermelha pode indicar perda do sinal óptico. "
                        "Vou encaminhar o atendimento para análise técnica."
                    ),
                    intent="suporte_falha_optica",
                    active_area="support",
                    action="handoff_human",
                    handoff_target="technical_human",
                    context_facts=["Luz LOS vermelha", "Conexão indisponível desde ontem"],
                )
            elif "sem internet" in texto:
                saida = SaidaAgenteUnico(
                    response="Qual é o estado das luzes do equipamento de conexão?",
                    intent="suporte_sem_conexao",
                    active_area="support",
                    action="respond",
                    handoff_target=None,
                    context_facts=["O usuário já é cliente", "Sem Internet desde ontem"],
                )
            elif "cep" in texto or "88110-000" in texto:
                saida = SaidaAgenteUnico(
                    response=(
                        "O CEP 88110-000 está na área atendida. Estão disponíveis "
                        "os planos de 500, 700 e 900 Mbit/s."
                    ),
                    intent="comercial_consulta_cobertura",
                    active_area="commercial",
                    action="respond",
                    handoff_target=None,
                    context_facts=["CEP informado: 88110-000"],
                )
            else:
                saida = SaidaAgenteUnico(
                    response="Para consultar a disponibilidade, informe seu CEP.",
                    intent="comercial_planos",
                    active_area="commercial",
                    action="respond",
                    handoff_target=None,
                    context_facts=["O usuário deseja conhecer os planos."],
                )
        else:
            raise TypeError(f"Esquema não suportado pelo modo mock: {esquema}")

        latencia_ms = (perf_counter() - inicio) * 1000
        return MedicaoChamada(
            agente=agente,
            latencia_ms=latencia_ms,
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            saida=saida,
        )


def criar_cliente(modo: str) -> ClienteLLM:
    if modo == "mock":
        return ClienteMock()
    if modo == "openai":
        return ClienteOpenAI()
    raise ValueError(f"Modo desconhecido: {modo}. Use mock ou openai.")
