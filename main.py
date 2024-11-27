from typing import Type
import time
import os


"""
Classe que representa um processo.

@param    int    pid                 pid do processo
@param    int    time                Tempo de execução do processo
@param    int    current_priority    Prioridade atual do processo
@param    int    original_priority   Prioridade original do processo
"""
class Process:
    def __init__(self, pid: int, time: int, current_priority: int, original_priority: int):
        self.id = pid
        self.time = time
        self.current_priority = current_priority
        self.original_priority = original_priority
        self.waiting_time = 0


"""
Classe que representa uma fila de processos.
"""
class Queue:
    def __init__(self):
        self.processes = []

    """
    Método que adiciona um processo à fila.

    @param    Process    process    Processo a ser adicionado à fila.
    """
    def enqueue(self, process: Type[Process]):
        self.processes.append(process)

    def dequeue(self):
        return self.processes.pop(0) if self.processes else None

    """
    Método __str__ é retornado quando a classe é printada, 
     mostrando os processos de forma organizada.
    """
    def __str__(self):
        return ' '.join([f"[P{process.id} {process.time}u.t]" for process in self.processes])


"""
Classe que simula/representa um processador.
Responsável pelo processamento, escalonamento e alteração
 de prioridade dos processos.

@param    int    max_waiting_time    Tempo máximo que um processo
                                      deve aguardar sem ser processado
@param    int    quantum             Quantum do processador utilizado no Round Robin
"""
class Scheduler:
    def __init__(self, max_waiting_time: int, quantum: int):
        self.priority_queues = []  # filas de prioridade
        self.max_waiting_time = max_waiting_time
        self.quantum = quantum
        self.elapsed_time = 0
        self.global_pid = 1  # variável utilizada para nomear os processos
        self.history = []  # array que armazena o histórico de output

    """
    Método responsável por limpar a tela, tanto no Linux como no Windows.
    Utilizado para dar dinamismo nas saídas.
    """
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    """
    Método que mostra o estado atual das filas de prioridade.
    """
    def print_state(self):
        # Mostrando as filas em ordem reversa, decrescente
        for i in range(len(self.priority_queues) - 1, -1, -1):
            print(f"FILA {i + 1}: [{self.priority_queues[i]}]")

    """
    Método responsável por atualizar e mostrar o histórico
     de saídas. Também é responsável por mostrar o estado
     atual das filas de prioridade.

    @param    str    message     Mensagem que será adicionada ao histórico
    """
    def update_history(self, message: str):
        self.history.append(message)
        self.clear_screen()
        for event in self.history:
            print(event)
        self.print_state()

    """
    Método que implementa o método Round Robin nas filas
     de prioridade. Processa os processos na fila de
     maior prioridade, elevando a prioridade dos processos
     das outras filas conforme necessário.
    """
    def round_robin(self):
        # Loopando enquanto existirem processos nas filas de prioridade
        while any(queue.processes for queue in self.priority_queues):
            # Obtendo índice das filas de prioridade em ordem reversa, decrescente
            for priority in range(len(self.priority_queues) - 1, -1, -1):
                queue = self.priority_queues[priority]  # Acessando fila

                # Se não houver processos, próxima fila
                if not queue.processes:
                    continue

                # Remove o processo da fila
                process = queue.dequeue()
                if not process:
                    continue

                self.update_history("----------------------------------------------")
                self.update_history(f"Tempo {self.elapsed_time}: Processando P{process.id} da F{process.current_priority + 1} - ({process.time}u.t)")

                time.sleep(1)

                """
                Atualiza o tempo de espera dos processos das outras filas
                 de prioridade.
                """
                for p_queue in self.priority_queues:
                    for p in p_queue.processes:
                        p.waiting_time += self.quantum

                """
                A função min() obtém o menor valor entre dois valores.
                Dessa forma, o tempo para processar é o quantum ou o 
                 tempo do processo.
                Se o processo tiver tempo > quantum, o tempo de processamento
                 será o do quantum.
                Se o processo tiver tempo < quantum, o tempo de processamento
                 será o do processo.
                """
                time_to_process = min(self.quantum, process.time)
                process.time -= time_to_process  # Atualizando tempo do processo
                self.elapsed_time += time_to_process  # Atualizando variável de tempo passado
                process.waiting_time = 0  # Zerando tempo de espera

                self.promote_processes()  # Verificando se existem processos a serem promovidos

                if process.time > 0:  # Processo não finalizado
                    # Se o processo foi promovido anteriormente, deve retornar à fila original
                    if process.current_priority != process.original_priority:
                        self.update_history(f"Tempo {self.elapsed_time}: Processo P{process.id} retornou à F{process.original_priority + 1}")
                        process.current_priority = process.original_priority
                    # Devolvendo o processo à sua respectiva fila de processos
                    self.priority_queues[process.current_priority].enqueue(process)
                else:  # Processo finalizado
                    self.update_history(f"Tempo {self.elapsed_time}: Processo P{process.id} finalizado")

                break  # Processando a mesma fila, não indo adiante

    """
    Método responsável por verificar quantos/quais
     processos devem ser promovidos, considerando o tempo
     máximo de espera e o tempo de espera de cada um.
    """
    def promote_processes(self):
        # Obtendo listas de prioriodade na ordem reversa, decrescente
        for priority in range(len(self.priority_queues) - 2, -1, -1):
            queue = self.priority_queues[priority]  # Acessando a fila de prioridade
            # Loopando pelos processos da fila
            for process in list(queue.processes):
                # Se o tempo de espera exceder o tempo máximo de espera, então eleva a prioridade
                if process.waiting_time >= self.max_waiting_time:
                    # Prevenindo o escanolamento para uma fila inexistente
                    if process.current_priority < len(self.priority_queues) - 1:
                        self.update_history(f"Tempo {self.elapsed_time}: Promovendo processo P{process.id} de F{priority + 1} para F{priority + 2}")
                        queue.processes.remove(process)  # Remove-o da fila atual
                        process.current_priority += 1
                        self.priority_queues[process.current_priority].enqueue(process)  # Adiciona-o na fila correta
                        process.waiting_time = 0  # Zera o contador de tempo de espera

    """
    Método responsável por adicionar um processo à sua
     respectiva fila de prioridades. É utilizado, de fato,
     para a criação de processos.

    @param    int     priority    Número/fila de prioridade do processo
    @param    int     time        Tempo do processo
    """
    def add_process(self, priority: int, time: int):
        process = Process(self.global_pid, time, priority, priority)
        self.global_pid += 1
        self.priority_queues[priority].enqueue(process)




