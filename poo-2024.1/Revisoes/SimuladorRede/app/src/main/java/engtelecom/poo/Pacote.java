package engtelecom.poo;

import java.util.Objects;

/**
 * Classe que representa um pacote de dados na rede.
 */
public class Pacote extends DadosRede {
    private String conteudo;

    /**
     * Construtor para inicializar os atributos do pacote.
     *
     * @param enderecoIpOrigem  Endereço IP de origem.
     * @param portaOrigem       Porta de origem.
     * @param enderecoIpDestino Endereço IP de destino.
     * @param portaDestino      Porta de destino.
     * @param macDestino        Endereço MAC de destino.
     * @param conteudo          Conteúdo do pacote.
     */
    public Pacote(String enderecoIpOrigem, String portaOrigem, String enderecoIpDestino, String portaDestino, String macDestino, String conteudo) {
        super(enderecoIpOrigem, portaOrigem, enderecoIpDestino, portaDestino, macDestino);
        this.conteudo = conteudo;
    }

    /**
     * Getters e setters para o atributo conteudo
     */

    public String getConteudo() {
        return conteudo;
    }

    public void setConteudo(String conteudo) {
        this.conteudo = conteudo;
    }

    /**
     * Compara este pacote com outro objeto para verificar a igualdade
     *
     * @param o Objeto a ser comparado
     * @return true se os objetos forem iguais, false caso contrário
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Pacote pacote = (Pacote) o;
        return Objects.equals(enderecoIpOrigem, pacote.enderecoIpOrigem) &&
                Objects.equals(portaOrigem, pacote.portaOrigem) &&
                Objects.equals(enderecoIpDestino, pacote.enderecoIpDestino) &&
                Objects.equals(portaDestino, pacote.portaDestino) &&
                Objects.equals(macDestino, pacote.macDestino) &&
                Objects.equals(conteudo, pacote.conteudo);
    }

    /**
     * @return O código hash para este pacote.
     */
    @Override
    public int hashCode() {
        return Objects.hash(enderecoIpOrigem, portaOrigem, enderecoIpDestino, portaDestino, macDestino, conteudo);
    }
}
