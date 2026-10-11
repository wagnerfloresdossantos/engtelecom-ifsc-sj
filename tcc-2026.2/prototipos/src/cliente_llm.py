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


# Representa qualquer esquema de saída baseado em BaseModel.
T = TypeVar("T", bound=BaseModel)


# Interface comum aos clientes real e simulado.
# As arquiteturas utilizam o mesmo método nos dois modos.
class ClienteLLM:
    def gerar(
        self,
        agente: str,
        prompt: str,
        esquema: type[T],
        mensagem: str,
    ) -> MedicaoChamada:
        raise NotImplementedError


# Cliente responsável pelas chamadas reais à OpenAI.
class ClienteOpenAI(ClienteLLM):
    def __init__(self) -> None:
        # Importação feita somente ao utilizar o cliente real.
        from openai import OpenAI

        # O modelo deve ser configurado no ambiente ou no arquivo .env.
        modelo = os.getenv("TCC_OPENAI_MODEL", "").strip()

        if not modelo:
            raise RuntimeError(
                "Defina TCC_OPENAI_MODEL antes de usar o modo openai."
            )

        self.modelo = modelo

        # O SDK utiliza a variável OPENAI_API_KEY.
        self.cliente = OpenAI()

    def gerar(
        self,
        agente: str,
        prompt: str,
        esquema: type[T],
        mensagem: str,
    ) -> MedicaoChamada:
        # Mede o tempo da chamada, incluindo a obtenção da saída.
        inicio = perf_counter()

        resposta = self.cliente.responses.parse(
            model=self.modelo,
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": mensagem},
            ],
            # Solicita uma saída estruturada conforme o modelo Pydantic.
            text_format=esquema,
            store=False,
        )

        latencia_ms = (perf_counter() - inicio) * 1000
        saida = resposta.output_parsed

        # Uma chamada sem saída estruturada não pode continuar o fluxo.
        if saida is None:
            raise RuntimeError(
                f"O agente {agente} não produziu uma saída estruturada."
            )

        # Registra o consumo informado pela API.
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
    """
    Simula respostas para verificar a orquestração sem utilizar a API.

    Nesta etapa, cobre somente o piloto comercial e técnico.
    As respostas são fixas e não avaliam a qualidade dos prompts,
    a interpretação do histórico ou a retenção real do contexto.
    """

    def gerar(
        self,
        agente: str,
        prompt: str,
        esquema: type[T],
        mensagem: str,
    ) -> MedicaoChamada:
        inicio = perf_counter()

        # Normaliza a mensagem para as verificações simples do piloto.
        texto = mensagem.lower()

        # ------------------------------------------------------------
        # Triagem: escolhe o especialista inicial ou o novo especialista.
        # ------------------------------------------------------------
        if esquema is SaidaTriagem:
            if any(
                termo in texto
                for termo in ("sem internet", "los", "falha")
            ):
                saida = SaidaTriagem(
                    destination="support",
                    intent=(
                        "suporte_falha_optica"
                        if "los" in texto
                        else "suporte_sem_conexao"
                    ),
                    reason="A mensagem atual relata falha de conexão.",
                    context_to_forward=[mensagem],
                )
            else:
                saida = SaidaTriagem(
                    destination="commercial",
                    intent="comercial_planos",
                    reason=(
                        "A mensagem atual solicita informações sobre planos."
                    ),
                    context_to_forward=[mensagem],
                )

        # ------------------------------------------------------------
        # Comercial: responde ou solicita nova triagem.
        # ------------------------------------------------------------
        elif esquema is SaidaComercial:
            if any(
                termo in texto
                for termo in ("sem internet", "los", "falha")
            ):
                saida = SaidaComercial(
                    # O especialista não responde ao usuário neste caso.
                    response=None,
                    intent=(
                        "suporte_falha_optica"
                        if "los" in texto
                        else "suporte_sem_conexao"
                    ),
                    action="request_reroute",

                    # A triagem escolherá o próximo especialista.
                    # Este campo é reservado ao atendimento humano.
                    handoff_target=None,
                    context_facts=[
                        "O usuário informou que já é cliente "
                        "e está sem Internet."
                    ],
                )

            elif "cep" in texto or "88110-000" in texto:
                saida = SaidaComercial(
                    # Resposta fixa para o CEP previsto no cenário piloto.
                    response=(
                        "O CEP 88110-000 está na área atendida. "
                        "Estão disponíveis os planos de "
                        "500, 700 e 900 Mbit/s."
                    ),
                    intent="comercial_consulta_cobertura",
                    action="respond",
                    handoff_target=None,
                    context_facts=["CEP informado: 88110-000"],
                )

            else:
                saida = SaidaComercial(
                    response=(
                        "Para consultar a disponibilidade, informe seu CEP."
                    ),
                    intent="comercial_planos",
                    action="respond",
                    handoff_target=None,
                    context_facts=[
                        "O usuário deseja conhecer os planos."
                    ],
                )

        # ------------------------------------------------------------
        # Suporte: coleta informações ou encaminha para um humano.
        # ------------------------------------------------------------
        elif esquema is SaidaSuporte:
            if "los" in texto:
                saida = SaidaSuporte(
                    response=(
                        "A luz LOS vermelha pode indicar perda "
                        "do sinal óptico. Vou encaminhar o atendimento "
                        "para análise técnica."
                    ),
                    intent="suporte_falha_optica",
                    action="handoff_human",

                    # Destino humano previsto no cenário piloto.
                    handoff_target="technical_human",

                    # Fatos fixos do piloto, sem extração real do histórico.
                    context_facts=[
                        "Luz LOS vermelha",
                        "Conexão indisponível desde ontem",
                    ],
                )
            else:
                saida = SaidaSuporte(
                    response=(
                        "Qual é o estado das luzes "
                        "do equipamento de conexão?"
                    ),
                    intent="suporte_sem_conexao",
                    action="respond",
                    handoff_target=None,
                    context_facts=[
                        "O usuário já é cliente",
                        "Sem Internet desde ontem",
                    ],
                )

        # ------------------------------------------------------------
        # Agente único: trata as duas áreas sem trocar de agente.
        # ------------------------------------------------------------
        elif esquema is SaidaAgenteUnico:
            if "los" in texto:
                saida = SaidaAgenteUnico(
                    response=(
                        "A luz LOS vermelha pode indicar perda "
                        "do sinal óptico. Vou encaminhar o atendimento "
                        "para análise técnica."
                    ),
                    intent="suporte_falha_optica",
                    active_area="support",
                    action="handoff_human",
                    handoff_target="technical_human",
                    context_facts=[
                        "Luz LOS vermelha",
                        "Conexão indisponível desde ontem",
                    ],
                )

            elif "sem internet" in texto:
                saida = SaidaAgenteUnico(
                    response=(
                        "Qual é o estado das luzes "
                        "do equipamento de conexão?"
                    ),
                    intent="suporte_sem_conexao",
                    active_area="support",
                    action="respond",
                    handoff_target=None,
                    context_facts=[
                        "O usuário já é cliente",
                        "Sem Internet desde ontem",
                    ],
                )

            elif "cep" in texto or "88110-000" in texto:
                saida = SaidaAgenteUnico(
                    response=(
                        "O CEP 88110-000 está na área atendida. "
                        "Estão disponíveis os planos de "
                        "500, 700 e 900 Mbit/s."
                    ),
                    intent="comercial_consulta_cobertura",
                    active_area="commercial",
                    action="respond",
                    handoff_target=None,
                    context_facts=["CEP informado: 88110-000"],
                )

            else:
                saida = SaidaAgenteUnico(
                    response=(
                        "Para consultar a disponibilidade, informe seu CEP."
                    ),
                    intent="comercial_planos",
                    active_area="commercial",
                    action="respond",
                    handoff_target=None,
                    context_facts=[
                        "O usuário deseja conhecer os planos."
                    ],
                )

        else:
            # Evita simular silenciosamente um agente ainda não implementado.
            raise TypeError(
                f"Esquema não suportado pelo modo mock: {esquema}"
            )

        # No modo simulado, a latência mede somente o processamento local.
        # Ela não deve ser comparada com a latência das chamadas reais.
        latencia_ms = (perf_counter() - inicio) * 1000

        return MedicaoChamada(
            agente=agente,
            latencia_ms=latencia_ms,

            # Não há consumo de tokens no modo simulado.
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            saida=saida,
        )


# Seleciona o cliente utilizado pelas duas arquiteturas.
def criar_cliente(modo: str) -> ClienteLLM:
    if modo == "mock":
        return ClienteMock()

    if modo == "openai":
        return ClienteOpenAI()

    raise ValueError(
        f"Modo desconhecido: {modo}. Use mock ou openai."
    )