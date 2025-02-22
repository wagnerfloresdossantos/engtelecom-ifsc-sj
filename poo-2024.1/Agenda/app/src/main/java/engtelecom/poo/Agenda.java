package engtelecom.poo;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;

public class Agenda {

    private ArrayList<Contato> agenda;

    public Agenda() {
        agenda = new ArrayList<>();
    }

    public ArrayList<Contato> getAgenda() {
        return agenda;
    }

    public boolean addContato(Contato c){
        if(agenda.contains(c)) {
            System.out.println("\nContato já existe!\n");
            return false;
        }
        agenda.add(c);
        System.out.println("\nContato Adicionado!\n");
        return true;
    }

    public boolean removeContato(String n, String s){
        return agenda.removeIf(elemento->elemento.getNome().equals(n) && elemento.getSobrenome().equals(s));
    }

    public boolean addTelefone(String r, String n, int posicao){
        try {
            return this.agenda.get(posicao).addTelefone(r, n);
        } catch (Exception e){
            return false;
        }
    }

    public boolean addEmail(String r, String m, int posicao){
        try {
            return this.agenda.get(posicao).addEmail(r, m);
        } catch (Exception e){
            return false;
        }
    }

    public boolean updateTelefone(String r, String n, int posicao){
        try {
            return this.agenda.get(posicao).updateTelefone(r, n);
        } catch (Exception e){
            return false;
        }
    }

    public boolean updateEmail(String r, String n, int posicao){
        try {
            return this.agenda.get(posicao).updateEmail(r, n);
        } catch (Exception e){
            return false;
        }
    }

    public boolean removeTelefone(String r, int posicao){
        try {
            return this.agenda.get(posicao).removeTelefone(r);
        } catch (Exception e){
            return false;
        }
    }

    public boolean removeEmail(String r, int posicao){
        try {
            return this.agenda.get(posicao).removeEmail(r);
        } catch (Exception e){
            return false;
        }
    }

    public boolean listaTodosContatos(){

        int i = 0;
        for(Contato contato: this.agenda){
            System.out.print("Posição: " + i + " ");
            System.out.println(contato);
            i++;
        }
        return true;
    }


    @Override
    public String toString() {
        return "Agenda{" +
                "agenda=" + agenda +
                '}';
    }
}
