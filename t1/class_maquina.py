from class_transicao import Transicao
class Maquina:
    def __init__(self, estados:list, alfabetoEntrada: list, alfabetoSaidaFita: list, funcoesTransicao:list):
        self.estados = estados
        self.alfabetoEntrada = alfabetoEntrada
        self.alfabetoSaidaFita = alfabetoSaidaFita
        self.funcoesTransicao = self.defineFuncoesTransicao(funcoesTransicao)

    def defineFuncoesTransicao(funcoesTransicao):
        #funcoesTransicao -> ["(1,1)=(3,$,R)",""]
        listaTransicoes = list()
        for transicao in funcoesTransicao:
            partes = transicao.split('=')
            condicao = partes[0].strip('()').split(',') #0: estado atual na maquina,1: char lido
            acao = partes[1].strip('()').split(',')     #0: proxEstado, 1: charEscrito, 2: movimentoCabecote

            novaT = Transicao(condicao[0], condicao[1], acao[0], acao[1], acao[2])
            listaTransicoes.append(novaT)

        return listaTransicoes
    
            