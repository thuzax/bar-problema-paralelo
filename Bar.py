from threading import Semaphore

class Bar(object):
    def __init__(self, numeroRodadas, maxNumeroClientes):
        # self.clientes = clientes
        # self.garcons = garcons
        self.rodadaAumentada = False
        self.numeroRodadas = numeroRodadas
        self.numeroClientes = 0
        self.maxNumeroClientes = maxNumeroClientes
        self.rodadaAtual = 0
        self.filaPedidos = []
        self.semaforo = Semaphore()
        print("***************RODADA " + str(self.rodadaAtual) + "**********************")

    def estaAberto(self):
        return (self.rodadaAtual < self.numeroRodadas)

    def cheio(self):
        return (self.numeroClientes >= self.maxNumeroClientes)

    def vazio(self):
        return (self.numeroClientes == 0)

    def adicionaCliente(self):
        if(self.semaforo.acquire):
            self.numeroClientes += 1
            self.semaforo.release()

    def removeCliente(self):
        if(self.semaforo.acquire):
            self.numeroClientes -= 1
            self.semaforo.release()


    def adicionaPedido(self, cliente):
        if(self.semaforo.acquire()):
            self.filaPedidos.append(cliente)
            self.semaforo.release()

    def entregaPedidoProGarcom(self):
        if(self.semaforo.acquire()):
            pedidoDoGarcom = self.filaPedidos.pop(0)
            self.semaforo.release()
        
        return pedidoDoGarcom
    
    def aumentaRodada(self):
        if(self.semaforo.acquire()):
            if(not self.rodadaAumentada):
                self.rodadaAtual += 1
                self.rodadaAumentada = True
                for cliente in self.clientes:
                    cliente.clearJaBebeu()
                if(self.estaAberto()):
                    print("***************RODADA " + str(self.rodadaAtual) + "**********************")
            self.semaforo.release()
    
    def setRodadaNaoAumentada(self):
        if(self.semaforo.acquire()):
            if(self.rodadaAumentada):
                self.rodadaAumentada = False
            self.semaforo.release()
    
    def filaEstaVazia(self):
        return (len(self.filaPedidos) == 0)

    def setClientes(self, clientes):
        self.clientes = clientes

    def avisaHorarioFechamento(self):
        for cliente in self.clientes:
            cliente.setPedidoAtendido()
            cliente.clearJaBebeu()