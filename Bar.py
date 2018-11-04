from threading import Semaphore

# representacao do bar
class Bar(object):
    def __init__(self, numeroRodadas, maxNumeroClientes):
        # numero de rodadas passada por parametro
        self.numeroRodadas = numeroRodadas
        # numero de clientes passado por parametro
        self.maxNumeroClientes = maxNumeroClientes
        
        # variavel que impede que dois garcons aumentem a rodada ao mesmo tempo
        self.rodadaAumentada = False
        # numero de clientes presentes no bar
        self.numeroClientes = 0
        
        self.rodadaAtual = 0
        # fila que armazena os clientes que fizeram pedidos
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

    # insere na fila o cliente que fez o pedido
    def adicionaPedido(self, cliente):
        if(self.semaforo.acquire()):
            self.filaPedidos.append(cliente)
            self.semaforo.release()

    # retorna o primeiro pedido da fila para o garcom
    def entregaPedidoProGarcom(self):
        if(self.semaforo.acquire()):
            pedidoDoGarcom = self.filaPedidos.pop(0)
            self.semaforo.release()
        
        return pedidoDoGarcom
    
    def aumentaRodada(self):
        if(self.semaforo.acquire()):
            # se algum garcom ja aumentou a rodada, a rodada nao deve ser aumentada novamente
            # ate que algum cliente faca um pedido
            if(not self.rodadaAumentada):
                self.rodadaAtual += 1
                self.rodadaAumentada = True
                for cliente in self.clientes:
                    # todos os clientes que ja beberam na rodada anterior poderao beber novamente
                    cliente.clearJaBebeu()
                # se o bar ainda estiver aberto, abre uma nova rodada
                if(self.estaAberto()):
                    print("***************RODADA " + str(self.rodadaAtual) + "**********************")
            self.semaforo.release()
    
    # quando um cliente faz um pedido em uma nova rodada, 
    # essa funcao e chamada para que, quando necessario, 
    # a rodada possa ser aumentada pelos garcons
    def setRodadaNaoAumentada(self):
        if(self.semaforo.acquire()):
            if(self.rodadaAumentada):
                self.rodadaAumentada = False
            self.semaforo.release()
    
    def filaEstaVazia(self):
        return (len(self.filaPedidos) == 0)

    def setClientes(self, clientes):
        self.clientes = clientes

    # quando a ultima rodada e terminada destrava-se os cadeados necessários para que os clientes possam sair
    def avisaHorarioFechamento(self):
        for cliente in self.clientes:
            cliente.setPedidoAtendido()
            cliente.clearJaBebeu()