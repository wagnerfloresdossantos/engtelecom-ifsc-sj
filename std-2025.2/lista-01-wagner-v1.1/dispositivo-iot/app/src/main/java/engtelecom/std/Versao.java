package engtelecom.std;
/**
 * Representa uma versão no formato vX.Y e permite comparação.
 * Usado se precisar comparar versões localmente no IoT (opcional).
 */
public class Versao implements Comparable<Versao> {
    private final int maj, min;

    public Versao(String s) {
        String x = s.startsWith("v") ? s.substring(1) : s;
        String[] p = x.split("\\.");
        this.maj = Integer.parseInt(p[0]);
        this.min = (p.length > 1) ? Integer.parseInt(p[1]) : 0;
    }
    @Override public int compareTo(Versao o) {
        if (this.maj != o.maj) return this.maj - o.maj;
        return this.min - o.min;
    }
    @Override public String toString() { return "v" + maj + "." + min; }
}

