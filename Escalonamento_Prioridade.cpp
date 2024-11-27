
/*+-------------------------------------------------------------+
 | UNIFAL – Universidade Federal de Alfenas.                    |
 | BACHARELADO EM CIENCIA DA COMPUTACAO.                        |
 | Trabalho..: Escalonamento por Prioridade                     |
 | Disciplina: Sistemas Operacionais                            |
 | Professor.: Fellipe Rey                                      |
 | Aluno(s)..: Diogo da Silva Moreira - 2023.1.08.003           |
 | Pedro Henrique Botelho da Silva - 2023.1.08.027              |
 | Data......:                                                  |
 +-------------------------------------------------------------+*/

#include <iostream>
#include <queue>
#include <vector>
#include <iomanip>
#include <limits>  

using namespace std;

// estrutura que representa um processo
struct Processo {
    int id;
    int prioridade;
    int tempoExecucao;
    int tempoRestante;

    // para a fila de prioridade
    bool operator<(const Processo& p) const {
        return prioridade > p.prioridade;
    }
};

// função para adicionar um processo à fila de prioridades
void adicionarProcessos(priority_queue<Processo> &fila, int n) {
    for (int i = 0; i < n; i++) {
        Processo p;
        cout << "\nInsira os dados do processo " << i+1 << endl;
        cout << "ID do Processo: ";
        cin >> p.id;
        cout << "Prioridade: ";
        cin >> p.prioridade;
        cout << "Tempo total de execucao: ";
        cin >> p.tempoExecucao;

        p.tempoRestante = p.tempoExecucao;

        // adiciona o processo na fila de prioridade
        fila.push(p);
    }
}

// função para exibir os processos na fila no momento
void mostrarFila(priority_queue<Processo> fila) {
    vector<Processo> processos;
    cout << "\nEstado atual da fila de processos:\n";
    cout << left << setw(10) << "ID" << setw(15) << "Prioridade" << setw(20) << "Tempo Execucao" << setw(20) << "Tempo Restante" << endl;
    while (!fila.empty()) {
        Processo p = fila.top();
        fila.pop();
        processos.push_back(p);
        cout << left << setw(10) << p.id << setw(15) << p.prioridade << setw(20) << p.tempoExecucao << setw(20) << p.tempoRestante << endl;
    }

    // recoloca os processos na fila original
    for (Processo p : processos) {
        fila.push(p);
    }
}

// função que executa o escalonamento por prioridade
void escalonarPorPrioridade(priority_queue<Processo> &fila, int quantum) {
    int tempoTotal = 0;  // aqui para acompanhar o tempo total de execução
    while (!fila.empty()) {
        mostrarFila(fila);
        Processo p = fila.top();
        fila.pop();

        cout << "\nExecutando processo ID: " << p.id << " com prioridade: " << p.prioridade << endl;

        // executa o processo pelo quantum ou até o final do tempo de execução
        int tempoExecutado = (p.tempoRestante > quantum) ? quantum : p.tempoRestante;
        p.tempoRestante -= tempoExecutado;
        tempoTotal += tempoExecutado;

        cout << "Processo " << p.id << " executado por " << tempoExecutado << " unidades de tempo. Restante: " << p.tempoRestante << "\nTempo total de execução até agora: " << tempoTotal << endl;

        // se o processo não terminou, ele volta à fila com prioridade reajustada
        if (p.tempoRestante > 0) {
            p.prioridade++;  // rebaixa a prioridade
            cout << "Processo " << p.id << " rebaixado para prioridade " << p.prioridade << endl;
            fila.push(p);
        } else {
            cout << "Processo " << p.id << " finalizado." << endl;
        }

        // pause para depuração passo a passo
        cout << "\nPressione Enter para continuar para o próximo passo..." << endl;
        cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');  // limpa o buffer
        cin.get();  // aguarda o usuário pressionar Enter
    }

    cout << "\nTodos os processos foram finalizados! Tempo total de execução: " << tempoTotal << endl;
}

int main() {
    priority_queue<Processo> fila;
    int numProcessos, quantum;

    // entrada de dados pelo usuário
    cout << "Bem-vindo ao escalonador por prioridade!" << endl;
    cout << "Insira o número de processos: ";
    cin >> numProcessos;
    cout << "Insira o valor do quantum: ";
    cin >> quantum;

    adicionarProcessos(fila, numProcessos);

    // executar o escalonador
    escalonarPorPrioridade(fila, quantum);

    return 0;
}
