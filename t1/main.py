from turingReversivel import TuringReversivel
def ler_arquivo(nome_arquivo):
    """Le o arquivo e retorna as definicoes da maquina e a entrada

    Args:
        nome_arquivo (str): path para o arquivo

    """
    with open(nome_arquivo, "r") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]
    
    estados = linhas[1].split()
    alfabeto_entrada = linhas[2].split()
    alfabeto_fita = linhas[3].split()

    transicoes = []
    for linha in linhas[4:-1]:
        esquerda, direita = linha.split("=")
        estado, simbolo = esquerda.strip("()").split(",")
        novo_estado, novo_simbolo, direcao = direita.strip("()").split(",")

        transicoes.append((
            estado.strip(), simbolo.strip(), novo_simbolo.strip(), direcao.strip(), novo_estado.strip()
        ))

    palavra_entrada = linhas[-1]

    return estados, alfabeto_entrada, alfabeto_fita, transicoes, palavra_entrada


def main():
    #falar dicionario, tuplas e listas
    nome_arquivo = "entrada-quintupla.txt"
    estados, alfabeto_entrada, alfabeto_fita, transicoes, palavra_entrada = ler_arquivo(nome_arquivo)

    maquina = TuringReversivel(estados, alfabeto_entrada, alfabeto_fita, transicoes)

    maquina.set_entrada(palavra_entrada)
    maquina.executar()
    maquina.mostrar_fitas()

if __name__ == "__main__":
    main()
