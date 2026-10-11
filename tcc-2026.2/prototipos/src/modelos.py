from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel


# Áreas disponíveis nas duas arquiteturas.
# Literal limita o campo aos identificadores definidos abaixo.
AreaAtendimento = Literal[
    "first_contact",  # Primeiro atendimento
    "commercial",    # Comercial
    "ombudsman",     # Ouvidoria
    "support",       # Suporte técnico
]


# Destinos permitidos para encaminhamento ao atendimento humano.
# Esses destinos não representam agentes de IA.
DestinoHumano = Literal[
    "first_contact_human",
    "commercial_human",
    "ombudsman_human",
    "technical_human",
]


# Ações que um agente especializado pode solicitar.
AcaoEspecialista = Literal[
    "respond",         # Responder ao usuário
    "handoff_human",    # Encaminhar para atendimento humano
    "request_reroute", # Solicitar uma nova classificação à triagem
]


# Estrutura da saída do agente único.
# O Pydantic valida os tipos e os valores permitidos.
class SaidaAgenteUnico(BaseModel):
    # Resposta final apresentada ao usuário.
    response: str

    # Intenção identificada na mensagem.
    # As intenções serão definidas durante a elaboração dos cenários.
    intent: str

    # Área identificada pelo agente único.
    # Serve para avaliar a classificação, sem trocar de agente.
    active_area: AreaAtendimento

    # O agente único pode responder ou encaminhar para um humano.
    action: Literal["respond", "handoff_human"]

    # Destino humano quando action for "handoff_human".
    # Nas respostas comuns, deverá receber None.
    handoff_target: DestinoHumano | None

    # Fatos relevantes para a continuidade do atendimento.
    context_facts: list[str]


# Estrutura da saída do agente de triagem.
# A triagem escolhe o especialista, sem responder ao usuário.
class SaidaTriagem(BaseModel):
    # Área selecionada para tratar a mensagem.
    destination: AreaAtendimento

    # Intenção identificada na classificação.
    intent: str

    # Justificativa da escolha, registrada para análise.
    reason: str

    # Fatos encaminhados ao especialista selecionado.
    context_to_forward: list[str]


# Estrutura comum às saídas dos quatro especialistas.
class SaidaEspecialista(BaseModel):
    # Resposta ao usuário.
    # Ao solicitar nova triagem, deverá receber None.
    response: str | None

    # Intenção identificada pelo especialista.
    intent: str

    # Ação solicitada ao orquestrador.
    action: AcaoEspecialista

    # Destino de atendimento humano.
    # Deverá receber None nas ações "respond" e "request_reroute".
    # O próximo especialista será escolhido pela triagem.
    handoff_target: DestinoHumano | None

    # Fatos relevantes que devem permanecer no estado da conversa.
    context_facts: list[str]


# Cada especialista herda os campos de SaidaEspecialista.
# As classes separadas permitem identificar os componentes no código.
# "pass" indica que não há campos adicionais nesta etapa.
class SaidaPrimeiroAtendimento(SaidaEspecialista):
    pass


class SaidaComercial(SaidaEspecialista):
    pass


class SaidaOuvidoria(SaidaEspecialista):
    pass


class SaidaSuporte(SaidaEspecialista):
    pass


# Estado da conversa mantido pelo orquestrador.
# Uma nova instância deverá ser criada para cada conversa.
@dataclass
class EstadoConversa:
    # Mensagens do usuário e respostas apresentadas pelo sistema.
    historico: list[dict[str, str]]

    # Informações relevantes extraídas durante o atendimento.
    fatos_relevantes: list[str]

    # Especialista ativo na arquitetura multiagente.
    # None indica que ainda não há especialista selecionado.
    agente_ativo: AreaAtendimento | None = None


# Registro de uma chamada ao modelo de linguagem.
# Uma mensagem pode gerar várias chamadas na arquitetura multiagente.
@dataclass
class MedicaoChamada:
    # Identificador do agente que realizou a chamada.
    agente: str

    # Tempo gasto na chamada, em milissegundos.
    latencia_ms: float

    # Quantidade de tokens enviados ao modelo.
    input_tokens: int

    # Quantidade de tokens produzidos pelo modelo.
    output_tokens: int

    # Total de tokens informado para a chamada.
    total_tokens: int

    # Saída estruturada e validada pelo Pydantic.
    saida: BaseModel