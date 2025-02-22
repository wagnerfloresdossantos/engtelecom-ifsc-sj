package engtelecom.poo;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Classe que representa um firewall de rede.
 */
public class Firewall extends Identificador implements DispositivoRede{

    private ArrayList<RegrasFiltragem> regras;

    /**
     * Construtor que inicializa os atributos do firewall e a lista de regras de filtragem.
     *
     * @param macAddress Endereço MAC do firewall.
     * @param ipAddress  Endereço IP do firewall.
     * @param regras     Regras de filtragem configuradas.
     */
    public Firewall(String macAddress, String ipAddress, ArrayList<RegrasFiltragem> regras) {
        super(macAddress, ipAddress);
        this.regras = regras;
    }

    /**
     * Processa um pacote de acordo com as regras de filtragem configuradas.
     *
     * @param pacote O pacote a ser processado.
     */
    @Override
    public void processarPacote(Pacote pacote) {
        for (int i = 0; i < regras.size(); i++) {
            RegrasFiltragem regra = regras.get(i);
            if (regra.equals(pacote)) {
                if (regra.getAcao() == Acao.ENCAMINHAR) {
                    System.out.println("Firewall: Pacote encaminhado conforme a regra " + i + ": " + regra.getAcao());
                } else {
                    System.out.println("Firewall: Pacote descartado conforme a regra " + i + ": " + regra.getAcao());
                }
                return;
            }
        }
        System.out.println("Firewall: Nenhuma regra satisfeita. Pacote descartado.");
    }


    /**
     * Adiciona uma regra de filtragem.
     *
     * @param regra A regra de filtragem a ser adicionada.
     */
    public void addRegra(RegrasFiltragem regra) {
        regras.add(regra);
    }
    /**
     * Getter para acessar atributo
     *
     * @return A lista de regras de filtragem configuradas.
     */
    public ArrayList<RegrasFiltragem> getRegras() {
        return regras;
    }

}
