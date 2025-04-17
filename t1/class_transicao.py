class Transicao:
    def __init__(self, estadoAtual: int, charLido: str, proxEstado: int, charEscrito: str, movimentoCabecote: int):
        self.estadoAtual = estadoAtual
        self.charLido = charLido
        self.proxTransicao = proxEstado
        self.charEscrito = charEscrito
        self.movimentoCabeco = movimentoCabecote #cabecote += movimentoCabecote 1 ou -1 