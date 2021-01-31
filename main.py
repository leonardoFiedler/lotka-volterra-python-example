import numpy as np
import pylab as p
from scipy import integrate
from matplotlib import pyplot as plt

# Parametros do modelo
# u = Numero de presas (Neste exemplo representara os peixes).
# v = Numero de predadores (Neste exemplo representara os tubaroes).

# Definicao das constantes
a = 1.0  # Taxa de crescimento natural dos peixes, quando nao ha nenhum tubarao
b = 0.1  # Taxa natural de morte dos peixes, devido a caca
c = 1.5  # Taxa natural de crescimento dos tubaroes, quando nao ha nenhum peixe
d = 0.75 # Fator que determina quantos peixes capturados permitem o nascimento de um novo tubarao

def dX_dt(X, t=0):
    """
        Retorna a taxa de crescimento para as populacoes de tubaroes e peixes.
    """
    u, v = X[0], X[1]
    return np.array([
        a * u - b * u * v, 
        -c * v + d * b * u * v
    ])

def d2X_dt2(X, t=0):
    """
    Estabilidade de pontos fixados
    Proximo desses dois pontos, o sistema pode ser linearizado: dX_dt = A_f*X
    onde A representa a matriz Jacobian executada no ponto correspondente.
    Esta funcao retorna a matriz Jacobian, executada pelo parametro X.
    """
    u, v = X[0], X[1]
    return np.array([
        [a - b * v, -b * u],
        [b * d * v, -c + b * d * u]
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

def plot_trajetoria_direcional(X_f1):
    """
    Esta funcao plota algumas trajetorias no plano para diferentes pontos 
    iniciados em X_f0 e X_f1. Utiliza o mapa de cores para definir a trajetoria
    """
    # Posicoes de X0 entre X_f0 e X_f1
    values = np.linspace(0.3, 0.9, 5)

    # Cor de cada uma das trajetorias
    vcolors = plt.cm.autumn_r(np.linspace(0.3, 1., len(values)))

    f2 = plt.figure()
    # Plot da trajetoria
    for v, col in zip(values, vcolors):
        # ponto de inicio
        X0 = v * X_f1
        X = integrate.odeint(dX_dt, X0, t)
        plt.plot(X[:,0], X[:,1], lw=3.5*v, color=col, label='X0=(%.f, %.f)' % ( X0[0], X0[1]) )

    # Define a grade e computa a direcao para cada ponto
    # Limites das axis
    ymax = plt.ylim(ymin=0)[1]
    xmax = plt.xlim(xmin=0)[1]
    nb_points = 20

    x = np.linspace(0, xmax, nb_points)
    y = np.linspace(0, ymax, nb_points)

    X1 , Y1  = np.meshgrid(x, y)                       # create a grid
    DX1, DY1 = dX_dt([X1, Y1])                      # compute growth rate on the gridt
    M = (np.hypot(DX1, DY1))                           # Norm of the growth rate 
    M[ M == 0] = 1.                                 # Avoid zero division errors 
    DX1 /= M                                        # Normalize each arrows
    DY1 /= M

    plt.title('Trajetorias e Campos de Direcao')
    Q = plt.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=plt.cm.jet)
    plt.xlabel('Numero de Peixes')
    plt.ylabel('Numero de Tubaroes')
    plt.legend()
    plt.grid()
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    f2.savefig('peixes_e_tubaroes_2.png')
    return xmax, ymax

def IF(X):
    u, v = X
    return u**(c/a) * v * np.exp( -(b/a)*(d*u+v) )

def plot_contornos(X_f1, xmax, ymax):
    values  = np.linspace(0.3, 0.9, 5)

    for v in values:
        X0 = v * X_f1                               # starting point
        X = integrate.odeint( dX_dt, X0, t)
        I = IF(X.T)                                 # compute IF along the trajectory
        I_mean = I.mean()
        delta = 100 * (I.max()-I.min())/I_mean
        print('X0=(%2.f,%2.f) => I ~ %.1f |delta = %.3G %%' % (X0[0], X0[1], I_mean, delta))

    nb_points = 80                              # grid size
    x = np.linspace(0, xmax, nb_points)
    y = np.linspace(0, ymax, nb_points)
    X2 , Y2  = np.meshgrid(x, y)                   # create the grid
    Z2 = IF([X2, Y2])                           # compute IF on each point
    f3 = plt.figure()
    CS = plt.contourf(X2, Y2, Z2, cmap=plt.cm.Purples_r, alpha=0.5)
    CS2 = plt.contour(X2, Y2, Z2, colors='black', linewidths=2. )
    plt.clabel(CS2, inline=1, fontsize=16, fmt='%.f')
    plt.grid()
    plt.xlabel('Number of rabbits')
    plt.ylabel('Number of foxes')
    plt.ylim(1, ymax)
    plt.xlim(1, xmax)
    plt.title('IF contours')
    f3.savefig('peixes_e_tubaroes_3.png')

# Metodo principal
if __name__ == '__main__':
    """
    Equilibro populacional
    O equilibrio populacional ocorre quando a taxa de crescimento e igual a 0. 
    Isto gera dois pontos fixos.
    """

    X_f0 = np.array([0., 0.])
    X_f1 = np.array([c/(d*b), a/b])

    # Resultado deve ser True - o que significa que ambas as populacoes estao em equilibrio
    print(all(dX_dt(X_f0) == np.zeros(2)) and all(dX_dt(X_f1) == np.zeros(2)))

    # Proximo do X_f0, que representa a extincao de ambas as especies, teremos:
    A_f0 = d2X_dt2(X_f0)
    print(A_f0)

    """
    Proximo do X_f0, o numero de peixes aumenta e a populacao de tubaroes diminui. 
    Isto origina um ponto de cela
    Pontos de cela sao pontos no grafico de uma funcao onde as derivadas na direcao
    ortogonal sao todas zero (ponto critico).
    Em outras palavras, as direcoes x e y discordam sobre se essa entrada deve ser um ponto
    de maximo ou de minimo.
    https://pt.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/optimizing-multivariable-functions/a/maximums-minimums-and-saddle-points

    Proximo de X_f1 temos
    """

    A_f1 = d2X_dt2(X_f1)
    print(A_f1)

    """
    Integrando com o ODE usando a funcao integrate do scipy
    """

    # Definicao do tempo
    t = np.linspace(0, 15, 1000)

    # Condicoes iniciais - 10 peixes e 5 tubaroes
    X0 = np.array([10, 5])

    X, infodict = integrate.odeint(dX_dt, X0, t, full_output=True)
    print(infodict['message'])

    plot_evolucao(X)
    xmax, ymax = plot_trajetoria_direcional(X_f1)
    plot_contornos(X_f1, xmax, ymax)

    
    
    
