package engtelecom.poo;

import java.util.Scanner;

/**
 * Classe App, responsável pela interação com o usuário e execução da simulação
 */
public class App {

    private SistemaElevador sistema;

    /**
     * Método contrutor da classe App
     * @param numAndares numero de andares do edifício
     */
    public App(int numAndares) {
        sistema = new SistemaElevador(numAndares);
    }

    /**
     * Exibe o menu de opções para o usuário
     * @return a opção escolhida pelo usuário
     */
    public int menu() {
        Scanner entrada = new Scanner(System.in);

        System.out.println();
        System.out.printf("..::ESCOLHA A OPÇÃO::..\n" +
                "1 - Chamar Elevador\n" +
                "2 - Selecionar andar de dentro do elevador\n" +
                "3 - Sair do Programa\n" +
                "> ");

        return entrada.nextInt();
    }

    /**
     * Método para chamar o elevador a partir do andar
     * @throws InterruptedException se a thread for interrompida enquanto dorme
     */
    public void chamarElevador() throws InterruptedException {
        Scanner entrada = new Scanner(System.in);
        System.out.println("Digite o andar que você está: ");
        int andar = entrada.nextInt();
        if (andar < 0 || andar >= sistema.getNumAndares()) {
            System.out.println("Andar inválido. Por favor, escolha um andar entre 0 e " + (sistema.getNumAndares() - 1));
            return;
        }
        System.out.println("Você deseja subir ou descer? (Digite 'subir' ou 'descer')");
        String direcao = entrada.next();
        sistema.chamarElevador(andar, direcao);
    }

    /**
     * Método para selecionar o andar de dentro do elevador
     * @throws InterruptedException se a thread for interrompida enquanto dorme
     */
    public void selecionarAndar() throws InterruptedException {
        Scanner entrada = new Scanner(System.in);
        System.out.println("Digite o andar de destino: ");
        int andar = entrada.nextInt();
        if (andar < 0 || andar >= sistema.getNumAndares()) {
            System.out.println("Andar inválido. Por favor, escolha um andar entre 0 e " + (sistema.getNumAndares() - 1));
            return;
        }
        sistema.selecionaAndar(andar);
    }

    /**
     * Método principal que inicializa o sistema e permite a interação com o usuário
     * @param args argumento de linha de comando (Não foi utilizado)
     * @throws InterruptedException se a thread for interrompida enquanto dorme
     *
     */
    public static void main(String[] args) throws InterruptedException {
        Scanner entrada = new Scanner(System.in);
        System.out.println("Digite o número de andares do prédio: ");
        int numAndares = entrada.nextInt();
        App app = new App(numAndares);
        int opcao;

        do {
            opcao = app.menu();
            switch (opcao) {
                case 1 -> app.chamarElevador();
                case 2 -> app.selecionarAndar();
            }
        } while (opcao != 3);
    }
}
