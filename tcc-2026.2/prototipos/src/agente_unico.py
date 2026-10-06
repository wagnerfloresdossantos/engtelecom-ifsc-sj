from __future__ import annotations

from carregador import renderizar_prompt
from cliente_llm import ClienteLLM
from modelos import MedicaoChamada, SaidaAgenteUnico


class ArquiteturaAgenteUnico:
    def __init__(self, cliente: ClienteLLM, base_conhecimento: str) -> None:
        self.cliente = cliente
        self.base_conhecimento = base_conhecimento
        self.historico: list[dict[str, str]] = []

    def processar(self, mensagem_usuario: str) -> tuple[str, list[MedicaoChamada]]:
        prompt = renderizar_prompt(
            "agente-unico.md",
            self.base_conhecimento,
            self.historico,
            mensagem_usuario,
        )
        medicao = self.cliente.gerar(
            "agente_unico", prompt, SaidaAgenteUnico, mensagem_usuario
        )
        saida = medicao.saida
        self.historico.extend(
            [
                {"role": "user", "content": mensagem_usuario},
                {"role": "assistant", "content": saida.response},
            ]
        )
        return saida.response, [medicao]
