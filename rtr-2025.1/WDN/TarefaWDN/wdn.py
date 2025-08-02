from itertools import permutations  # Importa função para gerar permutações de elementos

# Grade padrão DWDM (ITU-T G.692) com espaçamento de 100 GHz
# Cria um dicionário onde a chave é o número do canal e o valor é a frequência em THz
base_canal = 191.7  # Frequência do canal 17
canais_itu = {canal: round(base_canal + 0.1 * (canal - 17), 1) for canal in range(17, 62)}

def listar_canais_itu():
    """Exibe a lista de canais disponíveis da grade ITU-T G.692."""
    print("\n--- Canais ITU-T G.692 ---")
    for canal, freq in canais_itu.items():
        print(f" Canal {canal}: {freq} THz")
    print("-" * 40)

def escolher_e_analisar():
    """Permite ao usuário escolher canais e realiza a análise de FWM."""
    
    # Recebe os números dos canais digitados pelo usuário
    entrada = input("Digite os números dos canais desejados (ex: 20 21 23): ")
    
    try:
        # Converte os números digitados para inteiros
        canais = list(map(int, entrada.strip().split()))
        
        # Verifica se todos os canais estão dentro da grade válida
        for c in canais:
            if c not in canais_itu:
                raise ValueError(f"Canal {c} não está na grade ITU-T G.692.")
        
        # Verifica se há ao menos 3 canais (mínimo para gerar FWM)
        if len(canais) < 3:
            print("Erro: é necessário escolher pelo menos 3 canais.\n")
            return

        # Converte os canais em frequências correspondentes (em THz)
        frequencias = [canais_itu[c] for c in canais]
        frequencias_set = set(frequencias)  # Conjunto para busca rápida

        interferencias = set()  # Guarda os casos de interferência detectados

        # Gera todas as permutações possíveis de 3 frequências diferentes
        for fi, fj, fk in permutations(frequencias, 3):
            ff = round(fi + fj - fk, 1)  # Calcula frequência gerada e arredonda

            # Verifica se a frequência gerada ff está entre as frequências de entrada
            if ff in frequencias_set:
                interferencias.add((fi, fj, fk, ff))  # Adiciona a interferência

        # Exibe o resultado da análise
        print("\n--- ANÁLISE FWM ---")
        if interferencias:
            print(f"Detectadas {len(interferencias)} sobreposições por Four Wave Mixing:\n")
            for fi, fj, fk, ff in sorted(interferencias):
                print(f"ff = {fi} + {fj} - {fk} = {ff} THz (interferente!)")
        else:
            print("Nenhuma interferência FWM detectada.")
        print("-" * 40)

    except Exception as e:
        # Captura e exibe erros de entrada inválida
        print(f"Erro: {e}")

def menu():
    """Exibe o menu principal e gerencia as opções do usuário."""
    while True:
        print("\n=== MENU FWM - ITU G.692 ===")
        print("1. Listar canais ITU disponíveis")
        print("2. Escolher canais e analisar Four Wave Mixing")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_canais_itu()  # Mostra canais disponíveis
        elif opcao == '2':
            escolher_e_analisar()  # Escolhe e analisa canais
        elif opcao == '3':
            print("Encerrando o programa.")
            break  # Sai do laço e encerra
        else:
            print("Opção inválida. Tente novamente.")

# Inicia o programa com o menu interativo
menu()
