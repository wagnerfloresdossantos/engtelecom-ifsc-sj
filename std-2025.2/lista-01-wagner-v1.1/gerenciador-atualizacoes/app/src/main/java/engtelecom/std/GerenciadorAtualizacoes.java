package engtelecom.std;
/**
 * Ponto de entrada do Gerenciador:
 * - Inicia o ouvinte multicast (preenche a tabela IP->versão)
 * - Cria a CLI para interagir: lista | inc | aplicar | sair
 */
public class GerenciadorAtualizacoes {
    public static final String MCAST_ADDR = "231.0.0.1";
    public static final int MCAST_PORT = 1290;
    public static final int TCP_PORT = 1234;

    public static void main(String[] args) throws Exception {
        TabelaDispositivos tabela = new TabelaDispositivos();
        AtualizadorTcp atualizador = new AtualizadorTcp(TCP_PORT, tabela);
        Cli cli = new Cli(tabela, atualizador);

        Thread t = new UdpOuvinteMulticast(MCAST_ADDR, MCAST_PORT, tabela);
        t.setDaemon(true);
        t.start();

        cli.run(); // loop bloqueante
        System.out.println("Encerrado.");
    }
}
