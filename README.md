# Modelo de Lotka-Volterra

## Sobre o projeto

O objetivo deste projeto é apresentar uma implementação para o modelo de Lotka-Volterra, mostrando a relação entre tubarões e peixes. Este projeto segue o exemplo do [Scipy-Cookbook][scipy-cookbook].

[scipy-cookbook]: https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.html

## Sobre o modelo

Segundo [Wikipedia][wikipedia-lotka-volterra], o matemático Vito Volterra (1860-1940) desenvolveu em 1925 o modelo de equação ao tomar conhecimento do trabalho do zoologista Umberto d’Ancona, que analisou o crescimento da população de tubarões e o decrescimento de populações dos demais peixes em um mar da Itália. O biofísico Alfred J. Lotka (1880-1949), no mesmo ano estudou a interação predador-caça e publicou um livro chamado Elements of Physical Biology, apresentando a mesma modelagem. Por conta da coincidência nas pesquisas, o nome do modelo passou a ser reconhecimento como Lotka-Volterra.
O objetivo deste modelo é compreender a relação entre presa e predador. Ainda segundo o Wikipedia, a equação Lotka-Volterra é formada por um par de equações diferenciais, não lineares e de primeira ordem.

[wikipedia-lotka-volterra]:https://pt.wikipedia.org/wiki/Equa%C3%A7%C3%A3o_de_Lotka-Volterra


## Setup inicial

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução do projeto

```
python main.py
```

