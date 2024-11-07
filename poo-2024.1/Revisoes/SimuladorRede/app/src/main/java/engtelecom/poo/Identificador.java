package engtelecom.poo;
/**
 * Classe Abstrata que representa um Identificador de dispositivo.
 * Esta classe serve como base para dispositivos de rede como roteadores, comutadores e firewalls.
 *
 * Contém atributos comuns a todos os dispositivos de rede, como endereço MAC e endereço IP.
 */
public class Identificador {

    private String macAddress;
    private String ipAddress;

    /**
     * Construtor que inicializa os atributos do dispositivo.
     *
     * @param macAddress Endereço MAC.
     * @param ipAddress  Endereço IP.
     */
    public Identificador(String macAddress, String ipAddress) {
        this.macAddress = macAddress;
        this.ipAddress = ipAddress;
    }

    /**
     * Getter para atributos
     */
    public String getMacAddress() {
        return macAddress;
    }

    public String getIpAddress() {
        return ipAddress;
    }
}
