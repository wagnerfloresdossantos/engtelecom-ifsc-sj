package engtelecom.poo;

/**
 * Classe que representa o painel de elevador de cada andar de um edifício
 * Contém métodos para pressionar, resetar e verificar estado dos botões
 */
public class PainelAndar {
    private int andar;
    private boolean botaoSubir;
    private boolean botaoDescer;

    /**
     * Método Contrutor
     * @param andar recebe como parâmetro o andar em que está o painel
     */
    public PainelAndar(int andar) {
        this.andar = andar;
        this.botaoSubir = false;
        this.botaoDescer = false;
    }

    /**
     * Método para pressionar o botão subir
     */
    public void pressBotaoSubir() {
        this.botaoSubir = true;
    }

    /**
     * Metodo para pressionar o botão descer
     */
    public void pressBotaoDescer() {
        this.botaoDescer = true;
    }

    /**
     * Reseta o botão para subir.
     */
    public void resetBotaoSubir() {
        this.botaoSubir = false;
    }

    /**
     * Reseta o botão para descer.
     */
    public void resetBotaoDescer() {
        this.botaoDescer = false;
    }

    /**
     * Retorna o estado do botão para subir.
     * @return true se o botão de subir está pressionado, caso contrário false.
     */
    public boolean getBotaoSubir() {
        return botaoSubir;
    }

    /**
     * Retorna o estado do botão para descer.
     * @return true se o botão de descer está pressionado, caso contrário false.
     */
    public boolean getBotaoDescer() {
        return botaoDescer;
    }

    /**
     * Retorna o número do andar deste painel.
     * @return O número do andar.
     */
    public int getAndar() {
        return andar;
    }
}
