package engtelecom.poo;

import java.util.Arrays;

public class Data {

    // Atributos
    private int dia;
    private int mes;
    private int ano;
    private String meses [] = new String[] {"Janeiro","Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"};

    // Dias máximos em cada mês (considerando ano não bissexto)
    private final int[] DIAS_MAXIMOS = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    // Método construtor padrão que inicializa com a data 01/01/1970;
    public Data(){
        this(1,1,1970);
    }
    // Método construtor sobrecarregado para dia
    public Data(int dia){
        this(dia,1,1970);
    }

    // Método construtor sobrecarregado para dia e mês
    public Data(int dia, int mes){
        this(dia,mes,1970);
    }

    // Método construtor sobrecarregado para dia, mês e ano
    public Data(int dia, int mes, int ano) {


        this.dia = dia;
        this.mes = mes;
        this.ano = ano;

    }

    public int getDia() {
         return dia;
    }

    // Metodo set para dia
    public boolean setDia(int dia) {
        if (validaData(dia, mes, ano)) {
            this.dia = dia;
            return true;
        }else {
            return false;
        }
    }

    public int getMes() {
        return mes;
    }

    // Metodo set para mês
    public boolean setMes(int mes) {
        if(validaData(dia, mes,ano)) {
            this.mes = mes;
            return true;
        } else {
            return false;
        }
    }

    public int getAno() {
        return ano;
    }

    // Metodo set para ano
    public boolean setAno(int ano) {
        if(validaData(dia, mes,ano)) {
            this.ano = ano;
            return true;
        } else{
            return false;
        }
    }
    // Métodp para validar data
    private boolean validaData(int dia, int mes, int ano){
        if (ano < 1 ||  dia < 1 || mes > 12 || dia < 1 || dia > DIAS_MAXIMOS[mes-1]){
            return false;
        }
        // Verifica Bissexto
        if (mes == 2 && dia == 29 && (ano % 4 == 0 && (ano % 100 != 0 || ano % 400 ==0 ))){
            return true;
        }
        return true;
    }

    @Override
    public String toString() {
        return String.format("%02d/%02d/%04d", dia, mes, ano);
    }

    public String dataPorExtenso(){
        String mesExtenso = meses[mes-1];
        return  dia + " de " + mesExtenso + " de " + ano + ".";
    }

    public int diasDesdeOinicio(){

        /**
         * int total de dias
         *
         * laço para anos
         * if bissexto 366 dias
         * else normais 365
         *
         * laço para os meses
         * if bissexto
         *
         * total de dias = dia
         *
         * return dia
         */
        return dia;
    }

    public int difercaDias(Data d){
        /**
         * dias na data - dias na outra data
         */
        return dia;
    }


}
