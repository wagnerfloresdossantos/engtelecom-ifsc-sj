package engtelecom.poo;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CarroTest {

    @Test
    public void validarConstrutor(){
        Carro c = new Carro();
        // esperado, obtido
        assertEquals(0,c.getVelocidadeAtual());
    }

    @Test
    public void testarAcelerar(){
        Carro c = new Carro();

        // esperado, obtido
        assertEquals(0,c.acelerar(-10));
        assertEquals(10,c.acelerar(10));
        assertEquals(10,c.acelerar(0));
        assertEquals(120,c.acelerar(400));
    }


    @Test
    public void testeFrear(){
        Carro c = new Carro();
        c.acelerar(30);

        assertEquals(0, c.frear(20));
        assertEquals(10, c.frear(0));
        assertEquals(10, c.frear(-1));
        assertEquals(0, c.frear(20));
    }


}
