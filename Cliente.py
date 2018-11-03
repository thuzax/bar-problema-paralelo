import threading
import time
import random

CHANCE_DE_NAO_PEDIR = 0.2

class Cliente(threading.Thread):
    def __init__ (self, nome, bar):
        threading.Thread.__init__(self)
        self.nome = nome
        self.vaiPedir = threading.Event()
        self.vaiPedir.set()
        self.pedidoAtendido = threading.Event()
        self.jaBebeu = threading.Event()
        self.bar = bar

    def run(self):
        time.sleep(random.random() * 2)
        self.bar.adicionaCliente()
        print(self.nome + " chegou no bar!!")
        while(not self.bar.cheio()):
            continue
        
        while(self.bar.estaAberto()):
            if (self.vaiPedir.is_set() and not self.jaBebeu.is_set()):
                if(self.bar.estaAberto()):
                    self.fazPedido()
                    self.esperaPedido()
                    self.recebePedido()
                    self.consomePedido()
        
        self.bar.removeCliente()

    def fazPedido(self):
        self.bar.adicionaPedido(self)
        self.bar.setRodadaNaoAumentada()
        print(self.nome + " fez pedido")
        self.vaiPedir.clear()
        self.pedidoAtendido.clear()
        time.sleep(1)
    
    def esperaPedido(self):
        print(self.nome + " esperando pedido")
        self.pedidoAtendido.wait()

    def recebePedido(self):
        time.sleep(1)
        print(self.nome + " recebeu o pedido")

    def consomePedido(self):
        print(self.nome + " está consumindo o pedido")
        time.sleep(random.random() * 10)
        print(self.nome + " terminou de consumir seu pedido")
        self.vaiPedir.set()
        self.jaBebeu.set()
        time.sleep(1)

    def getNome(self):
        return self.nome
    
    def setPedidoAtendido(self):
        self.pedidoAtendido.set()
    
    def clearJaBebeu(self):
        # print(self.jaBebeu.is_set())
        self.jaBebeu.clear()
        # print(self.jaBebeu.is_set())