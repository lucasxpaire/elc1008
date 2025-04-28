from class_maquina import Maquina

def le_arquivo(path):
    with open(path, "r") as f:
        linhas = [linha.strip() for linha in f.readlines()]

        definicaoMaquina = {
            "estados": linhas[1].split(),
            "alfabetoEntrada": linhas[2].split(),
            "alfabetoFita": linhas[3].split(),
            "funcoesTransicao": linhas[4:-1]
        }
        return definicaoMaquina

if __name__ == "__main__":
    definicoes = le_arquivo("entrada-quintupla.txt")

    turing = Maquina(
        definicoes['estados'],
        definicoes['alfabetoEntrada'],
        definicoes['alfabetoFita'],
        definicoes['funcoesTransicao']
    )

    # Definir a fita de entrada com um exemplo, conforme o arquivo de entrada
    fitaInicial = '1100'  # Exemplo de entrada para a máquina
    turing.set_fita_entrada(fitaInicial)

    # Processar a máquina de Turing reversível
    turing.processamento_main()

    # Mostrar o estado das três fitas após a execução
    turing.mostrar_fitas()
