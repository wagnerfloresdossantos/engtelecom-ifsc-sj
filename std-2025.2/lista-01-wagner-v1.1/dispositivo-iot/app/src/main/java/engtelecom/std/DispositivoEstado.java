package engtelecom.std;
/**
 * Guarda o estado do dispositivo (versão do software).
 * Métodos sincronizados para acesso seguro entre threads.
 */
public class DispositivoEstado {
    private String versao;

    public DispositivoEstado(String versao) {
        this.versao = versao;
    }
    public synchronized String getVersao() {
        return versao;
    }
    public synchronized void setVersao(String v) {
        this.versao = v;
    }
}
