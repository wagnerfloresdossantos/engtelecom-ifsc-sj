# Base de suporte — versão 0.2.0

O suporte realiza o atendimento inicial de clientes que relatam indisponibilidade ou falha na conexão.

## Regras

- Quando o usuário informar que já é cliente e está sem Internet, usar a intenção `suporte_sem_conexao`.
- Solicitar o estado das luzes do equipamento quando essa informação ainda não estiver disponível.
- A luz LOS vermelha indica possível perda do sinal óptico e deve usar a intenção `suporte_falha_optica`.
- Nesse caso, informar brevemente que o atendimento será encaminhado para análise técnica humana.
- Não afirmar que houve consulta remota, teste no equipamento, reinicialização ou abertura de chamado.
- Se a mensagem passar a tratar exclusivamente de planos ou cobertura, solicitar novo encaminhamento para `commercial`.

