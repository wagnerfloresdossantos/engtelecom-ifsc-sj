package engtelecom.poo;

import java.util.HashMap;

/**
 * Classe que representa um comutador (switch) de rede.
 */
public class Comutador extends Identificador implements DispositivoRede {

    private HashMap<String, Integer> tabelaMac;
    private static final int MAX_PORTAS = 12;  // Número máximo de portas

    /**
     * Construtor que inicializa os atributos do comutador e a tabela MAC.
     *
     * @param macAddress Endereço MAC do comutador.
     * @param ipAddress  Endereço IP do comutador.
     * @param tabelaMac  Tabela de endereços MAC e portas associadas.
     */
    public Comutador(String macAddress, String ipAddress, HashMap<String, Integer> tabelaMac) {
        super(macAddress, ipAddress);
        this.tabelaMac = new HashMap<>();
    }

    /**
     * Insere um endereço MAC e a porta associada na tabela MAC, se o número máximo de portas ainda não foi alcançado.
     *
     * @param macAddress Endereço MAC a ser inserido.
     * @param porta      Porta associada ao endereço MAC.
     */
    public boolean inserirTabelaMac(String macAddress, int porta) {
        if (tabelaMac.size() < MAX_PORTAS) {
            tabelaMac.put(macAddress, porta);
            return true;
        } else {
            return false;
        }
    }

    /**
     * Processa um pacote e encaminha-o para a porta Física do Comutador correspondente.
     *
     * @param pacote O pacote a ser processado.
     */
    @Override
    public void processarPacote(Pacote pacote) {
        String macDestino = pacote.getMacDestino();
        int portaOrigem = Integer.parseInt(pacote.getPortaOrigem());

        if (tabelaMac.containsKey(macDestino)) {
            // Se o endereço MAC de destino é conhecido, encaminha para a porta correspondente
            System.out.println("Comutador: Pacote encaminhado para a porta física: " + tabelaMac.get(macDestino));
        } else {
            // Se o endereço MAC de destino não é conhecido, encaminha para todas as portas exceto a porta de origem
            System.out.println("Comutador: Endereço MAC desconhecido. Pacote encaminhado para todas as portas, exceto a porta de origem");
            for (int porta : tabelaMac.values()) {
                if (porta != portaOrigem) {
                    System.out.println("Comutador: Pacote encaminhado para a porta física: " + porta);
                }
            }
        }
    }
}
