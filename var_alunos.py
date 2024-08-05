import foosball_alunos

def le_replay(nome_ficheiro):
    bola = [] 
    jogador_vermelho = []
    jogador_azul = []
    
    try:
        with open(nome_ficheiro, 'r') as file:
            linha = file.read().split('\n')

        for i in range(3):
            pos = linha[i].split(';')
            for j in pos:
                aux = j.split(',')
                nova_pos = tuple([float(aux[0]), float(aux[1])])

                if i == 0:
                    bola.append(nova_pos)
                elif i == 1:
                    jogador_vermelho.append(nova_pos)
                elif i == 2:
                    jogador_azul.append(nova_pos)
                    
        resultado = {
            'bola': bola,
            'jogador_vermelho': jogador_vermelho,
            'jogador_azul': jogador_azul
        }        
        
        return resultado
    
    except FileNotFoundError:
            return "Ficheiro não existe"    

    except Exception as e:
        return f"Erro ao abrir o ficheiro: {e}"


def main():
    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
    replay = le_replay('replay_golo_jv_0_ja_1.txt')
    estado_jogo['jogador_vermelho'].penup()
    estado_jogo['jogador_azul'].penup()
    for i in range(len(replay['bola'])):
        estado_jogo['janela'].update()
        estado_jogo['jogador_vermelho'].setpos(replay['jogador_vermelho'][i])
        estado_jogo['jogador_azul'].setpos(replay['jogador_azul'][i])
        estado_jogo['bola']['bola'].setpos(replay['bola'][i])
    estado_jogo['janela'].exitonclick()


if __name__ == '__main__':
    main()