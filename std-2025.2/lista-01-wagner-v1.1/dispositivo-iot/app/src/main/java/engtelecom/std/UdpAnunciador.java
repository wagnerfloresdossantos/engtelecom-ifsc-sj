package engtelecom.std;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
/**
 * Thread que, a cada 10s, envia por UDP multicast a versão do dispositivo.
 * Formato da mensagem: "IOT;vX.Y;<timestampMillis>"
 */
public class UdpAnunciador extends Thread {
    private final String mcastAddr;
    private final int mcastPort;
    private final DispositivoEstado estado;

    public UdpAnunciador(String addr, int port, DispositivoEstado estado) {
        this.mcastAddr = addr;
        this.mcastPort = port;
        this.estado = estado;
    }

    @Override public void run() {
        try (DatagramSocket ds = new DatagramSocket()) {
            InetAddress group = InetAddress.getByName(mcastAddr);
            while (true) {
                String payload = "IOT;" + estado.getVersao() + ";" + System.currentTimeMillis();
                byte[] buf = payload.getBytes(StandardCharsets.UTF_8);
                DatagramPacket pkt = new DatagramPacket(buf, buf.length, group, mcastPort);
                ds.send(pkt);
                //System.out.println("[IoT] multicast -> " + payload);
                Thread.sleep(10_000);
            }
        } catch (Exception e) {
            System.err.println("[IoT] erro UDP: " + e.getMessage());
        }
    }
}
