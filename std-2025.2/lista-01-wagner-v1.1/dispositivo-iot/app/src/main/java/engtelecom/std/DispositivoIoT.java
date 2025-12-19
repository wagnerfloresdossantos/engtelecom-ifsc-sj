package engtelecom.std;
/**
 * Ponto de entrada do Dispositivo IoT.
 * - Cria o estado (versão atual)
 * - Inicia a thread de anúncios UDP multicast
 * - Inicia a thread do servidor TCP (porta 1234) para receber nova versão
 * - Mantém o processo vivo
 */
public class DispositivoIoT {
    public static final int TCP_PORT = 1234;
    public static final String MCAST_ADDR = "231.0.0.1";
    public static final int MCAST_PORT = 1290;

    public static void main(String[] args) throws Exception {
        // Versão inicial recebida como argumento (padrão v1.0)
        String versaoInicial = (args != null && args.length > 0) ? args[0] : "v1.0";
        DispositivoEstado estado = new DispositivoEstado(versaoInicial);
        // Threads de anúncio UDP e servidor TCP
        Thread tUdp = new UdpAnunciador(MCAST_ADDR, MCAST_PORT, estado);
        Thread tTcp = new TcpServidor(TCP_PORT, estado);
        tUdp.setDaemon(true);
        tTcp.setDaemon(true);

        tUdp.start();
        tTcp.start();

        System.out.println("[IoT] versão inicial " + versaoInicial);
        System.out.println("[IoT] Servidor TCP ouvindo na porta " + TCP_PORT);
        System.out.println("[IoT] Enviando anúncios multicast para " + MCAST_ADDR + ":" + MCAST_PORT);

        // mantém o processo vivo (estilo simples, como nos exemplos)
        Thread.currentThread().join();
    }
}
