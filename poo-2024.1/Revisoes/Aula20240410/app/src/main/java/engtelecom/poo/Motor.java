package engtelecom.poo;

public class Motor {

    private String potencia;
    private String velocidade;

    public Motor(String potencia, String velocidade) {
        this.potencia = potencia;
        this.velocidade = velocidade;
    }



    @Override
    public String toString() {
        return "Motor{" +
                "potencia='" + potencia + '\'' +
                ", velocidade='" + velocidade + '\'' +
                '}';
    }
}
