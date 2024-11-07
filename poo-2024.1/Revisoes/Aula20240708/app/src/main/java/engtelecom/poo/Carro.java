package engtelecom.poo;

/**
 * Representa um carro em um jogo de corrida
 *
 * @author Wagner Santos
 */
public class Carro {

    /**
     * Velocidade atual do carro
     */
    private int velocidadeAtual;

    private static final int VELOCIDADE_MAXIMA = 120;
    private static final int VELOCIDADE_MINIMA = 0;


    /**
     * Construtor
     */
    public Carro() {
        this.velocidadeAtual = 0;
    }

    /**
     * Incrementa a velocidade do carro de acordo com o parâmetro fornecido
     * @param i incremento da velocidade
     * @return nova velocidade do carro
     */
    public int acelerar(int i){
        if(i > 0) {
            if (velocidadeAtual + i > VELOCIDADE_MAXIMA) {
                this.velocidadeAtual = VELOCIDADE_MAXIMA;
            } else {
                this.velocidadeAtual += i;
            }
        }
        return this.velocidadeAtual;
    }

    /**
     * Decrementa a velocidade do carro de acordo com o parametro fornecido
     * @param i decrementa a velocidade do carro
     * @return nova velocidade do carro
     */
    public int frear(int i){
        if(i > 0) {
            if (velocidadeAtual - i < VELOCIDADE_MINIMA) {
                this.velocidadeAtual = VELOCIDADE_MINIMA;
            } else {
                this.velocidadeAtual -= i;
            }
        }
        return this.velocidadeAtual;
    }

    public int getVelocidadeAtual() {
        return velocidadeAtual;
    }

    @Override
    public String toString() {
        return "Carro{" +
                "velocidadeAtual=" + velocidadeAtual +
                '}';
    }
}
