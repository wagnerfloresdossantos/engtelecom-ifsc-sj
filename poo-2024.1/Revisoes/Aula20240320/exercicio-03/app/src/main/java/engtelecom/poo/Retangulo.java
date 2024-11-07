package engtelecom.poo;

public class Retangulo {

    // Atributos
    private int largura;
    private int altura;
    private String codigo;

    // Métodps Consrutores
    public Retangulo(int largura, int altura, String codigo) {
        if (!setAltura(altura) || !setLargura(largura) || !setCodigo(codigo)) {
            this.largura = 4;
            this.altura = 3;
            this.codigo = "ASCII";
        }
    }
    public Retangulo() {
       this(4,3,"ASCII");
    }

    // Métodps Get e Set
    public int getLargura() {
        return largura;
    }

    public boolean setLargura(int largura) {
        if (largura <= 0) {
            return false;
        } else {
            this.largura = largura;
            return true;
        }
    }

    public int getAltura() {
        return altura;
    }

    public boolean setAltura(int altura) {
        if (altura <= 0) {
            return false;
        } else {
            this.altura = altura;
            return true;
        }
    }

    public String getCodigo() {
        return codigo;
    }

    public boolean setCodigo(String codigo) {
        if (codigo.equals("ASCII") || codigo.equals("UTF8")) {
            this.codigo = codigo;
            return true;
        } else {
            this.codigo = "ASCII";
            return true;
        }
    }

    public int areaRetangulo(){
        return altura * largura;
    }

    public int perimetroRetangulo(){
        return 2 * (altura + largura);
    }


    public String toString() {
        StringBuilder sb = new StringBuilder();

        if (codigo.equals("UTF8")) {

            // Parte Superior do retângulo
            sb.append("\u250c");
            for (int i = 0; i < largura; i++) {
                sb.append("\u2500");
            }
            sb.append("\u2510\n");

            // Adiciona as linhas intermediarias
            for (int i = 0; i < altura - 2; i++) {
                sb.append("\u2502");
                for (int j = 0; j < largura; j++) {
                    sb.append(" ");
                }
                sb.append("\u2502\n");
            }
            // Adiciona a parte inferior do retangulo
            sb.append("\u2514");
            for (int i = 0; i < largura; i++) {
                sb.append("\u2500");
            }
            sb.append("\u2518\n");
        }else {
            // Parte Superior do retângulo
            sb.append("+");
            for (int i = 0; i < largura; i++) {
                sb.append("-");
            }
            sb.append("+\n");

            // Adiciona as linhas intermediarias
            for (int i = 0; i < altura - 2; i++) {
                sb.append("|");
                for (int j = 0; j < largura; j++) {
                    sb.append(" ");
                }
                sb.append("|\n");
            }
            // Adiciona a parte inferior do retangulo
            sb.append("+");
            for (int i = 0; i < largura; i++) {
                sb.append("-");
            }
            sb.append("+\n");
        }
        return sb.toString();
    }

}
