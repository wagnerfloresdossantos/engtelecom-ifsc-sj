package engtelecom.poo;

/**
 * Interface que define um dispositivo de rede
 */
public interface DispositivoRede {

    /**
     * Processa um pacote de rede
     * @param pacote O pacote a ser processado
     */
    void processarPacote(Pacote pacote);
}
