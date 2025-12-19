package engtelecom.std;

import java.net.*;
import java.nio.charset.StandardCharsets;
/**
 * Thread que escuta o multicast 231.0.0.1:1290 e atualiza a tabela.
 * Imprime TODA mensagem recebida (a cada ~10s por IoT) para evidência.
 */
public class UdpOuvinteMulticast extends Thread {
    private final String mcastAddr;
    private final int mcastPort;
    private final TabelaDispositivos tabela;

    public UdpOuvinteMulticast(String addr, int port, TabelaDispositivos tabela) {
        this.mcastAddr = addr;
        this.mcastPort = port;
        this.tabela = tabela;
    }

    @SuppressWarnings("deprecation") // joinGroup(InetAddress) ainda usado nas aulas
    @Override
    public void run() {
        byte[] buf = new byte[1024];
        try (MulticastSocket ms = new MulticastSocket(mcastPort)) {
            InetAddress grupo = InetAddress.getByName(mcastAddr);
            ms.joinGroup(grupo); // API usada nos exemplos do professor
            System.out.println("[GER] ouvindo " + mcastAddr + ":" + mcastPort);

            while (true) {
                DatagramPacket p = new DatagramPacket(buf, buf.length);
                ms.receive(p);

                String msg = new String(p.getData(), p.getOffset(), p.getLength(), StandardCharsets.UTF_8);
                String[] t = msg.split(";", 3); // Formato: "IOT;vX.Y;timestamp"

                if (t.length >= 2 && "IOT".equals(t[0])) {
                    String ip   = p.getAddress().getHostAddress();
                    String vers = t[1];
                    String ts   = (t.length >= 3 ? t[2] : "-");

                    // Atualiza tabela e imprime sempre (mesmo se não mudou)
                    tabela.atualizar(ip, vers);
                    System.out.printf("[GER] visto %s versao %s (ts=%s)%n", ip, vers, ts);
                }
            }

        } catch (Exception e) {
            System.err.println("[GER] erro multicast: " + e.getMessage());
        }
    }
}
