package engtelecom.poo;

import java.util.ArrayList;

/**
 * Classe que representa o elevador
 * Gerencia o movimento e reuisições do elevador
 * Contém métodos para mover o elevador e atualizar o andar de destino
 */
public class Elevador {

    /**
     * andar atual do elevador
     * andar que se deseja ir
     * direção do elevador
     * andar que foi requisitado
     */
    private int andarAtual;
    private int andarDesejado;
    private String direcao;
    private ArrayList<Boolean> andarRequisitado;

    /**
     * Método Construtor
     * @param numAndares recebe como parâmetro o número de andares que terá o edifício
     */
    public Elevador(int numAndares) {
        this.andarAtual = 0;
        this.andarDesejado = 0;
        this.direcao = "parado";
        this.andarRequisitado = new ArrayList<>(numAndares);
        for (int i = 0; i < numAndares; i++) {
            andarRequisitado.add(false);
        }
    }

    /**
     * Método que requisita o andar
     * @param andar andar requisitado
     */
    public void requisitarAndar(int andar) {
        andarRequisitado.set(andar, true);
        atualizaAndarDesejado();
    }

    /**
     * Método que move o elevador
     */
    public void mover() {
        if (andarAtual < andarDesejado) {
            direcao = "subindo";
            andarAtual++;
        } else if (andarAtual > andarDesejado) {
            direcao = "descendo";
            andarAtual--;
        } else {
            direcao = "parado";
            andarRequisitado.set(andarAtual, false);
            atualizaAndarDesejado();
        }
    }

    /**
     * Método que atualiza o andar desejado e é usado no Método mover()
     */
    private void atualizaAndarDesejado() {
        for (int i = 0; i < andarRequisitado.size(); i++) {
            if (andarRequisitado.get(i)) {
                andarDesejado = i;
                return;
            }
        }
        andarDesejado = andarAtual;
    }

    /**
     * Métodp Get do atributo direção
     * @return direção
     */
    public String getDirecao() {
        return direcao;
    }

    /**
     * Método Get do atributo andar atual
     * @return andar atual
     */
    public int getAndarAtual() {
        return andarAtual;
    }
}
