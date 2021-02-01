import numpy as np
import pylab as p
from scipy import integrate
from matplotlib import pyplot as plt

def dX_dt(X, t=0):
    """
        Retorna a taxa de crescimento para as populacoes de tubaroes e peixes.
    """
    u, v = X[0], X[1]
    return np.array([
        a * u - b * u * v, 
        -c * v + d * b * u * v
    ])

def plot_evolucao(X):
    """
    Geracao do grafico para visualizar a evolucao das populacoes
    """
    peixes, tubaroes = X.T
    f1 = plt.figure()
    plt.plot(t, peixes,   'r-', label='Peixes')
    plt.plot(t, tubaroes, 'b-', label='Tubaroes')
    plt.grid()
    plt.legend(loc='best')
    plt.xlabel('Tempo')
    plt.ylabel('Populacao')
    plt.title('Evolucao das Populacoes de Tubarao e Peixe')
    f1.savefig('peixes_e_tubaroes_1.png')

# Metodo principal
if __name__ == '__main__':
    # Definicao das constantes
    a = 1.2  # Taxa de crescimento natural dos peixes, quando nao ha nenhum tubarao
    b = 0.3  # Taxa natural de morte dos peixes, devido a caca
    c = 0.3  # Taxa natural de morte dos tubaroes, quando nao ha nenhum peixe
    d = 0.15 # Fator que determina quantos peixes capturados permitem o nascimento de um novo tubarao

    # Definicao do tempo
    # Aqui e criado uma "linha" com valores 100 valores do 0 ate 100, todos com a mesma distancia
    # entre si
    t = np.linspace(0, 100, 100)

    # Condicoes iniciais - 15 peixes e 15 tubaroes
    X0 = np.array([15, 15])

    X, infodict = integrate.odeint(dX_dt, X0, t, full_output=True)
    print(infodict['message'])

    print(len(X))

    populacao_final = X[-1]
    peixes, tubaroes = populacao_final[0], populacao_final[1]

    print(f'Populacao no tempo 100 de peixes {peixes:.2f}')
    print(f'Populacao no tempo 100 de tubaroes {tubaroes:.2f}')

    # Salva o arquivo que mostra a evolucao das especies torno do tempo
    plot_evolucao(X)