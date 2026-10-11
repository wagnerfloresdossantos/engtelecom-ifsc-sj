from __future__ import annotations

from carregador import renderizar_prompt
from cliente_llm import ClienteLLM
from modelos import (
    EstadoConversa,
    MedicaoChamada,
    SaidaAgenteUnico,
)


class ArquiteturaAgenteUnico:
    def __init__(
        self,
        cliente: ClienteLLM,
        base_conhecimento: str,
    ) -> None:
        self.cliente = cliente

        # Base completa: conteúdo comum e conteúdo das quatro áreas.
        # A reunião desses documentos será feita no executor.
        self.base_conhecimento = base_conhecimento

        # Estado exclusivo desta conversa.
        # Não há especialista ativo na arquitetura de agente único.
        self.estado = EstadoConversa(
            historico=[],
            fatos_relevantes=[],
            agente_ativo=None,
        )

    def _contexto_para_prompt(self) -> list[dict[str, str]]:
        """
        Prepara uma cópia do histórico e dos fatos para o prompt.

        As entradas com role="context" são dados serializados
        pelo carregador, não mensagens enviadas diretamente à API.
        """
        contexto = [
            mensagem.copy()
            for mensagem in self.estado.historico
        ]

        contexto.extend(
            {"role": "context", "content": fato}
            for fato in self.estado.fatos_relevantes
        )

        return contexto

    def processar(
        self,
        mensagem_usuario: str,
    ) -> tuple[str, list[MedicaoChamada]]:
        # O mesmo agente recebe o contexto e a base completa
        # para interpretar e responder a cada mensagem.
        prompt = renderizar_prompt(
            "agente-unico.md",
            self.base_conhecimento,
            self._contexto_para_prompt(),
            mensagem_usuario,
        )

        # Uma chamada principal ao modelo por mensagem.
        medicao = self.cliente.gerar(
            "agente_unico",
            prompt,
            SaidaAgenteUnico,
            mensagem_usuario,
        )
        saida = medicao.saida

        # Verifica se há uma resposta final válida.
        if not saida.response.strip():
            raise RuntimeError(
                "O agente único produziu uma resposta vazia."
            )

        # Um encaminhamento humano exige um destino.
        if (
            saida.action == "handoff_human"
            and saida.handoff_target is None
        ):
            raise RuntimeError(
                "O encaminhamento humano exige handoff_target."
            )

        # Uma resposta comum não deve indicar destino humano.
        if (
            saida.action == "respond"
            and saida.handoff_target is not None
        ):
            raise RuntimeError(
                "Uma resposta comum deve ter handoff_target=None."
            )

        # Mantém todas as mensagens e respostas da conversa.
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

        # A saída fornece a lista atualizada de fatos relevantes.
        # Remove duplicatas, preservando a ordem.
        self.estado.fatos_relevantes = list(
            dict.fromkeys(saida.context_facts)
        )

        # active_area permanece na saída registrada para avaliação.
        # Não altera agente_ativo, pois não há troca de agente aqui.

        # Retorna a resposta e o registro da única chamada.
        return saida.response, [medicao]