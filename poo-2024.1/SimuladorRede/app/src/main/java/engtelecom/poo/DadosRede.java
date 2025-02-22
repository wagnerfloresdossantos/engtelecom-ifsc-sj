package engtelecom.poo;

/**
 * Classe abstrata que serve como base para Pacote e RegrasFiltragem.
 */
public abstract class DadosRede {
    protected String enderecoIpOrigem;
    protected String portaOrigem;
    protected String enderecoIpDestino;
    protected String portaDestino;
    protected String macDestino;

    /**
     * Construtor que inicializa os atributos comuns.
     *
     * @param enderecoIpOrigem  Endereço IP de origem.
     * @param portaOrigem       Porta de origem.
     * @param enderecoIpDestino Endereço IP de destino.
     * @param portaDestino      Porta de destino.
     * @param macDestino        Endereço MAC de destino.
     */
    public DadosRede(String enderecoIpOrigem, String portaOrigem, String enderecoIpDestino, String portaDestino, String macDestino) {
        this.enderecoIpOrigem = enderecoIpOrigem;
        this.portaOrigem = portaOrigem;
        this.enderecoIpDestino = enderecoIpDestino;
        this.portaDestino = portaDestino;
        this.macDestino = macDestino;
    }

    /**
     * Getters e setters para os atributos     *
     */
    public String getEnderecoIpOrigem() {
        return enderecoIpOrigem;
    }

    public void setEnderecoIpOrigem(String enderecoIpOrigem) {
        this.enderecoIpOrigem = enderecoIpOrigem;
    }

    public String getPortaOrigem() {
        return portaOrigem;
    }

    public void setPortaOrigem(String portaOrigem) {
        this.portaOrigem = portaOrigem;
    }

    public String getEnderecoIpDestino() {
        return enderecoIpDestino;
    }

    public void setEnderecoIpDestino(String enderecoIpDestino) {
        this.enderecoIpDestino = enderecoIpDestino;
    }

    public String getPortaDestino() {
        return portaDestino;
    }

    public void setPortaDestino(String portaDestino) {
        this.portaDestino = portaDestino;
    }

    public String getMacDestino() {
        return macDestino;
    }

    public void setMacDestino(String macDestino) {
        this.macDestino = macDestino;
    }
}
