/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package engtelecom.poo;

import java.util.ArrayList;

public class App {

    public static void main(String[] args) {



        Pessoa p = new Pessoa("Juca");
        Estudante e = new Estudante("Juca","233");
        Carro carro = new Carro("Fusca");

        ArrayList<Carro> arrayList = new ArrayList<>();

        Caixa <Carro> caixa = new Caixa<>();

        caixa.setConteudo(carro);

        Carro outro = caixa.getConteudo();

        Caixa<Pessoa> nova = new Caixa<>();
        nova.setConteudo(p);

        System.out.println(nova);

        /*
        Caixa c = new Caixa();
        c.setConteudo(e);
        c.setConteudo(carro);
        c.setConteudo(p);

        Carro outro = (Carro) c.getConteudo();

        System.out.println(outro);
 */

    }
}