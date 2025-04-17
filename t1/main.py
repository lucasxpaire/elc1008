from class_maquina import Maquina

def le_arquivo(path):
    with open(path, "r") as f:
        linhas = [linha.strip() for linha in f.readlines()]

        definicaoMaquina = {
            "estados":linhas[1].split(),
            "alfabetoEntrada":linhas[2].split(),
            "alfabetoFita":linhas[3].split(),
            "funcoesTransicao":linhas[4:-1]
        }
        return definicaoMaquina

maquina = le_arquivo("entrada-quintupla.txt")
Maquina(maquina['estados'], maquina['alfabetoEntrada'], maquina['alfabetoFita'], maquina['funcoesTransicao'])