
package engtelecom.poo;

import java.util.Scanner;

public class App {
    

    public static void main(String[] args) {

        Scanner linhaArquivo = new Scanner(System.in);

        char matriz[][] = new char[9][9];
        int linha = 0;
        int coluna = 0;
        // 1° Passo - Criação da matriz
        while (linhaArquivo.hasNext()) {
            
            String aux = linhaArquivo.nextLine();
              
            // Percorre cada caracter da linha e coloca na matriz
            linha = 0;
            while (linha < 9) {
                matriz[linha][coluna] = aux.charAt(linha);
                linha++;
            }
            coluna++;
        }
        // 2° Passo - Registro das minas
        // Varredura da matriz
        for(int j = 0; j < matriz.length; j++){
            for(int i = 0; i < matriz.length; i++){

                //Caso a casa seja uma bomba, deixa a bomba e continua varredura
                //adjacencias
                if(matriz[i][j] != '*'){
                    int cont = 0;
                    
                    //Verifica adjacencias em cima

                    //Se for linha 0 nem precisa verificar em cima
                    if(i != 0){   
                        for(int k = j-1; k < j+2; k++){
                                //parede esquerda
                                if(k < 0){ 
                                    k = 0;
                                }
                                //parede direita
                                if(k <= 8){ 
                                    if(matriz[i-1][k] == '*'){
                                        cont++;
                                    }
                                }
                        
                        }
                    }

                    //Verifica adjascencias nos lados
                    
                    //Se a casa for nas extremidades, não verifica nos lados
                    if(j-1 >= 0){
                        if(matriz[i][j-1] == '*') {
                            cont++;
                        }
                    }

                    if(j+1 != 9){
                        if(matriz[i][j+1] == '*') {
                            cont++;
                        }
                    }

                    //Verifica adjascencias em baixo

                    //Se for linha 8 não verifica em baixo
                    if(i != 8){   
                        for(int k = j-1; k < j+2; k++){

                            //Verifica limite da esquerda
                            if(k < 0){ 
                                k = 0;
                            }

                            //Verifica limite da direita
                            if(k <= 8){
                                if(matriz[i+1][k] == '*'){
                                    cont++;
                                }
                            }
                        }
                    }
                    
                    //Adiciona numero de bombas adjascentes
                    if(cont > 0){
                        matriz[i][j] = Character.forDigit(cont, 10); 
                    }
                }
            }
        }

        // Mostra a matriz com os resultados na tela
        for (int i = 0; i < matriz.length; i++) {
            for (int j = 0; j < matriz.length; j++) {
                System.out.print(matriz[i][j]);
            }
            System.out.println();
        }
    }
}
