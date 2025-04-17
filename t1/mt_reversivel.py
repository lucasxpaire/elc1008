class Transicao:
    def __init__(self, estado_origem, simbolo_lido, simbolo_escrito, direcao, estado_destino):
        self.estado_origem = estado_origem
        self.simbolo_lido = simbolo_lido
        self.simbolo_escrito = simbolo_escrito
        self.direcao = direcao  # 'L' ou 'R'
        self.estado_destino = estado_destino

    def __str__(self):
        return f"({self.estado_origem},{self.simbolo_lido})=({self.estado_destino},{self.simbolo_escrito},{self.direcao})"


class MTReversivel:
    def __init__(self):
        self.estados = []
        self.estado_inicial = None
        self.estado_final = None
        self.alfabeto_entrada = []
        self.alfabeto_fita = []
        self.transicoes = []
        self.fita_input = []
        self.fita_history = ['/']  # Inicia com '/'
        self.fita_output = ['/']   # Inicia com '/'
        self.cabecote_input = 0
        self.cabecote_history = 0
        self.cabecote_output = 0
        self.estado_atual = None
        self.estagio = 1  # 1: execução, 2: cópia, 3: retrace

    def carregar_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

            # Primeira linha: números básicos
            nums = linhas[0].split()
            num_estados = int(nums[0])
            num_simbolos_entrada = int(nums[1])
            num_simbolos_fita = int(nums[2])
            num_transicoes = int(nums[3])

            # Estados
            self.estados = list(map(int, linhas[1].split()))
            self.estado_inicial = self.estados[0]
            self.estado_final = self.estados[-1]
            self.estado_atual = self.estado_inicial

            # Alfabetos
            self.alfabeto_entrada = linhas[2].split()
            self.alfabeto_fita = linhas[3].split()

            # Transições
            for i in range(4, 4 + num_transicoes):
                partes = linhas[i].split('=')
                esq = partes[0].strip('()').split(',')
                dir = partes[1].strip('()').split(',')

                transicao = Transicao(
                    estado_origem=int(esq[0]),
                    simbolo_lido=esq[1],
                    simbolo_escrito=dir[1],
                    direcao=dir[2],
                    estado_destino=int(dir[0])
                )
                self.transicoes.append(transicao)

            # Configuração inicial das fitas
            self.fita_input = list(linhas[-1])  # Última linha é a entrada
            self.cabecote_input = 0

    def passo(self):
        if self.estagio == 1:  # Estágio de execução normal
            # Verificar limites da fita
            if self.cabecote_input < 0:
                self.fita_input.insert(0, 'B')
                self.cabecote_input = 0
            elif self.cabecote_input >= len(self.fita_input):
                self.fita_input.append('B')

            simbolo = self.fita_input[self.cabecote_input]
            
            # Encontrar transição válida
            for trans in self.transicoes:
                if trans.estado_origem == self.estado_atual and trans.simbolo_lido == simbolo:
                    # Executar transição
                    self.fita_input[self.cabecote_input] = trans.simbolo_escrito
                    
                    # Mover cabeçote
                    if trans.direcao == 'R':
                        self.cabecote_input += 1
                    elif trans.direcao == 'L':
                        self.cabecote_input -= 1
                    
                    # Registrar no histórico
                    self.fita_history.append(str(self.estado_atual))
                    self.cabecote_history = len(self.fita_history) - 1
                    
                    # Atualizar estado
                    self.estado_atual = trans.estado_destino
                    
                    # Verificar se chegou ao estado final
                    if self.estado_atual == self.estado_final:
                        self.estagio = 2  # Ir para estágio de cópia
                        self.cabecote_input = 0  # Resetar para começar a cópia
                    
                    return True
            
            return False  # Nenhuma transição encontrada
        
        elif self.estagio == 2:  # Estágio de cópia para output
            # Verificar se já copiamos tudo
            if self.cabecote_input >= len(self.fita_input):
                self.estagio = 3  # Ir para estágio de retrace
                return True
            
            # Copiar símbolo atual (ignorando o '/' inicial)
            if len(self.fita_output) == 1 and self.fita_output[0] == '/':
                self.fita_output.pop()  # Remover o '/' inicial
            
            self.fita_output.append(self.fita_input[self.cabecote_input])
            self.cabecote_input += 1
            self.cabecote_output = len(self.fita_output) - 1
            
            return True
        
        elif self.estagio == 3:  # Estágio de retrace (reversão)
            # Condição de parada: histórico vazio (apenas o '/' inicial)
            if len(self.fita_history) <= 1:
                return False
            
            # Obter último estado do histórico
            estado_anterior = int(self.fita_history[-1])
            
            # Encontrar transição reversa
            transicao_encontrada = None
            for trans in self.transicoes:
                if trans.estado_destino == self.estado_atual and trans.estado_origem == estado_anterior:
                    transicao_encontrada = trans
                    break
            
            if transicao_encontrada:
                # Remover do histórico
                self.fita_history.pop()
                self.cabecote_history = len(self.fita_history) - 1
                
                # Mover cabeçote na direção oposta
                if transicao_encontrada.direcao == 'R':
                    self.cabecote_input -= 1
                elif transicao_encontrada.direcao == 'L':
                    self.cabecote_input += 1
                
                # Atualizar estado
                self.estado_atual = estado_anterior
                
                # Verificar se voltou ao início
                if self.estado_atual == self.estado_inicial:
                    return False
                
                return True
            
            return False  # Nenhuma transição reversa encontrada

    def imprimir_estado(self):
        print("\n=== Estado da MT Reversível ===")
        print(f"Estágio: {self.estagio}")
        print(f"Estado atual: {self.estado_atual}")
        
        print("\nFita Input:")
        print(''.join(self.fita_input))
        print(' ' * self.cabecote_input + '^')
        
        print("\nFita History:")
        print(''.join(self.fita_history))
        print(' ' * self.cabecote_history + '^')
        
        print("\nFita Output:")
        print(''.join(self.fita_output))
        print(' ' * self.cabecote_output + '^')
        print("=============================")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python simulador.py <arquivo_entrada>")
        return
    
    # Criar e configurar a MT
    mt = MTReversivel()
    mt.carregar_arquivo(sys.argv[1])
    
    print("=== Simulação de MT Reversível ===")
    print("Configuração inicial:")
    mt.imprimir_estado()
    
    passo = 1
    while mt.passo():
        input(f"\nPressione Enter para executar o passo {passo}...")
        mt.imprimir_estado()
        passo += 1
    
    print("\nSimulação concluída!")
    print("Estado final:")
    mt.imprimir_estado()


if __name__ == "__main__":
    main()