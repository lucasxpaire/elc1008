from class_maquina import Maquina

def le_arquivo(path):
    with open(path, "r") as f:
        linhas = [linha.strip() for linha in f.readlines()]

        definicaoMaquina = {
            "estados": linhas[1].split(),
            "alfabetoEntrada": linhas[2].split(),
            "alfabetoFita": linhas[3].split(),
            "funcoesTransicao": linhas[4:-1],
            "fitaEntrada": linhas[-1]
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

    fitaInicial = definicoes['fitaEntrada'] 
    turing.set_fita_entrada(fitaInicial)

    turing.processamento_main()

    turing.mostrar_fitas()
