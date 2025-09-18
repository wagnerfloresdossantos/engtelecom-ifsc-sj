package engtelecom.std;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class AtenderCliente implements Runnable{

    private Socket cliente;
    
    public AtenderCliente(Socket cliente){
        this.cliente = cliente;
    }
    
    @Override
    public void run() {
        if (cliente != null){

            try {

            System.out.println("Cliente conectado: " + cliente.getInetAddress());

            // Estabelecimento dos fluxos de entrada
            BufferedReader entrada = new BufferedReader(new InputStreamReader(cliente.getInputStream(), "UTF-8"));
            DataOutputStream saida = new DataOutputStream(cliente.getOutputStream());

            // Comunicação
            String recebido = entrada.readLine();
            System.out.println("Cliente falou: " + recebido);
            saida.writeBytes(recebido.toUpperCase() +"\n");
            

        }catch (IOException e){
            System.err.println("Erro ao iniciar servidor: " + e.getMessage());
        }


        }
        
       
    }
    
}
