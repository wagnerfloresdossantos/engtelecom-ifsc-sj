package engtelecom.std;

import java.util.Locale;
import java.util.Map;
import java.util.Scanner;
/**
 * Interface de Linha de Comando (CLI) do Gerenciador.
 * Comandos: lista | inc | aplicar | sair
 */
public class Cli {
    private final TabelaDispositivos tabela;
    private final AtualizadorTcp atualizador;

    public Cli(TabelaDispositivos tabela, AtualizadorTcp atualizador) {
        this.tabela = tabela;
        this.atualizador = atualizador;
    }

    public void run() {
        try (Scanner sc = new Scanner(System.in)) {
            System.out.println("""
                Comandos:
                  lista     -> listar dispositivos e versões
                  inc       -> incrementar versão-alvo (v1.0 -> v1.1 -> v1.2 ...)
                  aplicar   -> atualizar desatualizados por TCP :1234
                  sair
                """);
            while (true) {
                System.out.print(">\n");
                String cmd = sc.nextLine().trim().toLowerCase(Locale.ROOT);
                switch (cmd) {
                    case "lista" -> {
                        System.out.println("Versão-alvo: " + atualizador.getVersaoAlvo());
                        Map<String,String> snap = tabela.snapshot();
                        if (snap.isEmpty()) System.out.println("(vazio)");
                        for (Map.Entry<String,String> e : snap.entrySet()) {
                            System.out.printf("- %s -> versao=%s%n", e.getKey(), e.getValue());
                        }
                    }
                    case "inc"     -> atualizador.incrementarVersao();
                    case "aplicar" -> atualizador.aplicar();
                    case "sair"    -> { return; }
                    default        -> System.out.println("Comando inválido.");
                }
            }
        } catch (Exception e) {
            System.err.println("[GER] erro CLI: " + e.getMessage());
        }
    }
}
