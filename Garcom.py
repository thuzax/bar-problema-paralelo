import threading
import time
import random

# classe que representa a thread garcom
class Garcom(threading.Thread):
    def __init__ (self, nome, capacidade, bar):
        threading.Thread.__init__(self)
        # nome do garcom
        self.nome = nome
        # capacidade de atendimento passado por parametro
        self.capacidade = capacidade
        # instancia do bar
        self.bar = bar
    
    def run(self):
        # espera o bar encher para comecar o atendimento
        while(not self.bar.cheio()):
            continue
        print(self.nome + " comecou a trabalhar")
        # enquanto houver clientes no bar
        while(not self.bar.vazio()):
            # se o bar fechou, deve avisar aos clientes para que eles saiam
            if(not self.bar.estaAberto()):
                self.bar.avisaHorarioFechamento()
            else:
                pedidos = self.recebePedidos()
                self.registraPedidos(pedidos)
                self.entregaPedidos(pedidos)
                # se, apos entregar os pedidos, a fila estiver vazia,
                # significa que nao ha mais ninguem para pedir nessa rodada
                # e a rodada deve ser aumentada
                if(self.bar.filaEstaVazia()):
                    self.bar.aumentaRodada()
                


    def recebePedidos(self):
        print(self.nome + " recebendo pedidos")
        pedidos = []
        # enquanto a capacidade de atendimento nao for alcancada 
        # e a fila de pedidos nao estiver vazia
        while(len(pedidos) < self.capacidade and not self.bar.filaEstaVazia()):
            # pega o pedido do cliente
            pedidos.append(self.bar.entregaPedidoProGarcom())
            time.sleep(((random.random() * 10) % 3) / 10)

        return pedidos
    
    def registraPedidos(self, pedidos):
        print(self.nome + " registrando pedidos")
        time.sleep(random.random() * 3)

    def entregaPedidos(self, pedidos):
        # entrega os pedidos para todos os clientes que pediram
        for cliente in pedidos:
            print(self.nome + " entregando pedido para " + cliente.getNome())
            time.sleep(random.random() * 10)
            cliente.setPedidoAtendido()