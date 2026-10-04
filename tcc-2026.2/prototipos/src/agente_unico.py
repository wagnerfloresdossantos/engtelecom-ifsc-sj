from __future__ import annotations

from carregador import renderizar_prompt
from cliente_llm import ClienteLLM
from modelos import MedicaoChamada, SaidaAgenteUnico


class ArquiteturaAgenteUnico:
    def __init__(self, cliente: ClienteLLM, base_comum: str) -> None:
        self.cliente = cliente
        self.base_comum = base_comum
        self.historico: list[dict[str, str]] = []

    def processar(self, mensagem_usuario: str) -> tuple[str, list[MedicaoChamada]]:
        prompt = renderizar_prompt(
            "agente-unico.md",
            self.base_comum,
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
