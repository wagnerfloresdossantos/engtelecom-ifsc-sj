package engtelecom.poo;

public class Termometro {

private double tempAtual;
private double tempMaxima;
private double tempMinima;
private char escala;

    public Termometro(double tempAtual, double tempMaxima, double tempMinima, char escala) {
        this.tempAtual = tempAtual;
        this.tempMaxima = tempMaxima;
        this.tempMinima = tempMinima;
        this.escala = escala;
    }

    public double getTempAtual() {
        return tempAtual;
    }

    public void setTempAtual(double tempAtual) {
        this.tempAtual = tempAtual;
    }

    public double getTempMaxima() {
        return tempMaxima;
    }

    public void setTempMaxima(double tempMaxima) {
        this.tempMaxima = tempMaxima;
    }

    public double getTempMinima() {
        return tempMinima;
    }

    public void setTempMinima(double tempMinima) {
        this.tempMinima = tempMinima;
    }

    public char getEscala() {
        return escala;
    }

    public void setEscala(char escala) {
        this.escala = escala;
    }

    public String retornaValorEcala(char c){
        return "0";
    }

    public String diferenca(Termometro t, char c){
        return "0";
    }


}
