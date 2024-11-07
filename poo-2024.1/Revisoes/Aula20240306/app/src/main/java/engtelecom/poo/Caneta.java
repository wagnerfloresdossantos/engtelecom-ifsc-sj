package engtelecom.poo;

public class Caneta {


    // Atributos
    private int nivelTinta = 10; // 0
    private String cor; // Null
    private boolean aberta; // false


    // Método
    public void abrirFechar(){
        aberta =! aberta;
    }

    public void desenhar(){
        if((aberta) && (nivelTinta > 0)) {
            System.out.println("Desenhando na cor " + cor);
            nivelTinta--;
        }
    }

    public void definirCor(String c){
        cor = c;
    }

    public void definirNivelTinta(int n){
        nivelTinta = n;
    }

}
