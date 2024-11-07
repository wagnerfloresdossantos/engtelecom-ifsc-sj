package engtelecom.poo;

public class Carro {

    private String modelo;

    public Carro(String carro) {
        this.modelo = carro;
    }


    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Carro carro = (Carro) o;
        return Objects.equals(modelo, carro.modelo);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(modelo);
    }

    @Override
    public String toString() {
        return "Carro{" +
                "modelo='" + modelo + '\'' +
                '}';
    }
}
