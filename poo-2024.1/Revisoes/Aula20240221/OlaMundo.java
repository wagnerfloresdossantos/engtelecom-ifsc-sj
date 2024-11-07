import java.util.Scanner;

public class OlaMundo {
    
    public static void main(String args[]){

        Scanner teclado = new Scanner(System.in);

        System.out.print("entre com seu nome: ");

        String nome = teclado.nextLine();

        System.out.println("Bom dia " + nome);

        int i = teclado.nextInt();
        int d = teclado.nextDouble();
        
    }
/* 
        System.out.println("Olá Mundo");

        int i = 0;

        //float f = 2.1;

        double d = 2.2;

        char c = 's';

       // boolean b = true;

        int ano = 2024;
        String nome = "Wagner";

        System.out.println("Nome: " + nome + " ano: " + ano);

        int a = 10;
        int b = 20;

        if (a == b){
            System.out.println("são iguais");
        } else if (a > b) {
            System.out.println("a é maior");
        } else{
            System.out.println("b é maior");
        }

        switch (nome) {
            case value:
                
                break;
        
            default:
                break;
        }


        temp = a + 1;
        while (a < b){
            System.out.println("temp");
            temp ++;
        }

        for (int i = a+1; i <b; i++){
            System.out.println(i);

        }



    }

    */

}
