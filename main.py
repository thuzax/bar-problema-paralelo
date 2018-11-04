import sys
from Cliente import Cliente
from Garcom import Garcom
from Bar import Bar

def main():
    if len(sys.argv) < 5:
        print("Quantidade inválida de argumentos. São necessários 4 argumentos")
        return
    
    numeroClientes = int(sys.argv[1])
    numeroGarcons = int(sys.argv[2])
    capacidadeGarcons = int(sys.argv[3])
    numeroRodadas = int(sys.argv[4])

    clientes = []
    garcons = []

    print(numeroClientes)
    print(numeroGarcons)
    print(capacidadeGarcons)
    print(numeroRodadas)

    # inicializa a instancia de bar
    bar = Bar(numeroRodadas, numeroClientes)

    # cria os clientes
    for i in range(numeroClientes):
        clientes.append(Cliente("cliente"+str(i), bar))

    bar.setClientes(clientes)

    # cria os garcons
    for i in range(numeroGarcons):
        garcons.append(Garcom("garcom"+str(i), capacidadeGarcons, bar))

    # comeca a execucao das threads dos garcons
    for garcom in garcons:
        garcom.start()
    # comeca a execucao das threads dos clientes
    for cliente in clientes:
        cliente.start()

main()
    