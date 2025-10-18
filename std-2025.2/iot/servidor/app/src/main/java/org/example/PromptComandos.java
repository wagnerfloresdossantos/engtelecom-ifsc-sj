package org.example;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Scanner;

public class PromptComandos implements Runnable{
    private Hashtable<Integer, Cliente> clientes; 

    public PromptComandos(Hashtable<Integer, Cliente> clientes){
        this.clientes = clientes;
    }

    @Override
    public void run() {
        Scanner teclado = new Scanner(System.in);
        String comando = "";
        do{
            System.out.println("> ");
            comando = teclado.nextLine();
               
            final var finalComando = comando + "\n";

            clientes.forEach((id, cliente)->{
                try{
                    cliente.saida().writeBytes(finalComando);
                }catch(IOException e){
                    System.err.println("Erro: "+ e.getMessage());
                }
            });

        }while(!comando.equals("sair"));
        System.exit(0);
        
    }
}
