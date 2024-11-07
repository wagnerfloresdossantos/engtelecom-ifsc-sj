/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package engtelecom.poo;

import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;
import java.util.stream.Stream;

public class App {

    public static void main(String[] args) throws IOException {


        try (Scanner arq = new Scanner(App.class.getClassLoader().getResourceAsStream("produtos.txt"))){
            while (arq.hasNext()){
                System.out.println(arq.nextLine());
            }
        }catch (Exception e){
            System.err.println("Erro "+ e.toString());

        }


        String currentDir = System.getProperty("user.dir");

        Path path = Path.of(currentDir+"/arquivo.txt");

        if(Files.exists(path)) {
            System.out.println(String.format("Arquivo: %s", path.toAbsolutePath()));
            System.out.println(String.format("Regular: %s", Files.isRegularFile(path)));
            System.out.println(String.format("Diretório: %s", Files.isDirectory(path)));
            System.out.println(String.format("Permissão de leitura: %s", Files.isReadable(path)));
            System.out.println(String.format("Permissão de escrita: %s", Files.isWritable(path)));
        } else {
            System.out.println("Arquivo não encontrado");
        }



        String currentDir = System.getProperty("user.dir");

        Path dir = Path.of(currentDir);

        try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir)) {
            for (Path path : stream) {
                if(Files.isRegularFile(path)) {
                    System.out.println(path.getFileName());
                }
            }
        }catch (IOException e){
                System.err.println("Erro: " + e);
            }





        String currentDir = System.getProperty("user.dir");

        Path path = Path.of(args[0]);

        if(Files.exists(path)) {
            System.out.println(String.format("Arquivo: %s", path.toAbsolutePath()));
            System.out.println(String.format("Regular: %s", Files.isRegularFile(path)));
            System.out.println(String.format("Diretório: %s", Files.isDirectory(path)));
            System.out.println(String.format("Permissão de leitura: %s", Files.isReadable(path)));
            System.out.println(String.format("Permissão de escrita: %s", Files.isWritable(path)));
        } else {
            System.out.println("Arquivo não encontrado");
        }



        String currentDir = System.getProperty("user.dir");

        Path inicial = Path.of(currentDir);

      try (Stream<Path> walk = Files.walk(inicial)){
          walk.sorted().forEach(arq -> {
              int profundidade = inicial.relativize(arq).getNameCount();
          });
      }

    }


}
