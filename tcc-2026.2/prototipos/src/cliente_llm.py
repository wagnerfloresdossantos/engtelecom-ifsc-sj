# =============================================================================
# Cliente LLM — v0.2.1
# Changelog em relação à v0.1 — 12/10/2026
#
# Correção v0.2.1 sobre v0.2.0:
# - Extraídas as entradas role="context" da lista JSON produzida pelo
#   carregador, preservando fatos entre turnos nas duas arquiteturas.
# - Validado o piloto-002 com carregador e arquiteturas fornecidos,
#   incluindo fatos técnicos e resumos nos turnos 5, 6 e 7.
#
# Objetivo: ampliar o mock para executar o cenário piloto-002, que percorre
# as quatro áreas e retorna ao comercial para recuperar o CEP anterior.
#
# Modificações:
# - Incluídos primeiro atendimento e ouvidoria no ClienteMock.
# - Ampliadas a triagem e a simulação do agente único para as quatro áreas.
# - Incluída nova triagem nas mudanças de assunto, sem escolha direta do
#   próximo especialista pelo especialista ativo.
# - Incluídos pedidos explícitos de atendimento humano e destinos por área.
# - Incluída leitura determinística do histórico e dos fatos relevantes
#   fornecidos na seção correspondente do prompt.
# - Incluída recuperação do CEP após mudanças de área, sem nova coleta.
# - Ampliado o comercial para disponibilidade e condições ausentes da base.
# - Incluídos os fluxos iniciais de reclamação e revisão de atendimento.
# - Incluído o fluxo de luzes verdes: reinicialização da ONT pela energia
#   por 30 segundos e atendimento humano se a conexão não for restabelecida.
# - Incluído reconhecimento da saudação inicial usada no piloto-002.
# - Ajustados os resumos humanos para preservar início da falha, estado
#   das luzes, reinicialização sem restabelecimento e relato de recorrência.
# - Removidas suposições fixas do piloto original, como registrar
#   "desde ontem" quando essa informação não foi fornecida.
#
# Compatibilidade:
# - Mantidas a interface gerar(), a fábrica criar_cliente() e as chamadas
#   reais do ClienteOpenAI; utilizados os esquemas de modelos.py.
# - O cliente não mantém memória própria: o estado pertence ao orquestrador.
#
# Validação:
# - Realizadas 25 verificações locais na ampliação inicial.
# - Conferidos os oito turnos do piloto-002 nas simulações das duas
#   arquiteturas, incluindo intenções, ações, destinos e rotas multiagente.
# - Integração com o orquestrador real ainda pendente de validação.
#
# Limitações:
# - O mock é determinístico e não interpreta livremente os prompts.
# - As regras reproduzem as bases fornecidas, incluindo base-suporte 0.3.2;
#   alterações nas bases podem exigir atualização do simulador.
# - Os testes do mock não avaliam qualidade de LLM, custo ou latência da API.
# - A versão deste arquivo é independente da versão geral do protótipo,
#   dos prompts, das bases e dos cenários.
# =============================================================================

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
    SaidaPrimeiroAtendimento,
    SaidaOuvidoria,
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
    """Simulador determinístico das quatro áreas, triagem e agente único.

    Não interpreta regras arbitrárias dos prompts nem mede qualidade de LLM.
    Lê apenas a seção renderizada de histórico e fatos relevantes do prompt.
    O estado continua pertencendo ao orquestrador; não há memória no cliente.
    As respostas reproduzem as bases fornecidas em 12/10/2026, incluindo
    base-suporte 0.3.2. Mudanças nas bases exigem atualização deste simulador.
    """

    AREAS = {
        SaidaPrimeiroAtendimento: "first_contact",
        SaidaComercial: "commercial",
        SaidaOuvidoria: "ombudsman",
        SaidaSuporte: "support",
    }
    HUMANOS = {
        "first_contact": "first_contact_human",
        "commercial": "commercial_human",
        "ombudsman": "ombudsman_human",
        "support": "technical_human",
    }

    @staticmethod
    def _normalizar(texto: str) -> str:
        import unicodedata
        return "".join(c for c in unicodedata.normalize("NFD", texto.lower())
                       if unicodedata.category(c) != "Mn")

    @staticmethod
    def _contexto(prompt: str) -> tuple[list[dict[str, str]], list[str]]:
        """Aceita JSON de estado ou texto nesta seção; ignora exemplos da base.

        JSON recomendado: {"historico": [{"role": "user", "content": "..."}],
        "fatos_relevantes": ["..."]}. Texto livre fica como contexto auxiliar.
        """
        import json
        import re
        trecho = re.search(
            r"### Histórico e fatos relevantes\s*\n(.*?)(?=\n### |\Z)",
            prompt, re.S,
        )
        if not trecho:
            return [], []
        bruto = trecho.group(1).strip()
        if not bruto or bruto == "{{historico}}":
            return [], []
        if bruto.startswith("```json"):
            bruto = bruto.removeprefix("```json").removesuffix("```").strip()
        try:
            valor = json.loads(bruto)
        except json.JSONDecodeError:
            return [], [bruto]
        if isinstance(valor, list):
            if all(isinstance(x, str) for x in valor):
                return [], valor
            entradas = [x for x in valor if isinstance(x, dict)]
            return ([x for x in entradas if x.get("role") != "context"],
                    [x["content"] for x in entradas
                     if x.get("role") == "context"
                     and isinstance(x.get("content"), str)])
        if isinstance(valor, dict):
            historico = valor.get("historico", valor.get("messages", []))
            fatos = valor.get("fatos_relevantes", valor.get("context_facts", []))
            return ([x for x in historico if isinstance(x, dict)],
                    [x for x in fatos if isinstance(x, str)])
        return [], []

    def _classificar(self, texto: str, anterior: str) -> tuple[str, str]:
        import re
        t = self._normalizar(texto)
        h = self._normalizar(anterior)
        reclamacao = bool(re.search(r"\b(reclamacao|reclamar|ouvidoria)\b", t))
        revisao = any(x in t for x in ("revisao", "revisar", "reavaliar"))
        comercial = bool(re.search(r"\b(planos?|precos?|cobertura|contratar|contratacao|cep|instalacao|beneficios|desconto)\b", t))
        suporte = bool(re.search(r"\b(los|luzes|ont|roteador|wifi|wi-fi|lenta|lentidao|reiniciei)\b", t)) or any(x in t for x in ("sem internet", "sem conexao", "internet caiu", "nao voltou"))
        if reclamacao or revisao:
            return "ombudsman", "ouvidoria_revisao_atendimento" if revisao else "ouvidoria_reclamacao"
        if comercial and suporte:
            return "first_contact", "necessidade_nao_identificada"
        if comercial or re.search(r"\b\d{5}-?\d{3}\b", t):
            intent = "comercial_consulta_cobertura" if re.search(r"\b\d{5}-?\d{3}\b", t) or "cobertura" in t else "comercial_contratacao" if any(x in t for x in ("contratar", "contratacao", "preco", "instalacao", "beneficio", "desconto")) else "comercial_planos"
            return "commercial", intent
        # Uma explicação técnica pode continuar uma reclamação já iniciada.
        mudanca = any(x in t for x in ("em vez", "agora quero", "deixe", "esqueca", "na verdade", "so quero"))
        if suporte:
            if any(x in h for x in ("reclamacao", "reclamar", "revisao")) and not mudanca:
                return "ombudsman", "ouvidoria_revisao_atendimento" if "revisao" in h else "ouvidoria_reclamacao"
            return "support", "suporte_falha_optica" if "los" in t and "vermelh" in t else "suporte_sem_conexao" if any(x in t for x in ("sem internet", "sem conexao", "nao voltou", "luzes", "reiniciei")) else "suporte_dificuldade_tecnica"
        if any(x in t for x in ("horario", "endereco", "telefone", "servicos", "o que voces oferecem", "contato")):
            return "first_contact", "primeiro_atendimento_informacoes"
        if t.strip(" .!?😊") == "ola, preciso de ajuda" or t.strip(" .!?😊") in ("oi", "ola", "bom dia", "boa tarde", "boa noite", "preciso de ajuda"):
            return "first_contact", "primeiro_atendimento_inicio"
        # Respostas curtas e pedidos de humano usam a necessidade anterior.
        if h and (len(t.split()) <= 6 or self._humano(t)):
            area, intent = self._classificar(anterior, "")
            if area != "first_contact":
                return area, intent
        return "first_contact", "necessidade_nao_identificada"

    def _humano(self, texto: str) -> bool:
        t = self._normalizar(texto)
        return any(x in t for x in ("humano", "atendente", "pessoa de verdade")) and not any(x in t for x in ("nao quero", "nao preciso", "sem atendente"))

    def gerar(self, agente: str, prompt: str, esquema: type[T],
              mensagem: str) -> MedicaoChamada:
        import re
        inicio = perf_counter()
        if esquema not in (*self.AREAS, SaidaTriagem, SaidaAgenteUnico):
            raise TypeError(f"Esquema não suportado pelo modo mock: {esquema}")
        historico, fatos = self._contexto(prompt)
        usuarios = [str(x.get("content", "")) for x in historico
                    if x.get("role") == "user"]
        anterior = usuarios[-1] if usuarios else " ".join(fatos)
        area, intent = self._classificar(mensagem, anterior)
        t = self._normalizar(mensagem)
        contexto = " ".join([*usuarios, *fatos, mensagem])
        completo = self._normalizar(contexto)

        # Extração simples e explícita de fatos; nunca pressupõe 'desde ontem'.
        fatos = list(fatos)
        ceps = re.findall(r"\b(\d{5})-?(\d{3})\b", contexto)
        cep = "-".join(ceps[-1]) if ceps else None
        if cep:
            fatos = [f for f in fatos if not f.startswith("CEP informado:")]
            fatos.append(f"CEP informado: {cep}")
        if "ja sou cliente" in t:
            fatos.append("O usuário informou que já é cliente.")
        if "sem internet" in t or "sem conexao" in t:
            fatos.append("O usuário relata conexão indisponível" +
                         (" desde ontem." if "desde ontem" in t else "."))
        if "los" in t and "vermelh" in t:
            fatos = [f for f in fatos if not f.startswith("Estado das luzes:")]
            fatos.append("Estado das luzes: LOS vermelha.")
        if "verde" in t and ("luz" in t or "luzes" in t or "ont" in t):
            fatos = [f for f in fatos if not f.startswith("Estado das luzes:")]
            fatos.append("Estado das luzes: verdes.")
        if "reiniciei" in t or "ja reinic" in t:
            fatos.append("Reinicialização realizada pelo usuário.")
            if "sem internet" in t or "continua" in t:
                fatos.append("Conexão continua indisponível após a reinicialização, segundo o usuário.")
        if self._humano(mensagem):
            fatos.append("O usuário solicita atendimento humano.")
        if area == "ombudsman":
            fatos.append("Manifestação declarada pelo usuário: " + mensagem)
        if area == "commercial" and "plano" in t:
            fatos.append("Interesse comercial declarado: " + mensagem)
        protocolos = re.findall(r"protocolo\s*[:#]?\s*([\w-]+)", mensagem, re.I)
        for protocolo in protocolos:
            fatos.append(f"Protocolo declarado pelo usuário: {protocolo}")
        fatos = list(dict.fromkeys(fatos))

        if esquema is SaidaTriagem:
            saida = esquema(destination=area, intent=intent,
                            reason=f"Regra determinística do mock identificou a área {area}.",
                            context_to_forward=fatos)
        elif esquema is not SaidaAgenteUnico and self.AREAS[esquema] != area:
            saida = esquema(response=None, intent=intent, action="request_reroute",
                            handoff_target=None, context_facts=fatos)
        else:
            action, destino = "respond", None
            humano = self._humano(mensagem) or "O usuário solicita atendimento humano." in fatos
            resumo = "; ".join(f for f in fatos if not f.startswith(("CEP informado:", "Interesse comercial", "Orientação apresentada:"))) or mensagem
            if area == "commercial":
                resumo = "; ".join(f for f in fatos if f.startswith(("CEP informado:", "Interesse comercial"))) or mensagem
            if humano:
                action = "handoff_human"
                resposta = f"É necessário continuar com atendimento humano. Resumo: {resumo}"
            elif area == "first_contact":
                if intent == "primeiro_atendimento_inicio":
                    resposta = "Olá! Como posso ajudar?"
                elif intent == "primeiro_atendimento_informacoes":
                    resposta = ("O Provedor Alfa oferece Internet por fibra óptica e atendimento comercial, técnico e de reclamações."
                                if any(x in t for x in ("servicos", "oferecem"))
                                else "Essa informação não está disponível na base de conhecimento.")
                else:
                    resposta = "Qual necessidade você deseja tratar primeiro?" if " e " in t else "Pode descrever o que você precisa?"
            elif area == "commercial":
                if intent == "comercial_contratacao":
                    action = "handoff_human"
                    resposta = f"As condições de contratação, preços e taxas não estão definidos na base. É necessário atendimento comercial humano. Resumo: {resumo}"
                elif not cep:
                    resposta = "Para consultar a disponibilidade, informe seu CEP."
                elif cep == "88110-000":
                    resposta = "O CEP 88110-000 está na área atendida. Estão disponíveis planos de 500, 700 e 900 Mbit/s."
                else:
                    action = "handoff_human"
                    resposta = f"A disponibilidade para o CEP {cep} não está definida na base. É necessário atendimento comercial humano para confirmação."
            elif area == "ombudsman":
                descrito = any(x in completo for x in ("sem internet", "sem conexao", "desde", "cobranca", "nao resolveu", "nao fui atendido", "protocolo", "recorrente"))
                if descrito:
                    action = "handoff_human"
                    resposta = f"Entendo sua manifestação. É necessário continuar com atendimento humano de ouvidoria. Resumo: {resumo}"
                else:
                    resposta = "Qual ponto do atendimento você deseja reavaliar?" if intent == "ouvidoria_revisao_atendimento" else "Sobre qual situação você deseja registrar a reclamação?"
            else:
                # Usa o estado mais recente, respeitando correções de cor.
                cores = [f for f in fatos if f.startswith("Estado das luzes:")]
                estado = self._normalizar(cores[-1]) if cores else completo
                reiniciou = "Reinicialização realizada pelo usuário." in fatos or "reiniciei" in completo or "ja reinic" in completo
                if "los" in estado and "vermelh" in estado:
                    intent, action = "suporte_falha_optica", "handoff_human"
                    resposta = f"A luz LOS vermelha pode indicar perda do sinal óptico relacionada à indisponibilidade. É necessário atendimento técnico humano. Resumo: {resumo}"
                elif "verde" in estado:
                    if reiniciou and ("sem internet" in t or "nao voltou" in t or "continua" in t):
                        action = "handoff_human"
                        resposta = f"A conexão continua indisponível após a reinicialização. É necessário atendimento técnico humano. Resumo: {resumo}"
                    elif reiniciou:
                        resposta = "A conexão voltou após a reinicialização?"
                    else:
                        resposta = "Desligue a ONT da energia, aguarde 30 segundos e ligue novamente, sem usar o botão RESET. A conexão voltou após esse procedimento?"
                        fatos.append("Orientação apresentada: desligar a ONT da energia por 30 segundos e verificar se a conexão voltou.")
                elif intent == "suporte_dificuldade_tecnica":
                    action = "handoff_human"
                    resposta = f"Não há procedimento correspondente a essa dificuldade na base. É necessário atendimento técnico humano. Resumo: {resumo}"
                else:
                    resposta = "Qual é o estado das luzes do equipamento de conexão?"
            if action == "handoff_human":
                destino = self.HUMANOS[area]
            campos = dict(response=resposta, intent=intent, action=action,
                          handoff_target=destino, context_facts=fatos)
            if esquema is SaidaAgenteUnico:
                campos["active_area"] = area
            saida = esquema(**campos)
        return MedicaoChamada(agente=agente,
                              latencia_ms=(perf_counter() - inicio) * 1000,
                              input_tokens=0, output_tokens=0, total_tokens=0,
                              saida=saida)


def criar_cliente(modo: str) -> ClienteLLM:
    if modo == "mock":
        return ClienteMock()
    if modo == "openai":
        return ClienteOpenAI()
    raise ValueError(f"Modo desconhecido: {modo}. Use mock ou openai.")
