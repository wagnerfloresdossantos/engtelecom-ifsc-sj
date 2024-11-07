public class Exercicio02 {
    
    public static void main(String[] var0) {

       // verifica se foram informadas as 3 notas via argumento 
       if (var0.length != 3) {
          System.out.println("notas invalidas, preencha p1, p2 e a");

       // imprime a quantidade de notas recebidas via argumento
       // imprime o valor de cada nota vinculado a determidada avaliação 
       } else {
          System.out.println("Forneceu " + var0.length + " notas");
          System.out.println("Notas Fornecidas: ");
          System.out.println("P1: " + var0[0]);
          System.out.println("P2: " + var0[1]);
          System.out.println("a: " + var0[2]);

          // variavel CD que recebe valor da equação
          double CF = (double)Math.round((Double.parseDouble(var0[0]) * 2.0 + Double.parseDouble(var0[1]) * 3.0) / 5.0 * 0.9 + Double.parseDouble(var0[2]) * 0.1);
          
          // imprime o conceiro final e se o aluno foi aprovado CF>=6 ou reprovado
          System.out.println("Conceito Final: " + CF);
          if (CF >= 6.0) {
             System.out.println("APROVADO");
          } else {
             System.out.println("REPROVADO");
          }
       }
 
    }
 }