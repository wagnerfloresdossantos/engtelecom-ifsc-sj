```mermaid
sequenceDiagram
    autonumber

    actor U as Usuário
    participant T as Triagem
    participant C as Agente comercial
    participant S as Agente de suporte
    participant R as Registro da execução

    rect
        Note over U,C: Atendimento comercial
        U->>T: Quero conhecer os planos de Internet
        T->>C: Encaminha a mensagem inicial
        C->>U: Solicita o CEP
        U->>C: Meu CEP é 88110-000
        C->>U: Informa a cobertura e os planos disponíveis
    end

    rect
        Note over U,S: Mudança para suporte
        U->>C: Já sou cliente e estou sem Internet desde ontem
        C->>T: Solicita nova triagem e informa os fatos relevantes
        T->>S: Encaminha a mensagem e o contexto necessário
        S->>U: Solicita o estado das luzes do equipamento
        U->>S: A luz LOS está vermelha
        S->>U: Encaminha para análise técnica humana
    end

    T-->>R: Registra decisões de encaminhamento
    C-->>R: Registra respostas, latência e tokens
    S-->>R: Registra respostas, latência e tokens
```
    Nota: Neste fluxo, a triagem define o primeiro destino da conversa. O agente especializado permanece ativo enquanto o assunto pertence à sua área e solicita nova triagem quando identifica uma mudança. Durante o reencaminhamento, somente as informações necessárias são transferidas ao próximo agente.