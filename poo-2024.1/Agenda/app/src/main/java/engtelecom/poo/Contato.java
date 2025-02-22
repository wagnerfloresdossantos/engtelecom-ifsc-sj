package engtelecom.poo;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.function.Predicate;

public class Contato {

    private String nome;
    private String sobrenome;
    private LocalDate dataNasc;
    private ArrayList<Telefone> telefones;
    private ArrayList<Email> emails;

    public Contato(String nome, String sobrenome, LocalDate dataNasc) {
        this.nome = nome;
        this.sobrenome = sobrenome;
        this.dataNasc = dataNasc;
        this.telefones = new ArrayList<>();
        this.emails = new ArrayList<>();
    }


    public boolean addTelefone(String r, String n){
       Telefone tel = new Telefone(r,n);
       return telefones.add(tel);
    }

    public boolean addEmail(String r, String e){
        Email email = new Email(r,e);
        return emails.add(email);
    }

    public boolean removeTelefone(String r) {
        return telefones.removeIf(elemento -> elemento.getRotulo().equals(r));
    }
    public boolean removeEmail(String e){
        return emails.removeIf(elemento -> elemento.getRotulo().equals(e));
    }

    public boolean updateTelefone(String r, String n){
        if(removeTelefone(r)){
            return addTelefone(r,n);
        }
        return false;
    }

    public boolean updateEmail(String r, String e){
        if(removeEmail(r)) {
            return addEmail(r, e);
        }
        return false;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getSobrenome() {
        return sobrenome;
    }

    public void setSobrenome(String sobrenome) {
        this.sobrenome = sobrenome;
    }

    public LocalDate getDataNasc() {
        return dataNasc;
    }

    public void setDataNasc(LocalDate dataNasc) {
        this.dataNasc = dataNasc;
    }

    public ArrayList<Telefone> getTelefones() {
        return telefones;
    }

    public void setTelefones(ArrayList<Telefone> telefones) {
        this.telefones = telefones;
    }

    public ArrayList<Email> getEmails() {
        return emails;
    }

    public void setEmails(ArrayList<Email> emails) {
        this.emails = emails;
    }

    @Override
    public String toString() {
        return "Contato{" +
                "nome='" + nome + '\'' +
                ", sobrenome='" + sobrenome + '\'' +
                ", dataNasc=" + dataNasc +
                ", telefones=" + telefones +
                ", emails=" + emails +
                '}';
    }
}
