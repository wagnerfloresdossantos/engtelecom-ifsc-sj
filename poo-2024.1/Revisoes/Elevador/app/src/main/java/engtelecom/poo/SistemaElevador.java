package engtelecom.poo;

import java.util.ArrayList;

/**
 * Classe que representa o sistema de um elevador.
 * Integra todas as partes (Elevador, PainelInterno e PainelAndar).
 * Contém os métodos para processar os passos da simulação e exibir o status do sistema.
 */
public class SistemaElevador {
    private Elevador elevador;
    private PainelInterno painelInterno;
    private ArrayList<PainelAndar> paineisAndar;
    private int numAndares;

    /**
     * Construtor que inicializa o sistema com o número de andares especificado.
     * @param numAndares Número de andares do prédio.
     */
    public SistemaElevador(int numAndares) {
        this.numAndares = numAndares;
        elevador = new Elevador(numAndares);
        painelInterno = new PainelInterno(numAndares);
        paineisAndar = new ArrayList<>(numAndares);
        for (int i = 0; i < numAndares; i++) {
            paineisAndar.add(new PainelAndar(i));
        }
    }

    /**
     * Método para chamar o elevador a partir de um andar específico e direção desejada.
     * @param andar Andar de onde o elevador é chamado.
     * @param direcao Direção desejada (subir ou descer).
     */
    public void chamarElevador(int andar, String direcao) throws InterruptedException {
        if (direcao.equals("subir")) {
            paineisAndar.get(andar).pressBotaoSubir();
        } else if (direcao.equals("descer")) {
            paineisAndar.get(andar).pressBotaoDescer();
        } else {
            System.out.println("Direção inválida. Por favor, escolha 'subir' ou 'descer'.");
            return;
        }
        elevador.requisitarAndar(andar);
        displayStatus();
        espera();
    }

    /**
     * Método para selecionar um andar de dentro do elevador.
     * @param andar Andar selecionado.
     */
    public void selecionaAndar(int andar) throws InterruptedException {
        painelInterno.pressBotao(andar);
        elevador.requisitarAndar(andar);
        displayStatus();
        espera();
    }

    /**
     * Método que faz o elevador esperar enquanto se move entre os andares.
     * @throws InterruptedException Se a thread for interrompida enquanto dorme.
     */
    private void espera() throws InterruptedException {
        elevador.mover();
        int andarAtual = elevador.getAndarAtual();

        // Reseta os botões de chamada do andar atual
        if (paineisAndar.get(andarAtual).getBotaoSubir()) {
            paineisAndar.get(andarAtual).resetBotaoSubir();
        }
        if (paineisAndar.get(andarAtual).getBotaoDescer()) {
            paineisAndar.get(andarAtual).resetBotaoDescer();
        }

        painelInterno.resetBotao(andarAtual);
        Thread.sleep(1000);
    }

    /**
     * Método para exibir o status atual do elevador e dos andares.
     */
    private void displayStatus() {
        // Exibe o status atual do elevador e dos botões internos
        System.out.println("Elevador | Andar atual: " + elevador.getAndarAtual() + " | Direção: " + elevador.getDirecao());
        System.out.println("Botões: ");

        // Exibe o status dos botões internos do elevador
        for (int i = 0; i < painelInterno.getBotoes().size(); i++) {
            System.out.print(i + " (" + (painelInterno.getBotoes().get(i) ? "1" : "0") + ") ");
        }
        System.out.println();

        // Exibe o status dos botões de subir e descer em cada andar
        for (PainelAndar painelAndar : paineisAndar) {
            System.out.println(painelAndar.getAndar() + "o Andar: Elevador: " + elevador.getDirecao() + " | Andar: " + elevador.getAndarAtual() +
                    " | Botões: subir (" + (painelAndar.getBotaoSubir() ? "1" : "0") +
                    ") descer (" + (painelAndar.getBotaoDescer() ? "1" : "0") + ")");
        }
    }

    /**
     * Retorna o número de andares do sistema de elevador.
     * @return Número de andares.
     */
    public int getNumAndares() {
        return numAndares;
    }

}
