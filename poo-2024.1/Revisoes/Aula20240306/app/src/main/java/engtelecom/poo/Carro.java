package engtelecom.poo;

public class Carro {


    // Atributos
    private double velocidadeAtual;
    private final double VELOCIDADE_MAX;

    public Carro(double vMax) {
        this.velocidadeAtual = 0;
        this.VELOCIDADE_MAX = vMax;

    }

    public static String aceleracao(){
        return "9,8/w*s";
    }

    public double getVelocidadeAtual(){
        return velocidadeAtual;
    }



}
