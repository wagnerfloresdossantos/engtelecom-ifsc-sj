package engtelecom.poo;


import java.util.Random;

public class Buzz {


    // Atrubutos

    private boolean capaceteAberto; // Capacete aberto , falsp
    private boolean disparaLaser;  // Laser disparado, falso
    private boolean asaAberta; // Asa aberta, falso
    private String frases [] = new String[]{"Ao infinito e além!",
            "Estamos em uma missão intergaláctica!",
            "Com o capacete retrátil, estou pronto para qualquer desafio!",
            "As asas se abrem, e a aventura começa!",
            "Laser carregado e pronto para ação!",
            "Buzz Lightyear, o brinquedo espacial mais corajoso do universo!"
    };

    // Métodos
        public void capaceteRetratil(){
        capaceteAberto =! capaceteAberto;
    }

    public void falarFrase(){
        Random r = new Random();
        int n = r.nextInt(frases.length);
        System.out.println(frases[n]) ;
    }

    public void disparaLaser(){
        System.out.println("Laser Disparado -------------- *");
    }

    public void golpear(){
        System.out.println("Golpeando...");
    }

    public void abreAsas(){
    }

}
