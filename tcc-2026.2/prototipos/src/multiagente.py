from __future__ import annotations

from carregador import renderizar_prompt
from cliente_llm import ClienteLLM
from modelos import (
    EstadoConversa,
    MedicaoChamada,
    SaidaComercial,
    SaidaOuvidoria,
    SaidaPrimeiroAtendimento,
    SaidaSuporte,
    SaidaTriagem,
)


# Relaciona cada área ao arquivo de prompt e ao esquema de saída.
ESPECIALISTAS = {
    "first_contact": (
        "primeiro-atendimento.md",
        SaidaPrimeiroAtendimento,
    ),
    "commercial": (
        "comercial.md",
        SaidaComercial,
    ),
    "ombudsman": (
        "ouvidoria.md",
        SaidaOuvidoria,
    ),
    "support": (
        "suporte.md",
        SaidaSuporte,
    ),
}


class ArquiteturaMultiagente:
    def __init__(
        self,
        cliente: ClienteLLM,
        bases: dict[str, str],
    ) -> None:
        self.cliente = cliente
        self.bases = bases

        # Estado exclusivo desta conversa.
        # O histórico permanece disponível mesmo após a troca de agente.
        self.estado = EstadoConversa(
            historico=[],
            fatos_relevantes=[],
            agente_ativo=None,
        )

    def _contexto_para_prompt(
        self,
        fatos_adicionais: list[str] | None = None,
    ) -> list[dict[str, str]]:
        """
        Prepara uma cópia do histórico e dos fatos para o prompt.

        As entradas com role="context" são apenas dados serializados
        pelo carregador, não mensagens enviadas diretamente à API.
        """
        contexto = [
            mensagem.copy()
            for mensagem in self.estado.historico
        ]

        # Evita repetir fatos iguais na mesma entrada.
        fatos = list(
            dict.fromkeys(
                self.estado.fatos_relevantes
                + (fatos_adicionais or [])
            )
        )

        contexto.extend(
            {"role": "context", "content": fato}
            for fato in fatos
        )

        return contexto

    def _triar(
        self,
        mensagem_usuario: str,
        solicitacao: dict | None = None,
    ) -> MedicaoChamada:
        # A triagem recebe o histórico e os fatos da conversa.
        # Quando há mudança de assunto, também recebe a solicitação
        # produzida pelo especialista anterior.
        prompt = renderizar_prompt(
            "triagem.md",
            self.bases["triage"],
            self._contexto_para_prompt(),
            mensagem_usuario,
            solicitacao,
        )

        medicao = self.cliente.gerar(
            "triagem",
            prompt,
            SaidaTriagem,
            mensagem_usuario,
        )

        destino = medicao.saida.destination

        # Verifica se a área escolhida possui uma base carregada.
        # O orquestrador valida a configuração, sem escolher outra área.
        if destino not in self.bases:
            raise RuntimeError(
                f"Base de conhecimento não carregada para: {destino}."
            )

        # Somente a decisão da triagem define o especialista ativo.
        self.estado.agente_ativo = destino

        return medicao

    def _especialista(
        self,
        mensagem_usuario: str,
        contexto_encaminhado: list[str] | None = None,
    ) -> MedicaoChamada:
        area = self.estado.agente_ativo

        if area is None or area not in ESPECIALISTAS:
            raise RuntimeError(
                "Nenhum agente especializado válido está ativo."
            )

        arquivo, esquema = ESPECIALISTAS[area]

        # O especialista recebe sua base específica, o histórico
        # completo e os fatos relevantes disponíveis.
        prompt = renderizar_prompt(
            arquivo,
            self.bases[area],
            self._contexto_para_prompt(contexto_encaminhado),
            mensagem_usuario,
        )

        return self.cliente.gerar(
            area,
            prompt,
            esquema,
            mensagem_usuario,
        )

    def processar(
        self,
        mensagem_usuario: str,
    ) -> tuple[str, list[MedicaoChamada]]:
        # Todas as chamadas são registradas, inclusive aquelas
        # que apenas solicitam uma nova triagem.
        chamadas: list[MedicaoChamada] = []
        contexto_encaminhado: list[str] = []

        # A primeira mensagem exige uma triagem inicial.
        if self.estado.agente_ativo is None:
            triagem = self._triar(mensagem_usuario)
            chamadas.append(triagem)

            contexto_encaminhado = (
                triagem.saida.context_to_forward
            )

        # Nas mensagens seguintes, o especialista ativo é mantido.
        especialista = self._especialista(
            mensagem_usuario,
            contexto_encaminhado,
        )
        chamadas.append(especialista)
        saida = especialista.saida

        # O especialista pode identificar que o assunto mudou,
        # mas não escolhe diretamente o próximo agente.
        if saida.action == "request_reroute":
            if (
                saida.response is not None
                or saida.handoff_target is not None
            ):
                
                raise RuntimeError(
                    "Saída inconsistente ao solicitar nova triagem. "
                    f"Agente: {especialista.agente}; "
                    f"mensagem: {mensagem_usuario!r}; "
                    f"saída: {saida.model_dump()!r}"
                )
            

            triagem = self._triar(
                mensagem_usuario,
                solicitacao=saida.model_dump(),
            )
            chamadas.append(triagem)

            # O especialista escolhido pela nova triagem processa
            # a mesma mensagem, agora com o contexto encaminhado.
            especialista = self._especialista(
                mensagem_usuario,
                triagem.saida.context_to_forward,
            )
            chamadas.append(especialista)
            saida = especialista.saida

            # Limita o processamento a uma nova triagem por mensagem.
            # Uma segunda solicitação indica falha do fluxo e deve
            # ser investigada, em vez de gerar um ciclo indefinido.
            if saida.action == "request_reroute":
                raise RuntimeError(
                    "O especialista selecionado solicitou outra "
                    "triagem para a mesma mensagem."
                )

        # Uma resposta final precisa conter texto.
        if saida.response is None or not saida.response.strip():
            raise RuntimeError(
                "O fluxo terminou sem uma resposta para o usuário."
            )

        # Verifica a consistência do encaminhamento humano.
        if (
            saida.action == "handoff_human"
            and saida.handoff_target is None
        ):
            raise RuntimeError(
                "O encaminhamento humano exige handoff_target."
            )

        if (
            saida.action == "respond"
            and saida.handoff_target is not None
        ):
            raise RuntimeError(
                "Uma resposta comum deve ter handoff_target=None."
            )

        # Registra somente a mensagem do usuário e a resposta final.
        # As decisões internas ficam na lista de chamadas.
        self.estado.historico.extend(
            [
                {
                    "role": "user",
                    "content": mensagem_usuario,
                },
                {
                    "role": "assistant",
                    "content": saida.response,
                },
            ]
        )

        # A saída final fornece a lista atualizada de fatos.
        # O histórico completo continua preservado separadamente.
        self.estado.fatos_relevantes = list(
            dict.fromkeys(saida.context_facts)
        )

        return saida.response, chamadas