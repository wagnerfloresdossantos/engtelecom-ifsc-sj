package engtelecom.poo;

import java.util.ArrayList;

/**
 * Classe que representa o painel interno de um elevador
 * Contém métodos para pressionar, obter e resetar os botões
 */
public class PainelInterno {

    /**
     * Lista de botões boolean
     */
    private ArrayList<Boolean> botoes;

    /**
     * Método Construtor
     * @param numAndares recebe como parâmetro o numero de andares do edifício
     */
    public PainelInterno(int numAndares) {
        botoes = new ArrayList<>(numAndares);
        for (int i = 0; i < numAndares; i++) {
            botoes.add(false);
        }
    }

    /**
     * Método que pressiona o botão
     * @param andar recebe como parâmetro o andar/botãoo que deve ser pressionado
     */
    public void pressBotao(int andar) {
        botoes.set(andar, true);
    }
    /**
     * Método que reseta o botão
     * @param andar recebe como parâmetro o andar/botãoo que deve ser pressionado
     */
    public void resetBotao(int andar) {
        botoes.set(andar, false);
    }

    /**
     * Método Get para o argumento botoes
     * @return botoes
     */
    public ArrayList<Boolean> getBotoes() {
        return botoes;
    }
}
