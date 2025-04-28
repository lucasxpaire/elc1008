class Maquina:
    def __init__(self, estados: list, alfabetoEntrada: list, alfabetoSaidaFita: list, funcoesTransicao: list):
        self.estados = estados
        self.alfabetoEntrada = alfabetoEntrada
        self.alfabetoSaidaFita = alfabetoSaidaFita
        self.dicionarioTransicoes = dict()
        self._define_funcoes_transicao(estados, funcoesTransicao)

        self.fitaEntrada = str()    #fita 1
        self.fitaHistorico = str()  #fita 2
        self.fitaSaida = str()      #fita 3

        #Cabecotes
        self.cabecaEntrada = 0
        self.cabecaHistorico = 0
        self.cabecaSaida = 0

        self.estadoAtual = self.estados[0]
        self.historicoTransicoes = []

    def _define_funcoes_transicao(self, estados: list, funcoesTransicao: list):
        """Cria funções de transição descritas na entrada"""
        for estado in estados:
            self.dicionarioTransicoes[str(estado)] = dict()

        for transicao in funcoesTransicao:
            partes = transicao.split('=')
            condicao = partes[0].strip('()').split(',')# Ex: (1,1) -> estado, símbolo lido
            tripla = partes[1].strip('()').split(',') # Ex: (3,$,R) -> próximo estado, símbolo escrito, movimento
            self.dicionarioTransicoes[str(condicao[0])][condicao[1]] = tripla

    def set_fita_entrada(self, fita: str):
        self.fitaEntrada = list(fita)
        self.fitaHistorico = ['/' for _ in range(len(fita))]
        self.fitaSaida = ['/' for _ in range(len(fita))]

    def escreve_na_fita(self, fita, posicao, char):
        fita_lista = list(fita)
        while posicao >= len(fita_lista):
            fita_lista.append('_')
        fita_lista[posicao] = char  
        return ''.join(fita_lista)  
    
    def move_cabecote(self, movimento: str, fita: str):
        if movimento == 'R':
            if fita == 'entrada':
                self.cabecaEntrada += 1
            elif fita == 'historico':
                self.cabecaHistorico += 1
            elif fita == 'saida':
                self.cabecaSaida += 1


        elif movimento == 'L':
            if fita == 'entrada':
                self.cabecaEntrada -= 1
            elif fita == 'historico':
                self.cabecaHistorico -= 1
            elif fita == 'saida':
                self.cabecaSaida -= 1

    def _garante_espaco_na_fita(self, fita, posicao):
        while posicao >= len(fita):
            fita += '_'  # Adiciona espaços em branco
        return fita

    def processamento_main(self):
        self._computacao_direta()
        self._copiar_saida()
        self._retrace()

    def _computacao_direta(self):
        while self.cabecaEntrada < len(self.fitaEntrada):
            charLido = self.fitaEntrada[self.cabecaEntrada]
            tripla = self.dicionarioTransicoes[self.estadoAtual][charLido]

            # Guarda histórico
            self.historicoTransicoes.append({
                "estadoAnterior": self.estadoAtual,
                "cabecaEntradaAnterior": self.cabecaEntrada,
                "simboloentradaAnterior": charLido,
                "simbolohistoricoAnterior": self.fitaHistorico[self.cabecaHistorico]
            })

            self.estadoAtual = tripla[0]
            self.fitaEntrada = self.escreve_na_fita(self.fitaEntrada, self.cabecaEntrada, tripla[1])
            self.fitaHistorico = self.escreve_na_fita(self.fitaHistorico, self.cabecaHistorico, charLido)

            self.move_cabecote(tripla[2], 'entrada')
            self.move_cabecote(tripla[2], 'historico')

    def _copiar_saida(self):
        self.estadoAtual = 'B0'
        self.cabecaEntrada = 0
        self.cabecaSaida = 0

        while self.cabecaEntrada < len(self.fitaEntrada):
            simbolo = self.fitaEntrada[self.cabecaEntrada]

            self.fitaSaida = self.escreve_na_fita(self.fitaSaida, self.cabecaSaida, simbolo)

            self.move_cabecote('R', 'entrada')
            self.move_cabecote('R', 'saida')

    def _retrace(self):
        self.estadoAtual = self.estados[-1]  # Começa do estado final
        for transicao in reversed(self.historicoTransicoes):
            self.estadoAtual = transicao["estadoAnterior"]
            self.cabecaEntrada = transicao["cabecaEntradaAnterior"]
            self.fitaEntrada = self.escreve_na_fita(self.fitaEntrada, self.cabecaEntrada, transicao["simboloentradaAnterior"])
            self.fitaHistorico = self.escreve_na_fita(self.fitaHistorico, self.cabecaHistorico, transicao["simbolohistoricoAnterior"])

    def mostrar_fitas(self):
        print(f"Fita entrada: {self.fitaEntrada}")
        print(f"Fita historico: {self.fitaHistorico}")
        print(f"Fita saida: {self.fitaSaida}")
