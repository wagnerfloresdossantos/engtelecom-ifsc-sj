package engtelecom.poo;

import java.time.LocalDate;
import java.util.ArrayList;

public class Tarefa {


    private String titulo;
    private LocalDate prazoEntrega;
    private LocalDate dataConclusao;
    private ArrayList<Pessoa> listaPessoas;
    private Grupo grupo;

    public Tarefa(String titulo, LocalDate prazoEntrega, LocalDate dataConclusao, ArrayList<Pessoa> listaPessoas, Grupo grupo) {
        this.titulo = titulo;
        this.prazoEntrega = prazoEntrega;
        this.dataConclusao = dataConclusao;
        this.listaPessoas = listaPessoas;
        this.grupo = grupo;
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public LocalDate getPrazoEntrega() {
        return prazoEntrega;
    }

    public void setPrazoEntrega(LocalDate prazoEntrega) {
        this.prazoEntrega = prazoEntrega;
    }

    public LocalDate getDataConclusao() {
        return dataConclusao;
    }

    public void setDataConclusao(LocalDate dataConclusao) {
        this.dataConclusao = dataConclusao;
    }

    public ArrayList<Pessoa> getListaPessoas() {
        return listaPessoas;
    }

    public void setListaPessoas(ArrayList<Pessoa> listaPessoas) {
        this.listaPessoas = listaPessoas;
    }

    public Grupo getGrupo() {
        return grupo;
    }

    public void setGrupo(Grupo grupo) {
        this.grupo = grupo;
    }

    @Override
    public String toString() {
        return "Tarefa{" +
                "titulo='" + titulo + '\'' +
                ", prazoEntrega=" + prazoEntrega +
                ", dataConclusao=" + dataConclusao +
                ", listaPessoas=" + listaPessoas +
                ", grupo=" + grupo +
                '}';
    }
}
