package engtelecom.poo;

import java.util.ArrayList;

public class Carro {

    private String modelo;
    private Motor motor;
    private String cor;

    public Motor getMotor() {
        return motor;
    }

    public void setMotor(Motor motor) {
        this.motor = motor;
    }

    public Carro(String modelo, Motor motor, String cor) {
        this.modelo = modelo;
        this.motor = motor;
        this.cor = cor;
    }

    @Override
    public String toString() {
        return "Carro{" +
                "modelo='" + modelo + '\'' +
                ", motor=" + motor +
                ", cor='" + cor + '\'' +
                '}';
    }
}
