#include <TimerOne.h>
#include <cppQueue.h> 

const int SCALE_PIN = 2;
const int HOLD_PIN = 3;
const int ADC_PIN = 0;
const float VCC = 5.0;
const float ADC_TOP = 1023.0;

int scale;
int hold;
int adc;
float voltage;
long next_isr[2];  

typedef void (*TaskFunction)();  // Definindo um tipo de função de tarefa

// Fila de Funções usando cppQueue
cppQueue taskQueue(sizeof(TaskFunction), 10, FIFO);  // Fila FIFO com capacidade para 10 tarefas

// Função para adicionar tarefas na fila
void addTask(TaskFunction task) {
  taskQueue.push(&task);  // Adiciona a tarefa na fila
}

// Função para executar as tarefas da fila
void executeTasks() {
  TaskFunction task;
  while (!taskQueue.isEmpty()) {
    taskQueue.pop(&task);  // Retira a tarefa da fila
    task();                // Executa a tarefa
  }
}

// Função para tratar o repique
void trata_repique(int pin)
{
  detachInterrupt(digitalPinToInterrupt(pin));
  next_isr[pin-2] = micros() + 20000;  // 20 ms para debounce
}

// Função para verificar e reabilitar as interrupções após repique
void verifica_isrs()
{
  if (micros() >= next_isr[0]) {
    attachInterrupt(digitalPinToInterrupt(SCALE_PIN), scale_isr, RISING);
  }
  if (micros() >= next_isr[1]) {
    attachInterrupt(digitalPinToInterrupt(HOLD_PIN), hold_isr, RISING);
  }
}

// Função de interrupção para o botão Scale
void scale_isr()
{
  Serial.println("Scale");
  scale = !scale;  // Alterna entre Volts e miliVolts
  trata_repique(SCALE_PIN);  
}

// Função de interrupção para o botão Hold
void hold_isr()
{
  Serial.println("Hold");
  hold = !hold;  // Alterna entre atualizar ou segurar
  trata_repique(HOLD_PIN);  
}

// Função chamada pelo Timer1 a cada 500ms para realizar leituras e atualizar a saída
void timerCallback()
{
  addTask(le_entradas);    // Adiciona a tarefa de leitura na fila
  addTask(processa_tensao);  // Adiciona a tarefa de processamento da tensão na fila
  addTask(atualiza_saidas);  // Adiciona a tarefa de atualização da saída na fila
}

// Função para ler o valor do ADC (média de 10 leituras)
void le_entradas()
{
  long soma = 0;
  for (int i = 0; i < 10; i++) {
    soma += analogRead(ADC_PIN);
    delay(1);  
  }
  adc = soma / 10;  // Média das 10 leituras
}

// Função para processar a tensão com base no valor lido do ADC
void processa_tensao()
{
  voltage = adc * (VCC / ADC_TOP);  // Converte para Volts
  
  if (scale == 1)  // Se o botão Scale estiver ativo, converte para miliVolts
  {
    voltage = voltage * 1000;
  }
}

// Função para atualizar as saídas via Serial, com base no estado de Hold
void atualiza_saidas()
{
  if (hold == 0)  // Só atualiza se o botão Hold não estiver ativado
  {
    Serial.print("Tensão: ");
    Serial.print(voltage);
    if (scale == 1) {
      Serial.println(" mV");
    } else {
      Serial.println(" V");
    }
  }
}

void setup()
{
  pinMode(SCALE_PIN, INPUT_PULLUP);  // Configura o botão Scale como entrada com pull-up
  pinMode(HOLD_PIN, INPUT_PULLUP);   // Configura o botão Hold como entrada com pull-up
  Serial.begin(9600);  // Inicializa a comunicação Serial

  scale = 0;  // Inicia com Volts
  hold = 0;   // Inicia com atualização ativa
  
  attachInterrupt(digitalPinToInterrupt(SCALE_PIN), scale_isr, RISING);
  attachInterrupt(digitalPinToInterrupt(HOLD_PIN), hold_isr, RISING);

  // Configura o Timer1 para chamar a função a cada 500ms
  Timer1.initialize(500000);  // 500 ms = 500000 µs
  Timer1.attachInterrupt(timerCallback);
}

void loop()
{
  verifica_isrs();  // Verifica se deve reabilitar as interrupções 
  executeTasks();   // Executa as tarefas da fila
}
