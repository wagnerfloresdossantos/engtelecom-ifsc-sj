import re
import pandas as pd

def ler_dado_arquivo(nome_arquivo):
    """
    Lê o conteúdo de um arquivo texto contendo bits.
    Remove tudo que não for 0 ou 1.
    """
    with open(nome_arquivo) as arq:
        dado = arq.read()
        return re.sub(r'[^01]', '', dado)


def extrair_time_slots(dado, paq, pos_inicio):
    """
    Extrai os time slots (de 8 em 8 bits) se:
    - Bit HDB3 (posição 256) == '1'
    - PAQ (10011011) está no final do quadro (pos 504–511)
    """
    A = 256
    fim = 512
    time_slots = []

    if len(dado) >= fim + 8 and dado[A:A+1] == '1' and dado[fim:fim + 8] == paq:
        print(f"\n[Quadro detectado em bit {pos_inicio}] {dado[0:fim]}")
        time_slots = [dado[j:j+8] for j in range(0, fim, 8)]

    return time_slots


def detectar_quadros(dado, paq):
    """
    Procura o PAQ no fluxo e valida quadros a partir dele.
    Retorna lista de quadros válidos e posições dos PAQs.
    """
    pos = 0
    quadro = []
    paq_validos = []

    while True:
        pos = dado.find(paq, pos)
        if pos == -1:
            break

        trecho = dado[pos:]
        time_slots = extrair_time_slots(trecho, paq, pos)

        if time_slots:
            paq_validos.append(pos)
            quadro += [time_slots[:32], time_slots[32:]]

        pos += 1

    return quadro, paq_validos


def extrair_multiquadro(pamq, quadros):
    """
    Extrai sequência contínua de quadros iniciando com TS16 = pamq.
    """
    multiquadro = []

    for q in quadros:
        if q[16][:4] == pamq:
            if not multiquadro:
                multiquadro.append(q)
            else:
                break
        elif multiquadro:
            multiquadro.append(q)

    return multiquadro


def menu_quadros(quadros):
    """
    Menu interativo para exibir quadros individuais ou todos.
    """
    while True:
        try:
            escolha = int(input(f'\nEscolha o quadro (0-{len(quadros)-1}), -1 para todos ou -2 para sair: '))

            if escolha == -2:
                break
            elif escolha == -1:
                for i, q in enumerate(quadros):
                    print(f'\nQuadro {i}:\n{q}')
            elif 0 <= escolha < len(quadros):
                print(f'\nQuadro {escolha}:\n{quadros[escolha]}')
            else:
                print('Quadro inexistente!')
        except ValueError:
            print('Entrada inválida!')


def mostrar_quadros_em_tabela(quadros):
    """
    Exibe os quadros em formato tabular (DataFrame).
    """
    for i, q in enumerate(quadros):
        print(f"\nQuadro {i}:")
        df = pd.DataFrame([q], columns=[f"TS{j}" for j in range(32)])
        print(df.to_string(index=False))

