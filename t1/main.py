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
turing = Maquina(maquina['estados'], maquina['alfabetoEntrada'], maquina['alfabetoFita'], maquina['funcoesTransicao'])
turing.set_fita_entrada('1100')
print(turing.fitaEntradaESaida)
turing.processamento_main()
print(turing.fitaEntradaESaida)