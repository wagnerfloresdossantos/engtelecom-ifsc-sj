package engtelecom.poo;

public class Pessoa {

    private String Pessoa;

    public Pessoa(String pessoa) {
        Pessoa = pessoa;
    }

    @Override
    public String toString() {
        return "Pessoa{" +
                "Pessoa='" + Pessoa + '\'' +
                '}';
    }
}
