package engtelecom.std;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
/**
 * Atende uma conexão TCP: lê uma linha com a nova versão e atualiza o estado.
 * Responde "OK Atualizado para vX.Y" ou "ERRO Versão inválida".
 */
public class TcpAtendedor extends Thread {
    private final Socket cli;
    private final DispositivoEstado estado;

    public TcpAtendedor(Socket cli, DispositivoEstado estado) {
        this.cli = cli;
        this.estado = estado;
    }

    @Override public void run() {
        try (Socket s = cli;
             BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
             PrintWriter out = new PrintWriter(new OutputStreamWriter(s.getOutputStream(), StandardCharsets.UTF_8), true)) {

            String novaVersao = in.readLine(); // ex: "v1.1"
            if (novaVersao != null && !novaVersao.isEmpty()) {
                estado.setVersao(novaVersao);
                out.println("OK Atualizado para " + novaVersao);
            } else {
                out.println("ERRO Versão inválida");
            }
        } catch (Exception e) {
            System.err.println("[IoT] erro atendendo TCP: " + e.getMessage());
        }
    }
}
