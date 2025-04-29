class TuringReversivel():
    def _criacao_quadruplas(self, transicoes:list): #dicionarios
        quadruplas = {}
        for estado_atual, simbolo_lido, simbolo_escrito, direcao, novo_estado in transicoes:
            
            if estado_atual not in quadruplas:
                quadruplas[estado_atual] = {} #1,2, 3, 4,5,6 

            estado_intermediario = f"{estado_atual}_{simbolo_lido}" #"1_0", "1_X", "6_$"
            if estado_intermediario not in quadruplas:
                quadruplas[estado_intermediario] = {}

            quadruplas[estado_atual][simbolo_lido] = (simbolo_escrito, '0', estado_intermediario)
            quadruplas[estado_intermediario]['/'] = ('/', direcao, novo_estado)
        return quadruplas

    def _criar_transicoes_retrace(self, transicoes): #1,0->%,R,2  2,%->0,L,1
        quadruplas_retrace = {}
        for estado_atual, simbolo_lido, simbolo_escrito, direcao, novo_estado in transicoes:
            estado_intermediario = f"{estado_atual}_{simbolo_lido}"
            estado_retrace = f"C_{novo_estado}"

            if estado_retrace not in quadruplas_retrace:
                quadruplas_retrace[estado_retrace] = {}
            if f"C_{estado_intermediario}" not in quadruplas_retrace:
                quadruplas_retrace[f"C_{estado_intermediario}"] = {}

            quadruplas_retrace[estado_retrace]['/'] = ('/', self._inverter_direcao(direcao), f"C_{estado_intermediario}")
            quadruplas_retrace[f"C_{estado_intermediario}"][simbolo_escrito] = (simbolo_lido, '0', f"C_{estado_atual}")
        return quadruplas_retrace

    def _inverter_direcao(self, direcao):
        if direcao == 'R':
            return 'L'
        elif direcao == 'L':
            return 'R'
        else:
            return '0' #nem chega a usar

    def __init__(self, estados: list, alfabetoEntrada: list, alfabetoSaidaFita: list, funcoesTransicao: list):
        self.estados = estados
        self.alfabetoEntrada = alfabetoEntrada
        self.alfabetoSaida = alfabetoSaidaFita
        self.funcoesOriginais = funcoesTransicao

        self.dicionarioTransicoes = self._criacao_quadruplas(funcoesTransicao)
        self.dicionarioRetrace = self._criar_transicoes_retrace(funcoesTransicao)
        self.escreve = True

        self.fitaEntrada = str()
        self.fitaHistorico = []
        self.fitaSaida = str()

        self.cabecaEntrada = 0
        self.cabecaHistorico = 0
        self.cabecaSaida = 0

        self.estadoAtual = self.estados[0]
        self.estagio = 1

    def set_entrada(self, palavra:str):
        self.fitaEntrada = palavra


    def mostrar_fitas(self):
        print(f"Fita Entrada   : {self.fitaEntrada})")
        print(f"Fita Historico : {self.fitaHistorico})")
        print(f"Fita Saida     : {self.fitaSaida})")


    def _executar_estagio1(self):
        if self.cabecaEntrada < len(self.fitaEntrada):

            if self.escreve:
                simbolo_lido = self.fitaEntrada[self.cabecaEntrada] #le a fita

                #retorna tripla
                simbolo_escrito, movimento, proximo_estado = self.dicionarioTransicoes[self.estadoAtual][simbolo_lido]
                self._altera_fita_entrada(simbolo_escrito)
                self.escreve = False
            else: #FALSE "1_1"
                simbolo_escrito, movimento, proximo_estado = self.dicionarioTransicoes[self.estadoAtual]['/']
                self._move_cabeca_entrada(movimento)
                self.escreve = True

            # Atualizar fita de histórico:
            self.fitaHistorico.append(self.estadoAtual)


            self.estadoAtual = proximo_estado
            self.cabecaHistorico += 1
        else:
            self.estagio =2 

    def _altera_fita_entrada(self, char):
        fita = list(self.fitaEntrada)
        if self.cabecaEntrada < len(fita):
            fita[self.cabecaEntrada] = char
        else:
            fita.append(char)
        self.fitaEntrada = ''.join(fita)

    def _move_cabeca_entrada(self, movimento):
        if movimento == 'R':
            self.cabecaEntrada += 1
        elif movimento == 'L':
            self.cabecaEntrada -=1

    def _executar_estagio2(self):
        self.fitaSaida = self.fitaEntrada
        # Cabeça precisa ser posicionada no final da entrada para começar o retrace:
        self.cabecaEntrada = len(self.fitaEntrada) - 1
        self.cabecaHistorico = len(self.fitaHistorico) - 1
        self.estagio = 3

    def _executar_estagio3(self):
        if self.cabecaHistorico > 0:
            #"C_1_X", "C_1"
            estado_retrace = f"C_{self.fitaHistorico[self.cabecaHistorico]}" 

            simbolo_lido = self.fitaEntrada[self.cabecaEntrada]
        
            if self.escreve:            

                simbolo_escrito, movimento, proximo_estado = self.dicionarioRetrace[estado_retrace][simbolo_lido]

                self._altera_fita_entrada(simbolo_escrito)
                self.escreve = False
            else:
                simbolo_escrito, movimento, proximo_estado = self.dicionarioRetrace[estado_retrace]['/']
                self._move_cabeca_entrada(movimento)
                self.escreve = True

            self.fitaHistorico.pop(-1)
            self.estadoAtual = proximo_estado
            self.cabecaHistorico -= 1
        else:
            self.estagio = 0
            self.fitaHistorico.pop(-1)

    def executar(self):
        """
        Itera por cada estágio até acabar
        """
        while self.estagio != 0:
            if self.estagio == 1:
                self._executar_estagio1()
            elif self.estagio == 2:
                self._executar_estagio2()
            elif self.estagio == 3:
                self._executar_estagio3()
