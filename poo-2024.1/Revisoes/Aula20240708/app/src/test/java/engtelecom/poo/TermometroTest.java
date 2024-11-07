package engtelecom.poo;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class TermometroTest {

    @Test
    public void validarConstrutor(){
        Termometro c = new Termometro(10,100,0,'C');

    }

    @Test
    public void testeRetornaValorEscala(){
        Termometro t = new Termometro(40,100,0,'C');
        // esperado, obtido
        assertEquals("C(A=40, Min=0, Max=100)",t.retornaValorEcala('C'));
        assertEquals("K(A=313,15, Min=273,15, Max=373,15)",t.retornaValorEcala('F'));
        assertEquals("F(A=104, Min=32, Max=212)",t.retornaValorEcala('F'));


    }

    public void testeDiferenca(){

    }

}
