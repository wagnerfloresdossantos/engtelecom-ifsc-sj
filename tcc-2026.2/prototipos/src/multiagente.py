from __future__ import annotations

from carregador import renderizar_prompt
from cliente_llm import ClienteLLM
from modelos import MedicaoChamada, SaidaComercial, SaidaSuporte, SaidaTriagem


class ArquiteturaMultiagente:
    def __init__(self, cliente: ClienteLLM, bases: dict[str, str]) -> None:
        self.cliente = cliente
        self.bases = bases
        self.historicos: dict[str, list[dict[str, str]]] = {
            "commercial": [],
            "support": [],
        }
        self.contexto_global: list[dict[str, str]] = []
        self.agente_ativo: str | None = None

    def _triar(
        self,
        mensagem_usuario: str,
        solicitacao: dict | None = None,
    ) -> MedicaoChamada:
        prompt = renderizar_prompt(
            "triagem.md",
            self.bases["triage"],
            self.contexto_global,
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
            self.bases[self.agente_ativo],
            self.historicos[self.agente_ativo],
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
            contexto = chamadas[-1].saida.context_to_forward
            self.historicos[self.agente_ativo] = [
                {"role": "context", "content": fato} for fato in contexto
            ]
            especialista = self._especialista(mensagem_usuario)
            chamadas.append(especialista)
            saida = especialista.saida

        if saida.response is None:
            raise RuntimeError("O fluxo terminou sem uma resposta para o usuário.")

        self.historicos[self.agente_ativo].extend(
            [
                {"role": "user", "content": mensagem_usuario},
                {"role": "assistant", "content": saida.response},
            ]
        )
        self.contexto_global = [
            {"role": "context", "content": fato} for fato in saida.context_facts
        ]
        return saida.response, chamadas
