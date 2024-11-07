import java.util.Scanner;

public class Exercicio01 {

    public static void main(String[] args){

        // Criado objeto teclado para ler as informações
        Scanner teclado = new Scanner(System.in);

        // Imprimindo na tela
        System.out.print("Entre com o nome: ");

        // Lendo a informação do teclado para a Stirng "nome"
        String nome = teclado.nextLine();

        // Impriimindo na tela
        System.out.print("Entre com o ano que nasceu: ");

        // Lendo a informação do teclado para o int "anoNasc"
        int anoNasc = teclado.nextInt();

        // Impriimindo na tela
        System.out.print("Entre com o ano Atual: ");

        // Lendo a informação do teclado para o int "anoAtual"
        int anoAtual = teclado.nextInt();

        // Calculado a idade
        int idade = (anoAtual - anoNasc);
        
        // Imprimindo na tela
        System.out.println(nome + ", possui " + idade + " anos") ;
    }
}