# Fluxo do cenário piloto — arquitetura multiagente

```mermaid
sequenceDiagram
    autonumber

    actor U as Usuário
    participant T as Triagem
    participant C as Agente Comercial
    participant S as Agente de Suporte
    participant R as Registro de Execução

    rect
        Note over U,C: Início do atendimento comercial
        U->>T: Quero conhecer os planos de Internet
        T->>C: Encaminha mensagem e histórico
        C->>U: Solicita o CEP
        U->>C: Meu CEP é 88110-000
        C->>U: Continua o atendimento
    end

    rect
        Note over U,S: Mudança de assunto
        U->>C: Já sou cliente e estou sem Internet
        C->>T: Solicita transferência e envia o histórico
        T->>S: Encaminha a conversa ao suporte
        S->>U: Solicita os dados necessários
        U->>S: A luz LOS está vermelha
        S->>U: Informa o procedimento previsto
    end

    T-->>R: Registra decisões de encaminhamento
    C-->>R: Registra respostas e consumo
    S-->>R: Registra respostas e consumo
```

Neste fluxo, a triagem define o primeiro destino. O agente especializado mantém a conversa e solicita nova triagem somente quando identifica mudança de assunto.
