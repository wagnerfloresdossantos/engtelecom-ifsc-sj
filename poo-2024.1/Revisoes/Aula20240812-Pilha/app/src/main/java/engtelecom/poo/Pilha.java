package engtelecom.poo;

public class Pilha<E> {

    private E[] vetor;
    private int topo;
    private int tamanho;

    public Pilha(int tamanho) {
        this.vetor = (E[]) new Object[tamanho];
        this.topo = -1;
        this.tamanho = tamanho;
    }

    public boolean empilhar(E elemento) throws PilhaCheiaException {
        if(!isPilhaCheia()){
            this.vetor[++topo] = elemento;
            return true;
        } else {
            throw new PilhaCheiaException("Pilha está cheia");
        }
    }

    public E dsempilhar() throws PilhaVaziaExeception {
        if(isPinhaVazia()){
            throw new PilhaVaziaExeception("Pilha está vazia");
        }
        return this.vetor[topo--];
    }

    public E obterElementoTop() {
        return vetor[this.topo];
    }

    public boolean isPinhaVazia(){
        return this.topo == -1;
    }

    public boolean isPilhaCheia(){
        return this.topo == tamanho;
    }

}
