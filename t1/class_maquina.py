class Maquina:
    def __init__(self, estados: list, alfabetoEntrada: list, alfabetoSaidaFita: list, funcoesTransicao: list):
        self.estados = estados
        self.alfabetoEntrada = alfabetoEntrada
        self.alfabetoSaidaFita = alfabetoSaidaFita
        self.dicionarioTransicoes = dict()
        self._define_funcoes_transicao(estados, funcoesTransicao)

        # Inicializando as três fitas
        self.fitaEntrada = ""   # fita 1
        self.fitaHistorico = "" # fita 2
        self.fitaSaida = ""  # fita 3

        # Cabeçotes para cada fita
        self.cabecaEntrada = 0
        self.cabecaHistorico = 0
        self.cabecaSaida = 0

        # Estado atual da máquina
        self.estadoAtual = self.estados[0]  # Primeiro estado é o inicial
        self.historicoTransicoes = []

    def _define_funcoes_transicao(self, estados: list, funcoesTransicao: list):
        """Cria funções de transição descritas na entrada"""
        for estado in estados:
            self.dicionarioTransicoes[str(estado)] = dict()

        for transicao in funcoesTransicao:
            partes = transicao.split('=')
            condicao = partes[0].strip('()').split(',')  # Ex: (1,1) -> estado, símbolo lido
            tripla = partes[1].strip('()').split(',')     # Ex: (3,$,R) -> próximo estado, símbolo escrito, movimento
            self.dicionarioTransicoes[str(condicao[0])][condicao[1]] = tripla

    def set_fita_entrada(self, fita: str):
        self.fitaEntrada = fita
        self.fitaEntrada = list(self.fitaEntrada)  # para facilitar alteração
        self.fitaHistorico = ['/' for _ in range(len(fita))]
        self.fitaSaida = ['/' for _ in range(len(fita))]

    def escreve_na_fita(self, fita, posicao, char):
        fita_lista = list(fita)  # Converte a fita para lista
        while posicao >= len(fita_lista):
            fita_lista.append('_')  # Adiciona espaços em branco até atingir a posição necessária
        fita_lista[posicao] = char  # Agora é seguro escrever na posição
        return ''.join(fita_lista)  # Converte de volta para string

    def move_cabecote(self, movimento: str, fita: str):
        if movimento == 'R':
            if fita == 'input':
                self.cabecaEntrada += 1
            elif fita == 'history':
                self.cabecaHistorico += 1
            elif fita == 'output':
                self.cabecaSaida += 1
        elif movimento == 'L':
            if fita == 'input':
                self.cabecaEntrada -= 1
            elif fita == 'history':
                self.cabecaHistorico -= 1
            elif fita == 'output':
                self.cabecaSaida -= 1

    def _garante_espaco_na_fita(self, fita, posicao):
        while posicao >= len(fita):
            fita += '_'  # Adiciona espaços em branco (ou qualquer outro símbolo para espaço) na fita
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
                "simboloInputAnterior": charLido,
                "simboloHistoryAnterior": self.fitaHistorico[self.cabecaHistorico]
            })

            # Atualiza estado
            self.estadoAtual = tripla[0]

            # Escreve símbolo na fita de entrada
            self.fitaEntrada = self.escreve_na_fita(self.fitaEntrada, self.cabecaEntrada, tripla[1])

            # Registra movimento na fita de história (grava o símbolo anterior)
            self.fitaHistorico = self.escreve_na_fita(self.fitaHistorico, self.cabecaHistorico, charLido)

            # Move cabeçotes
            self.move_cabecote(tripla[2], 'input')
            self.move_cabecote(tripla[2], 'history')

    def _copiar_saida(self):
        # Cria novos estados Bs para copiar input para output
        self.estadoAtual = 'B0'
        self.cabecaEntrada = 0
        self.cabecaSaida = 0

        while self.cabecaEntrada < len(self.fitaEntrada):
            simbolo = self.fitaEntrada[self.cabecaEntrada]

            # Copia símbolo da fita input para a output
            self.fitaSaida = self.escreve_na_fita(self.fitaSaida, self.cabecaSaida, simbolo)

            # Move apenas input e output (history parado)
            self.move_cabecote('R', 'input')
            self.move_cabecote('R', 'output')

    def _retrace(self):
        # Inverte as transições
        self.estadoAtual = self.estados[-1]  # Começa do estado final
        for transicao in reversed(self.historicoTransicoes):
            # A transição inversa envolve a troca do estado e do símbolo lido
            self.estadoAtual = transicao["estadoAnterior"]
            self.cabecaEntrada = transicao["cabecaEntradaAnterior"]
            self.fitaEntrada = self.escreve_na_fita(self.fitaEntrada, self.cabecaEntrada, transicao["simboloInputAnterior"])
            self.fitaHistorico = self.escreve_na_fita(self.fitaHistorico, self.cabecaHistorico, transicao["simboloHistoryAnterior"])

            # Move os cabeçotes para o movimento inverso
            # Aqui, você pode precisar de mais lógica para lidar com o movimento da fita de entrada e histórico de forma reversa

    def mostrar_fitas(self):
        print("Fita Input: ", "".join(self.fitaEntrada))
        print("Fita History: ", "".join(self.fitaHistorico))
        print("Fita Output: ", "".join(self.fitaSaida))
