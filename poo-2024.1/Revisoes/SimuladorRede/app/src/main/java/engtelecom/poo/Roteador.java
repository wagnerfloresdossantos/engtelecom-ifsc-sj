package engtelecom.poo;

import java.util.HashMap;
/**
 * Classe que representa um roteador de rede.
 */
public class Roteador extends Identificador implements DispositivoRede{

    private HashMap<String, String> tabelaRotas;
    private String portaInternet;
    /**
     * Construtor que inicializa os atributos do roteador e a tabela de rotas.
     *
     * @param macAddress   Endereço MAC do roteador.
     * @param ipAddress    Endereço IP do roteador.
     * @param tabelaRotas  Tabela de rotas (rede -> porta).
     * @param portaInternet Porta padrão para saída na internet.
     */
    public Roteador(String macAddress, String ipAddress, HashMap<String, String> tabelaRotas, String portaInternet) {
        super(macAddress, ipAddress);
        this.tabelaRotas = tabelaRotas;
        this.portaInternet = portaInternet;
    }

    /**
     * Processa um pacote e encaminha-o para a porta correspondente com base na tabela de rotas.
     *
     * @param pacote O pacote a ser processado.
     */
    @Override
    public void processarPacote(Pacote pacote) {
        String ipDestino = pacote.getEnderecoIpDestino();
        String rede = ipDestino.substring(0, 1) + "xxx"; // Assumindo que a rede é definida pelo primeiro dígito do IP

        if (tabelaRotas.containsKey(rede)) {
            System.out.println("Roteador: Pacote encaminhado para a rede: " + rede + " na porta: " + tabelaRotas.get(rede));
        } else {
            System.out.println("Roteador: Rede desconhecida. Pacote encaminhado para a porta de saída padrão: " + portaInternet);
        }

    }

    /**
     * Adiciona uma rota à tabela de rotas.
     *
     * @param rede O prefixo da rede
     * @param porta A porta associada ao prefixo
     */
    public void addRota(String rede, String porta) {
       tabelaRotas.put(rede, porta);
    }

    /**
     * Getter para acessar atributo
     *
     * @return A tabela hash com Tabela de rotas
     */
    public HashMap<String, String> getTabelaRotas() {
        return tabelaRotas;
    }
}
