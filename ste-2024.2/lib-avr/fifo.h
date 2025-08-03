#ifndef __FIFO_H__
#define __FIFO_H__

template<int N, typename T>
class Fifo 
{  
private:
    T data[N];
    int in;
    int out;
    int size;

public:
    Fifo()
        : in(0), out(-1), size(0) {}

    void put(T c)
    {
        if (isFull()) 
        {
            return;
        }
        data[in] = c;
        in = (in + 1) % N;  
        size++;
    }

    T get()
    {
        if (isEmpty())
        {
            return '\0';
        }
        T value = data[out];
        out = (out + 1) % N;
        size--; 
        return value;
    }

    int currentSize() const
    {
        return size;
    } 

    bool isFull() const
    {
        return size == N;
    }

    bool isEmpty() const
    {
        return size == 0;
    }
};

#endif
