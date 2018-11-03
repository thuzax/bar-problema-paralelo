import threading
import time
import random

class Garcom(threading.Thread):
    def __init__ (self, nome, capacidade, bar):
        threading.Thread.__init__(self)
        self.nome = nome
        self.capacidade = capacidade
        self.numeroPedidosAtual = 0
        self.temCliente = True
        self.bar = bar
    
    def run(self):
        while(not self.bar.cheio()):
            continue
        print(self.nome + " comecou a trabalhar")
        while(not self.bar.vazio()):
            if(not self.bar.estaAberto()):
                self.bar.avisaHorarioFechamento()
            else:
                pedidos = self.recebePedidos()
                print("SAIU", len(pedidos), self.capacidade)
                self.registraPedidos(pedidos)
                self.entregaPedidos(pedidos)
                if(self.bar.filaEstaVazia()):
                    self.bar.aumentaRodada()
                


            

    def recebePedidos(self):
        print(self.nome + " recebendo pedidos")
        time.sleep(1)
        pedidos = []
        while(len(pedidos) < self.capacidade and not self.bar.filaEstaVazia()):
            pedidos.append(self.bar.entregaPedidoProGarcom())
        return pedidos
    
    def registraPedidos(self, pedidos):
        print(self.nome + " registrando pedidos")
        time.sleep(1)
        time.sleep(random.random() * 10)

    def entregaPedidos(self, pedidos):
        for cliente in pedidos:
            print(self.nome + " entregando pedido para " + cliente.getNome())
            time.sleep(1)
            time.sleep(random.random() * 10)
            cliente.setPedidoAtendido()

    def atingiuMaxPedidos(self):
        return (self.numeroPedidosAtual >= self.capacidade)
