import threading
import time
import random

CHANCE_DE_NAO_PEDIR = 0.2

# classe para representar a thread do cliente
class Cliente(threading.Thread):
    def __init__ (self, nome, bar):
        threading.Thread.__init__(self)
        # nome do cliente
        self.nome = nome
        # instancia do bar
        self.bar = bar
        # cadeado que evita que um cliente faca pedidos antes de terminar de consumir
        # se set() entao pode pedir
        self.vaiPedir = threading.Event()
        self.vaiPedir.set()

        #cadeado que obriga o cliente a esperar um pedido apos tê-lo feito
        self.pedidoAtendido = threading.Event()

        # cadeado que bloqueia um cliente caso ele ja tenha pedido na rodada
        self.jaBebeu = threading.Event()

    def run(self):
        # tempo aleatorio para chegada do cliente
        time.sleep(random.random() * 2)
        # incrementa a variavel que indica o numero de clientes dentro do bar
        self.bar.adicionaCliente()
        
        print(self.nome + " chegou no bar!!")

        # os pedidos so se iniciam quando o bar esta cheio
        while(not self.bar.cheio()):
            continue
        
        while(self.bar.estaAberto()):
            # se o cliente nao bebeu na rodada e pode pedir
            if (self.vaiPedir.is_set() and not self.jaBebeu.is_set()):
                if(self.bar.estaAberto()):
                    self.fazPedido()
                    self.esperaPedido()
                    self.recebePedido()
                    self.consomePedido()
        
        self.bar.removeCliente()
        print(self.nome + " saindo do bar!")

    def fazPedido(self):
        self.bar.adicionaPedido(self)
        self.bar.setRodadaNaoAumentada()
        print(self.nome + " fez pedido")
        # destranca a variavel vaiPedir
        self.vaiPedir.clear()
        # destranca a variavel de pedido atendido para que possa esperar a entrega
        self.pedidoAtendido.clear()
        # como ja pediu na rodada, ele deve esperar a proxima para pedir,
        # marca que ja bebeu o pedido da rodada
        self.jaBebeu.set()
        time.sleep(1)
    
    def esperaPedido(self):
        print(self.nome + " esperando pedido")
        # o cadeado de pedido atendido impede a thread de continuar ate que o pedido seja entregue
        self.pedidoAtendido.wait()

    def recebePedido(self):
        print(self.nome + " recebeu o pedido")
        time.sleep(1)

    def consomePedido(self):
        print(self.nome + " está consumindo o pedido")
        time.sleep(random.random() * 10)
        print(self.nome + " terminou de consumir seu pedido")
        # ao terminar de consumir o cliente esta apto a pedir
        self.vaiPedir.set()

    def getNome(self):
        return self.nome
    
    def setPedidoAtendido(self):
        self.pedidoAtendido.set()
    
    def clearJaBebeu(self):
        self.jaBebeu.clear()
