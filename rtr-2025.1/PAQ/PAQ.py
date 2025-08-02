def encontraPaq(dado, paq):
    timeSlot = []

    A = 256
    fim = 512
    
    if dado[A : A+1] == '1' and dado[fim : fim + 8] == paq:
        print(dado[0:fim], end='')
        timeSlot = [dado[j : j+8] for j in range(0, fim, 8)]    # Adiciona na lista 'timeSlot', de 8 em 8 bits

    return timeSlot

def mostraQuadros(quadro):
    
    while True:
        try:
            escolha = int(input(f'\nEscolha o quadro (0-{len(quadro)-1}) ou -1 para mostrar todos os quadros ou pressione -2 para sair: '))
            
            if escolha == -2:
                break
            elif escolha == -1:
                for i in range(0, len(quadro)):
                    print(f'\nQuadro {i}: \n{quadro[i]}')
            elif escolha in range(len(quadro)):
                print(f'\n{quadro[escolha]}')
            else:
                print('\nQuadro inexistente!')
        except:
            print('\nEntrada inválida!')

def encontraPamq(pamq, quadro):
    multiQuadro = []

    for q in quadro:            # Cria um iterador para os quadros
        if q[16][:4] == pamq:   # Verifica se o time slot 16 possui o PAMQ
            if not multiQuadro: # Se ainda não houver um multiquadro sendo formado, o inicia
                multiQuadro.append(q)
            else:
                break    
        elif multiQuadro:
            multiQuadro.append(q)

    return multiQuadro


with open('RX(vetor)MQ_v2.txt') as arq:
    dado = arq.read()
    dado = dado.replace(' ', '')
    inic = 0

    quadro = []
    paq = '10011011'
    paqVerd = []
    pamq = '0000'
    
    print('\nBits alinhados:')

    while True:
        inic = dado.find(paq, inic)

        if inic == -1:
            break
        else:
            timeSlot = encontraPaq(dado[inic:], paq)
            
            if timeSlot:
                paqVerd.append(inic)
                quadro[len(quadro) : len(quadro) + 2] = [timeSlot[:32], timeSlot[32:]] # Aloca nas duas últimas posições da lista 'quadro', as 32 primeiras e últimas sequencias de bits, respectivamente

            inic += 1
    
    print(f'\n\nOs PAQs verdadeiros estão nas posições: {paqVerd}')

    if quadro:
        quadro = encontraPamq(pamq, quadro)
        mostraQuadros(quadro)
    else:
        print('Não há nenhum quadro dentro do arquivo!')