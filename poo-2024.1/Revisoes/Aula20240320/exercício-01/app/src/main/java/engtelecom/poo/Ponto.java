package engtelecom.poo;

public class Ponto {

// Atributos
private double x;
private double y;

    // Método Contrutor
    public Ponto(double x, double y) {
        this.x = x;
        this.y = y;
    }

    // Métodos get e set
    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double getY() {
        return y;
    }

    public void setY(double y) {
        this.y = y;
    }

    // Método toString
    @Override
    public String toString() {
        return "(" + x + ", " + y +")";
    }

    public double distancia(Ponto p){
        return  Math.sqrt((Math.pow((p.getX()-this.getX()),2)) + Math.pow((p.getY()-this.getY()),2));
    }




}
