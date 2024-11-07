package engtelecom.poo.produto;

public class Telefone {

    protected int codigo;
    private String numeroSerie;
    private String modelo;
    private String cor;
    private double peso;


    public Telefone(int codigo, String numeroSerie, String modelo, String cor, double peso) {
        this.codigo = codigo;
        this.numeroSerie = numeroSerie;
        this.modelo = modelo;
        this.cor = cor;
        this.peso = peso;
    }

    public String imprimirDados() {
        return "Telefone{" +
                "codigo=" + codigo +
                ", numeroSerie='" + numeroSerie + '\'' +
                ", modelo='" + modelo + '\'' +
                ", cor='" + cor + '\'' +
                ", peso=" + peso +
                '}';
    }
}
