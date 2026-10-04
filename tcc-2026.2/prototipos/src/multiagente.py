from __future__ import annotations

from carregador import renderizar_prompt
from cliente_llm import ClienteLLM
from modelos import MedicaoChamada, SaidaComercial, SaidaSuporte, SaidaTriagem


class ArquiteturaMultiagente:
    def __init__(self, cliente: ClienteLLM, base_comum: str) -> None:
        self.cliente = cliente
        self.base_comum = base_comum
        self.historico: list[dict[str, str]] = []
        self.agente_ativo: str | None = None

    def _triar(
        self,
        mensagem_usuario: str,
        solicitacao: dict | None = None,
    ) -> MedicaoChamada:
        prompt = renderizar_prompt(
            "triagem.md",
            self.base_comum,
            self.historico,
            mensagem_usuario,
            solicitacao,
        )
        medicao = self.cliente.gerar("triagem", prompt, SaidaTriagem, mensagem_usuario)
        self.agente_ativo = medicao.saida.destination
        return medicao

    def _especialista(self, mensagem_usuario: str) -> MedicaoChamada:
        if self.agente_ativo == "commercial":
            arquivo, esquema = "comercial.md", SaidaComercial
        elif self.agente_ativo == "support":
            arquivo, esquema = "suporte.md", SaidaSuporte
        else:
            raise RuntimeError("Nenhum agente especializado está ativo.")

        prompt = renderizar_prompt(
            arquivo,
            self.base_comum,
            self.historico,
            mensagem_usuario,
        )
        return self.cliente.gerar(self.agente_ativo, prompt, esquema, mensagem_usuario)

    def processar(self, mensagem_usuario: str) -> tuple[str, list[MedicaoChamada]]:
        chamadas: list[MedicaoChamada] = []

        if self.agente_ativo is None:
            chamadas.append(self._triar(mensagem_usuario))

        especialista = self._especialista(mensagem_usuario)
        chamadas.append(especialista)
        saida = especialista.saida

        if saida.action == "request_reroute":
            solicitacao = saida.model_dump()
            chamadas.append(self._triar(mensagem_usuario, solicitacao))
            especialista = self._especialista(mensagem_usuario)
            chamadas.append(especialista)
            saida = especialista.saida

        if saida.response is None:
            raise RuntimeError("O fluxo terminou sem uma resposta para o usuário.")

        self.historico.extend(
            [
                {"role": "user", "content": mensagem_usuario},
                {"role": "assistant", "content": saida.response},
            ]
        )
        return saida.response, chamadas
