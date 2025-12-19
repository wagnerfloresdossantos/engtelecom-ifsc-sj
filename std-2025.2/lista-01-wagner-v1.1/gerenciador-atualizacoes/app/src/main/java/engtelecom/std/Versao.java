package engtelecom.std;
/**
 * Representa e compara versões "vX.Y".
 * Fornece método estático para comparar duas Strings diretamente.
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
        if (maj != o.maj) return maj - o.maj;
        return min - o.min;
    }
    public static int cmp(String a, String b) {
        return new Versao(a).compareTo(new Versao(b));
    }
}
