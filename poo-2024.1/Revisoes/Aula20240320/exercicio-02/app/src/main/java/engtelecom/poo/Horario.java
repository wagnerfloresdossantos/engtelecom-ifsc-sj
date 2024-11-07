package engtelecom.poo;

public class Horario {

    // Atributos
    private int hora;
    private int minutos;
    private int segundos;
    private String numerosMinSeg [] = new String[]{"zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez",
            "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito",
            "dezenove", "vinte", "vinte e um", "vinte e dois", "vinte e três", "vinte e quatro",
            "vinte e cinco", "vinte e seis", "vinte e sete", "vinte e oito", "vinte e nove", "trinta",
            "trinta e um", "trinta e dois", "trinta e três", "trinta e quatro", "trinta e cinco",
            "trinta e seis", "trinta e sete", "trinta e oito", "trinta e nove", "quarenta",
            "quarenta e um", "quarenta e dois", "quarenta e três", "quarenta e quatro", "quarenta e cinco",
            "quarenta e seis", "quarenta e sete", "quarenta e oito", "quarenta e nove", "cinquenta",
            "cinquenta e um", "cinquenta e dois", "cinquenta e três", "cinquenta e quatro",
            "cinquenta e cinco", "cinquenta e seis", "cinquenta e sete", "cinquenta e oito",
            "cinquenta e nove"};
    private String numerosHoras [] = new String[]{"zero", "uma", "duas", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez",
            "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito",
            "dezenove", "vinte", "vinte e uma", "vinte e duas", "vinte e três"};

    // Método construtor padrão que inicialize todos atributos com zero

    public Horario(){
        this(0,0,0);
    }

    // Método construtor padrão hora, minuto e segundo
    public Horario(int h, int m, int s){
        if (!setHora(h) || !setMinutos(m) || !setSegundos(s)) {
            this.hora = 0;
            this.minutos = 0;
            this.segundos = 0;
        }
    }
    // Método construtor padrão hora
    public Horario(int h){
      this(h,0,0);
    }

    // Método construtor padrão hora e minuto
    public Horario(int h, int m){
        this(h, m, 0);
    }



    // Méwtodos Set
    public boolean setHora(int h) {
        if (h >= 0 && h < 24) {
            this.hora = h;
            return true;
        } else {
            return false;
        }
    }

    public boolean setMinutos(int m) {
        if (m >= 0 && m < 60) {
            this.minutos = m;
            return true;
        } else {
            return false;
        }
    }

    public boolean setSegundos(int s) {
        if (s >= 0 && s < 60) {
            this.segundos = s;
            return true;
        } else {
            return false;
        }
    }

    @Override
    public String toString() {
        return String.format("%02d:%02d:%02d", hora, minutos, segundos);
    }

    public String horarioPorExtenso(){
        String horaExtenso = numerosHoras[hora];
        String minutoExtenso = numerosMinSeg[minutos];
        String segundosExtenso = numerosMinSeg[segundos];
        return  horaExtenso + " horas, " + minutoExtenso + " minutos, e " + segundosExtenso + " segundos.";
    }

    public long horarioEmSegundos(){
        return hora * 3600 + minutos * 60 + segundos;
    }

    public long diferencaSegundos(Horario h){
                return Math.abs(h.horarioEmSegundos()-this.horarioEmSegundos()) ;
    }

}
