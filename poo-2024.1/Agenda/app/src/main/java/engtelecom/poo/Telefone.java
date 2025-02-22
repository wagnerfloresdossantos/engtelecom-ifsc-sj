package engtelecom.poo;


import javax.swing.text.MaskFormatter;
import java.text.ParseException;
import java.util.ArrayList;

public class Telefone {

    private String rotulo;
    private String numeroTelefone;

    public Telefone(String rotulo, String numeroTelefone) {
        this.rotulo = rotulo;
        this.numeroTelefone = numeroTelefone;
    }

    public String getRotulo() {
        return rotulo;
    }

    public void setRotulo(String rotulo) {
        this.rotulo = rotulo;
    }

    public String getNumeroTelefone() {
        return numeroTelefone;
    }

    public void setNumeroTelefone(String numeroTelefone) {
        this.numeroTelefone = numeroTelefone;
    }

    public String formata(String mascara, String valor){
        MaskFormatter mask = null;
        String resultado = "";
        try {
            mask = new MaskFormatter(mascara);
            mask.setValueContainsLiteralCharacters(false);
            mask.setPlaceholderCharacter('_');
            resultado = mask.valueToString(valor);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return resultado;
    }

    @Override
    public String toString() {
        return "Telefone{" +
                "rotulo='" + rotulo +
                ", numeroTelefone='" + formata("(##) #####−####",numeroTelefone);
    }
}
