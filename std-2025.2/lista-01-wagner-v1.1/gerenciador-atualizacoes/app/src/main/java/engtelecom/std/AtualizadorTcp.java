package engtelecom.std;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
/**
 * Aplica a versão-alvo nos dispositivos desatualizados via TCP :1234.
 * - Incrementa a versão alvo (inc)
 * - Conecta com timeout
 * - Remove da tabela quem não responder/conectar
 */
public class AtualizadorTcp {
    private final int tcpPort;
    private final TabelaDispositivos tabela;
    private String versaoAlvo = "v1.0";

    public AtualizadorTcp(int port, TabelaDispositivos tabela) {
        this.tcpPort = port;
        this.tabela = tabela;
    }

    public String getVersaoAlvo() { return versaoAlvo; }

    public void incrementarVersao() {
        try {
            String s = versaoAlvo.startsWith("v") ? versaoAlvo.substring(1) : versaoAlvo;
            String[] p = s.split("\\.");
            int maj = Integer.parseInt(p[0]);
            int min = (p.length > 1 ? Integer.parseInt(p[1]) : 0) + 1;
            versaoAlvo = "v" + maj + "." + min;
            System.out.println("Nova versão-alvo: " + versaoAlvo);
        } catch (Exception e) {
            versaoAlvo = "v1.0";
            System.out.println("Reset para v1.0");
        }
    }

    public void aplicar() {
        Map<String,String> snap = tabela.snapshot();
        List<String> remover = new ArrayList<>();

        for (Map.Entry<String,String> e : snap.entrySet()) {
            String ip   = e.getKey();
            String vers = e.getValue();

            // só atualiza desatualizados
            if (vers != null && Versao.cmp(vers, versaoAlvo) >= 0) {
                continue;
            }

            try (Socket s = new Socket()) {
                s.connect(new InetSocketAddress(ip, tcpPort), 2000);

                PrintWriter out = new PrintWriter(
                        new OutputStreamWriter(s.getOutputStream(), StandardCharsets.UTF_8), true);
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));

                out.println(versaoAlvo);
                String resp = in.readLine();
                System.out.printf("[GER] %s <= %s (resp: %s)%n", ip, versaoAlvo, resp);

            } catch (Exception ex) {
                System.err.printf("[GER] ERRO conectando %s: %s (removendo)%n", ip, ex.getMessage());
                remover.add(ip);
            }
        }
        for (String ip : remover) tabela.remover(ip);
    }
}
