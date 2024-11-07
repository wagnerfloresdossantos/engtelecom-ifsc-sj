package engtelecom.poo.produto;

public class SemFio  extends Telefone{

    private double frequencia;
    private int canais;
    private double distanciaOperacao;


    public SemFio(int codigo, String numeroSerie, String modelo, String cor, double peso, double frequencia, int canais, double distanciaOperacao) {
        super(codigo, numeroSerie, modelo, cor, peso);
        this.frequencia = frequencia;
        this.canais = canais;
        this.distanciaOperacao = distanciaOperacao;
    }

    @Override
    public String imprimirDados() {

        return super.imprimirDados() + "Freq: " + this.frequencia;
    }

}
