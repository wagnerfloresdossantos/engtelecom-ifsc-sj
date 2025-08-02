# Visão Geral

Este projeto implementa um analisador de quadros PCM30 (E1) para detecção, alinhamento e visualização interativa dos dados TDM.

### 🚀 Funcionalidades:
- Leitura de arquivos contendo sequências binárias.
- Detecção do padrão de alinhamento de quadro (PAQ: `10011011`).
- Validação do bit de sincronismo (bit 256 deve ser `1`).
- Extração de quadros de 256 bits (32 octetos cada).
- Detecção de multiquadros a partir do PAMQ (4 bits iniciais do time slot 16).
- Visualização dos quadros extraídos (individualmente, em grupo ou em tabela).


### ❓ Questões do Exercício

#### a) O código faz o procedimento de alinhamento de quadro e verifica se o sistema permanece alinhado?
✅ Sim.  
A função `detectar_quadros()` encontra o primeiro PAQ válido e, a partir dele, verifica se os quadros seguintes mantêm o alinhamento com base na estrutura do protocolo.  
A função `extrair_time_slots()` valida os blocos somente se:
- O bit de sincronismo (posição 256) for `'1'`
- O PAQ estiver no final (bits 504–511)

#### b) O código encontra e marca o início de cada quadro enquanto estiver alinhado?
✅ Sim.  
A função `detectar_quadros()` armazena as posições dos PAQs válidos na lista `paq_validos`, que representa o início dos quadros alinhados.  
Além disso, o menu interativo permite inspecionar os quadros extraídos, e a aplicação imprime essas posições no terminal com:
```python
print(f"\n\nOs PAQs verdadeiros estão nas posições: {paq_validos}")
