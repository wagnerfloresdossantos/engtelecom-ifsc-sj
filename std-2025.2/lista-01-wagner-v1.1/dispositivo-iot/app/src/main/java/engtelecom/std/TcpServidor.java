package engtelecom.std;

import java.net.ServerSocket;
import java.net.Socket;
/**
 * Servidor TCP (:1234) que aceita conexões do Gerenciador.
 * Para cada conexão, cria uma thread TcpAtendedor.
 */
public class TcpServidor extends Thread {
    private final int port;
    private final DispositivoEstado estado;

    public TcpServidor(int port, DispositivoEstado estado) {
        this.port = port;
        this.estado = estado;
    }

    @Override public void run() {
        try (ServerSocket srv = new ServerSocket(port)) {
            while (true) {
                Socket cli = srv.accept();
                new TcpAtendedor(cli, estado).start(); // estilo "Thread por conexão"
            }
        } catch (Exception e) {
            System.err.println("[IoT] erro TCP: " + e.getMessage());
        }
    }
}
