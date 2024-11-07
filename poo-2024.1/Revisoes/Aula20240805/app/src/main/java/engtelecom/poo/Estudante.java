package engtelecom.poo;

public class Estudante<T extends Pessoa> {

    private String matricula;
    private String nome;

    public Estudante(String matricula, String nome) {
        this.matricula = matricula;
        this.nome = nome;
    }

    @Override
    public String toString() {
        return "Estudante{" +
                "matricula='" + matricula + '\'' +
                ", nome='" + nome + '\'' +
                '}';
    }
}
