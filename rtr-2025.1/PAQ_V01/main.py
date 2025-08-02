from pcm30_utils import (
    ler_dado_arquivo,
    detectar_quadros,
    extrair_multiquadro,
    menu_quadros,
    mostrar_quadros_em_tabela
)

def main():
    nome_arquivo = 'vetor.txt'
    paq = '10011011'
    pamq = '0000'

    print('\nBits alinhados:')

    dado = ler_dado_arquivo(nome_arquivo)
    quadros, paq_validos = detectar_quadros(dado, paq)

    if paq_validos:
        print(f'\n\nOs PAQs verdadeiros estão nas posições: {paq_validos}')
        print(f'Total de quadros válidos detectados: {len(quadros)}')

        print('\nInício dos quadros alinhados:')
        for i, pos in enumerate(paq_validos):
            print(f"Quadro {i:02d} começa no bit {pos}")

        while True:
            print("\nEscolha o que deseja visualizar:")
            print("1 - Todos os quadros alinhados (modo lista)")
            print("2 - Apenas quadros do multiquadro (com início pamq)")
            print("3 - Visualizar todos os quadros em formato tabular (pandas)")
            print("4 - Sair")

            escolha = input("Digite sua opção: ")

            if escolha == '1':
                menu_quadros(quadros)
            elif escolha == '2':
                multiquadro = extrair_multiquadro(pamq, quadros)
                if multiquadro:
                    menu_quadros(multiquadro)
                else:
                    print("Nenhum multiquadro encontrado com o pamq informado.")
            elif escolha == '4':
                print("Saindo.")
                break
            elif escolha == '3':
                mostrar_quadros_em_tabela(quadros)
            else:
                print("Opção inválida. Tente novamente.")
    else:
        print('\nNão há nenhum quadro válido no arquivo.')

if __name__ == '__main__':
    main()
