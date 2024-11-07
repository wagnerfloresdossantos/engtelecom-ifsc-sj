package engtelecom.poo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

/**
 * Classe principal para simulação de rede.
 */
public class App {

    private Comutador comutador;
    private Roteador roteador;
    private Firewall firewall;



    /**
     * Configura a topologia de rede conforme a especificação.
     */
    public App() {
        this.comutador = new Comutador("A1", "1001", new HashMap<>());  // HashMap para MAC -> Porta
        this.roteador = new Roteador("B2", "2001", new HashMap<>(), "eth0");  // HashMap para tabela de rotas
        this.firewall = new Firewall("C3", "3001", new ArrayList<>());  // ArrayList para regras de filtragem

        // Configuração Comutador
        comutador.inserirTabelaMac("A2",1);
        comutador.inserirTabelaMac("A3",2);
        comutador.inserirTabelaMac("A4",3);
        comutador.inserirTabelaMac("A5",4);

        // Configuração da rede
        roteador.addRota("1xxx", "eth1"); // Rota para a rede 1xxx
        roteador.addRota("2xxx", "eth2"); // Rota para a rede 2xxx

        // Adicionando regras ao firewall
        firewall.addRegra(new RegrasFiltragem("1001", "8080", "2002", "80", "A2", Acao.ENCAMINHAR));
        firewall.addRegra(new RegrasFiltragem("2001", "22", "3001", "443", "B3",  Acao.DESCARTAR));
    }

    /**
     * Exibe o menu e captura a opção escolhida pelo usuário.
     * @return A opção escolhida.
     */
    public int menu() {
        Scanner entrada = new Scanner(System.in);

        System.out.println();
        System.out.printf("..::ESCOLHA A OPÇÃO::..\n" +
                "1. Listar dispositivos por tipo\n" +
                "2. Listar dispositivos por rede\n" +
                "3. Listar rotas\n" +
                "4. Listar regras de filtragem\n" +
                "5. Criar regra de filtragem\n" +
                "6. Apagar regra de filtragem\n" +
                "7. Simular processamento de pacote\n" +
                "8. Sair do Programa\n" +
                "> ");

        return entrada.nextInt();
    }

    /**
     * Lista os dispositivos da rede agrupados por tipo.
     */
    public void listarDispositivoisPorTipo() {
        System.out.println("Dispositivos por tipo:");
        System.out.println("Comutador: MAC = " + comutador.getMacAddress() + ", IP = " + comutador.getIpAddress());
        System.out.println("Roteador: MAC = " + roteador.getMacAddress() + ", IP = " + roteador.getIpAddress());
        System.out.println("Firewall: MAC = " + firewall.getMacAddress() + ", IP = " + firewall.getIpAddress());
    }

    /**
     * Lista os dispositivos da rede agrupados por rede.
     */
    public void listarDispositivosPorRede() {
        System.out.println("Dispositivos por rede:");
        System.out.println("Comutador IP: " + comutador.getIpAddress() + " (MAC = " + comutador.getMacAddress() + ")");
        System.out.println("Roteador IP: " + roteador.getIpAddress() + " (MAC = " + roteador.getMacAddress() + ")");
        System.out.println("Firewall IP: " + firewall.getIpAddress() + " (MAC = " + firewall.getMacAddress() + ")");
    }

    /**
     * Exibe a tabela de rotas do roteador.
     */
    public void listarRotas() {
        System.out.println("Rotas do roteador:");
        roteador.getTabelaRotas().forEach((rede, porta) ->
                System.out.println("Rede: " + rede + " -> Porta: " + porta));
    }

    /**
     * Exibe a lista de regras de filtragem do firewall.
     */
    public void listarRegrasDeFiltragem() {
        System.out.println("Regras de filtragem do firewall:");
        for (int i = 0; i < firewall.getRegras().size(); i++) {
            RegrasFiltragem regra = firewall.getRegras().get(i);
            System.out.println("Regra " + i + ": " + regra.getEnderecoIpOrigem() + ":" +
                    regra.getPortaOrigem() + " -> " + regra.getEnderecoIpDestino() + ":" +
                    regra.getPortaDestino() + "MAC destino: " + regra.getMacDestino()+ " Ação: " + regra.getAcao());
        }
    }

