# Diagrama de sequência de bloco


## Conceitual do protocolo
```mermaid
---
    theme: forest
    sequence:
        actorMargin: 100
        boxPadding: 20
        mirrorActors: false
---

sequenceDiagram
    autonumber
    participant C as Cliente
    participant S as Servidor

        C ->> S: Pedido de conexao
        S -->> C: Resposta de conexão

    loop Fluxo de mensagens

        S ->> C: Pedido
        C -->> S: Resposta

    end
    
```
```mermaid
---
    theme: forest
    sequence:
        actorMargin: 100
        boxPadding: 20
        mirrorActors: false
---

sequenceDiagram
    autonumber
    participant C0 as Cliente 
    participant S as Servidor
    participant C1 as Thread Atendimento

    S->>C0: Pedido de conexão
    C0-->>S: Resposta de conexão
    S->>C1: Inicia Thread
    C1->>C0: Atendimento


    
    loop
        C0->>C1: Pedido
        C1-->>C0: Resposta
    end
    S->>C1: Fim

    
```