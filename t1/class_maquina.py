class Maquina:
    def __init__(self, estados:list, alfabetoEntrada: list, alfabetoSaidaFita: list, funcoesTransicao:list):
        #Inicialização da máquina
        self.estados = estados
        self.alfabetoEntrada = alfabetoEntrada
        self.alfabetoSaidaFita = alfabetoSaidaFita
        self.dicionarioTransicoes = dict()
        self._define_funcoes_transicao(estados, funcoesTransicao)

        #-------------------
        self.estadoAtual = self.estados[0] #primeiro item da lista sempre é o primeiro estado da maquina
        self.posicaoCabecote = 0
        self.fitaEntradaESaida = str()  
        self.historicoFita = list()
        self.fitaCopiaFinal = str()
        self.faseAtual = 1

    def _define_funcoes_transicao(self, estados: list, funcoesTransicao:list)->list:
        """Cria as funções de transição descritas na entrada 
        Args:
            funcoesTransicao (list): Lista de strings com o padrão (1,1)=(3,$,R)
        Returns:
            list: lista de Transicao
        """
        #funcoesTransicao -> ["(1,1)=(3,$,R)",""]
        for estado in estados:
            self.dicionarioTransicoes[str(estado)] = dict() 

        for transicao in funcoesTransicao:
            partes = transicao.split('=')
            condicao = partes[0].strip('()').split(',')   #0: estado atual na maquina,1: char lido
            tripla = partes[1].strip('()').split(',')     #0: proxEstado, 1: charEscrito, 2: movimentoCabecote
            dicionarioUm = self.dicionarioTransicoes[str(condicao[0])]
            dicionarioUm[condicao[1]] = tripla

    def set_fita_entrada(self, fita: str):
        self.fitaEntradaESaida = fita
        self.historicoFita.append(fita)

    def escreve_fita(self, char:str):
        # self.fitaEntradaESaida
        temp = list(self.fitaEntradaESaida)
        temp[self.posicaoCabecote] = char
        temp = "".join(temp)
        self.set_fita_entrada(temp)

    def move_cabecote(self, dirEsq):
        if dirEsq == 'R':
            self.posicaoCabecote=self.posicaoCabecote+1
        elif dirEsq == 'L':
            self.posicaoCabecote=self.posicaoCabecote-1

    def processamento_main(self): #add proximas fases aqui!!
        self._computacao_direta()



    def _computacao_direta(self, ):
        while self.posicaoCabecote < len(self.fitaEntradaESaida):
            charLido = self.fitaEntradaESaida[self.posicaoCabecote]
            tripla = self.dicionarioTransicoes[self.estadoAtual][charLido]
            self.estadoAtual = tripla[0]
            self.escreve_fita(tripla[1])
            self.move_cabecote(tripla[2])
        self.faseAtual=2