if __name__ == "__main__":
    # Lendo e validando variáveis
    quantum = int(input("Insira o quantum: "))
    while(quantum <= 0):
        print("O quantum deve ser inteiro positivo!")
        quantum = int(input("Insira o quantum: "))

    max_waiting_time = int(input("Insira o tempo máximo de espera: "))
    while(max_waiting_time <= 0):
        print("O tempo máximo de espera deve ser inteiro positivo!")
        max_waiting_time = int(input("Insira o tempo máximo de espera: "))

    num_priority_queues = int(input("Insira a quantidade de filas de prioridade: "))
    while(num_priority_queues <= 0):
        print("A quantidade de filas deve ser inteiro positivo!")
        num_priority_queues = int(input("Insira a quantidade de filas de prioridade: "))

    # Instanciando classe Scheduler
    scheduler = Scheduler(max_waiting_time, quantum)
    
    # Adicionando filas vazias, na quantidade indicada pelo usuário
    for i in range(num_priority_queues):
        scheduler.priority_queues.append(Queue())
    
    # Loopando pelas filas em ordem reversa, decrescente
    for i in range(num_priority_queues - 1, -1, -1):
        num_processes_queue = int(input(f"Insira a quantidade de processos da fila de prioridade {i + 1}: "))
        while(num_processes_queue <= 0):
            print("A quantidade de processos da fila de prioridade deve ser inteiro positivo!")
            num_processes_queue = int(input(f"Insira a quantidade de processos da fila de prioridade {i + 1}: "))

        for j in range(num_processes_queue):
            print(f"    Fila {i + 1}:")
            p_time = int(input(f"       Tempo do processo {scheduler.global_pid}: "))
            while(p_time <= 0):
                print("O tempo do processo deve ser inteiro positivo!")
                p_time = int(input(f"       Tempo do processo {scheduler.global_pid}: "))

            scheduler.add_process(i, p_time)
    
    scheduler.round_robin()