import java.util.Random;
import java.util.Scanner;

public class Exercicio03 {

    public static void main(String[] args) {
    
    // Cria objeto teclado     
    Scanner teclado = new Scanner(System.in);    

    // obtendo numeros pseudo aletários de 1 a 100 
    Random r = new Random();

    // atribui o numero sorteado a variável
    int numeroSorteado = r.nextInt(100)+1;

    // variável do palpite fornecido para o usuário
    int palpite;

    // variavel para o contador de tentativas
    int tentativas = 0;
    
    // Vetor para contar a quantidade de cada palpite anterior
    int[] contadorPalpiteAnterior = new int [100];    

    System.out.println("tente descobrir um numero entre 1 e 100");
        
        // loop para entativas enquanto o numro sorteado não é igual ao do palpite
        do {
         System.out.print("Digite o Papite: ");

         palpite = teclado.nextInt();
         tentativas++;

         if (contadorPalpiteAnterior [palpite - 1] > 0){
            System.out.println("Você escolheu " + contadorPalpiteAnterior[palpite - 1] + " vezes .. tente outro");
    
        } else{
             if (palpite == numeroSorteado){
                 System.out.println("Parabéns você acertou em " + tentativas + ".");
             } else if (palpite < numeroSorteado) {
                System.out.println("Experimente um número maior, o número sorteado está entre " + (palpite + 1) + " e 100");
             } else {
                 System.out.println("Experimente um número menor, o número sorteado está entre 1 e " + (palpite - 1) + ".");
             }
          
            }
            contadorPalpiteAnterior[palpite - 1]++;
     } while (palpite != numeroSorteado);
    }  
}