    /**
     * Permite criar uma nova regra de filtragem no firewall.
     */
    public void criarRegraDeFiltragem() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Criar nova regra de filtragem:");
        System.out.print("Digite o endereço IP de origem da regra: ");
        String ipOrigem = scanner.nextLine();
        System.out.print("Digite a porta IP de origem da regra: ");
        String portaOrigem = scanner.nextLine();
        System.out.print("Digite o endereço IP de destino da regra: ");
        String ipDestino = scanner.nextLine();
        System.out.print("Digite a porta IP de destino da regra: ");
        String portaDestino = scanner.nextLine();
        System.out.print("Digite o endereço MAC de destino da regra: ");
        String macDestino = scanner.nextLine();
        System.out.print("Digite o conteúdo da regra: ");
        String conteudo = scanner.nextLine();
        System.out.print("Escolha a ação (1 - ENCAMINHAR, 2 - DESCARTAR): ");
        int acaoInt = scanner.nextInt();
        Acao acao = (acaoInt == 1) ? Acao.ENCAMINHAR : Acao.DESCARTAR;

        RegrasFiltragem novaRegra = new RegrasFiltragem(ipOrigem, portaOrigem, ipDestino, portaDestino, macDestino, acao);
        firewall.addRegra(novaRegra);
        System.out.println("Regra adicionada com sucesso.");
    }

    /**
     * Permite apagar uma regra de filtragem do firewall.
     */
    public void apagarRegraDeFiltragem() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Apagar regra de filtragem:");
        System.out.print("Digite o número da regra a ser removida: ");
        int indice = scanner.nextInt();
        if (indice >= 0 && indice < firewall.getRegras().size()) {
            firewall.getRegras().remove(indice);
            System.out.println("Regra removida com sucesso.");
        } else {
            System.out.println("Índice de regra inválido.");
        }
    }

    /**
     * Simula o processamento de um pacote pela rede.
     */
    public void simularProcessamentoPacote() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Simular processamento de pacote:");
        System.out.print("Digite o endereço IP de origem: ");
        String ipOrigem = scanner.nextLine();
        System.out.print("Digite a porta IP de origem: ");
        String portaOrigem = scanner.nextLine();
        System.out.print("Digite o endereço IP de destino: ");
        String ipDestino = scanner.nextLine();
        System.out.print("Digite a porta IP de destino: ");
        String portaDestino = scanner.nextLine();
        System.out.print("Digite o endereço MAC de destino: ");
        String macDestino = scanner.nextLine();
        System.out.print("Digite o conteúdo do pacote: ");
        String conteudo = scanner.nextLine();

        Pacote novoPacote = new Pacote(ipOrigem, portaOrigem, ipDestino, portaDestino, macDestino, conteudo);
        comutador.processarPacote(novoPacote);
        roteador.processarPacote(novoPacote);
        firewall.processarPacote(novoPacote);
    }

    /**
     * Método principal que executa a aplicação.
     * @param args Argumentos da linha de comando.
     */
    public static void main(String[] args) {
        App app = new App();

        int opcao;

        do {
            opcao = app.menu();
            switch (opcao) {
                case 1 -> app.listarDispositivoisPorTipo();
                case 2 -> app.listarDispositivosPorRede();
                case 3 -> app.listarRotas();
                case 4 -> app.listarRegrasDeFiltragem();
                case 5 -> app.criarRegraDeFiltragem();
                case 6 -> app.apagarRegraDeFiltragem();
                case 7 -> app.simularProcessamentoPacote();
                case 8 -> System.out.println("Encerrando o programa.");
                default -> System.out.println("Opção inválida. Tente novamente.");
            }
        } while (opcao != 8);
    }
}
