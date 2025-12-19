package engtelecom.std;

import java.util.*;
/**
 * Armazena os dispositivos vistos: IP -> versão atual.
 * Fornece snapshot para iteração segura fora do lock.
 */
public class TabelaDispositivos {
    private final Map<String, String> mapa = Collections.synchronizedMap(new HashMap<>());

    public void atualizar(String ip, String versao) {
        mapa.put(ip, versao);
    }
    public Map<String, String> snapshot() {
        synchronized (mapa) { return new LinkedHashMap<>(mapa); }
    }
    public void remover(String ip) {
        mapa.remove(ip);
    }
    public String getVersao(String ip) {
        return mapa.get(ip);
    }
    public boolean isEmpty() { return mapa.isEmpty(); }
}
