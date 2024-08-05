import turtle as t
import functools
import random
import math
import time
import csv
import os

LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO = 90
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO = LADO_MAIOR_AREA / 4
START_POS_BALIZAS = ALTURA_JANELA / 4
BOLA_START_POS = (5,5)


# Funções responsáveis pelo movimento dos jogadores no ambiente. 
# O número de unidades que o jogador se pode movimentar é definida pela constante 
# PIXEIS_MOVIMENTO. As funções recebem um dicionário que contém o estado 
# do jogo e o jogador que se está a movimentar. 

def jogador_cima(estado_jogo, jogador):
    mover_jogador(estado_jogo, jogador, 0, PIXEIS_MOVIMENTO)

def jogador_baixo(estado_jogo, jogador):
    mover_jogador(estado_jogo, jogador, 0, -PIXEIS_MOVIMENTO)

def jogador_direita(estado_jogo, jogador):
    mover_jogador(estado_jogo, jogador, PIXEIS_MOVIMENTO, 0)

def jogador_esquerda(estado_jogo, jogador):
    mover_jogador(estado_jogo, jogador, -PIXEIS_MOVIMENTO, 0)

def mover_jogador(estado_jogo, jogador, delta_x, delta_y):
    
    jogador_turtle = estado_jogo[jogador]
    
    x, y = jogador_turtle.position()

    if (-LARGURA_JANELA / 2 < x + delta_x < LARGURA_JANELA / 2 and -ALTURA_JANELA / 2 < y + delta_y < ALTURA_JANELA / 2):    
        move(x + delta_x,y + delta_y,jogador_turtle)

def move(corX,corY,turt):
    turt.penup()
    turt.goto(corX,corY)
    turt.pendown()
    
def desenha_balizas(corX,corY,turt):
    j = 1
    for i in range(2):
        move(j*corX,j*corY,turt)
        for k in range(2):
            t.fd(LADO_MENOR_AREA)
            t.left(90)
            t.fd(LADO_MAIOR_AREA)
            t.left(90)  
            
        t.setheading(180)
        j = -1
        

def desenha_linhas_campo():
    ''' Função responsável por desenhar as linhas do campo, 
    nomeadamente a linha de meio campo, o círculo central, e as balizas. '''
    
    t.color('white')
    t.pensize(8)
    t.left(90)
    move(0,-ALTURA_JANELA/2,t)
    t.fd(ALTURA_JANELA)
    t.home()
    move(0,-2*RAIO_MEIO_CAMPO,t)
    t.circle(2*RAIO_MEIO_CAMPO)
    
    desenha_balizas(-LARGURA_JANELA/2,-LADO_MAIOR_AREA/2,t)
    t.hideturtle()
    

def criar_bola():
    '''
    Função responsável pela criação da bola. 
    Deverá considerar que esta tem uma forma redonda, é de cor preta, 
    começa na posição BOLA_START_POS com uma direção aleatória. 
    Deverá ter em conta que a velocidade da bola deverá ser superior à dos jogadores. 
    A função deverá devolver um dicionário contendo 4 elementos: o objeto bola, 
    a sua direção no eixo dos xx, a sua direção no eixo dos yy, 
    e um elemento inicialmente a None que corresponde à posição anterior da mesma.
    '''

    t_bola = t.Turtle()
    
    t_bola.shape("circle")
    t_bola.color("black")
    t_bola.penup()

    t_bola.goto(BOLA_START_POS)
    
    t_bola.goto(-1.2,0)

    dir_x = random.uniform(-1, 1)  
    dir_y = random.uniform(-1, 1)

    bola_info = {
        'bola': t_bola,
        'dir_x': dir_x,
        'dir_y': dir_y,
        'pos_ant': None
    }

    return bola_info


def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle). 
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial 
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo, 
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros: 
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''
    
    t_jogador = t.Turtle()
    t_jogador.shape("circle")
    t_jogador.shapesize(DEFAULT_TURTLE_SCALE,DEFAULT_TURTLE_SCALE)
    t_jogador.color(cor)
    
    move(x_pos_inicial,y_pos_inicial,t_jogador)
    
    
    return t_jogador


def init_state():
    estado_jogo = {}
    estado_jogo['bola'] = None
    estado_jogo['jogador_vermelho'] = None
    estado_jogo['jogador_azul'] = None
    estado_jogo['var'] = {
        'bola' : [],
        'jogador_vermelho' : [],
        'jogador_azul' : [],
    }
    estado_jogo['pontuacao_jogador_vermelho'] = 0
    estado_jogo['pontuacao_jogador_azul'] = 0
    return estado_jogo

def cria_janela():
    #create a window and declare a variable called window and call the screen()
    window=t.Screen()
    window.title("Foosball Game")
    window.bgcolor("green")
    window.setup(width = LARGURA_JANELA,height = ALTURA_JANELA)
    window.tracer(0)
    return window

def cria_quadro_resultados():
    #Code for creating pen for scorecard update
    quadro=t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0,260)
    quadro.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco',24,"normal"))
    return quadro


def terminar_jogo(estado_jogo):
    '''
     Função responsável por terminar o jogo. Nesta função, deverá atualizar o ficheiro 
     ''historico_resultados.csv'' com o número total de jogos até ao momento, 
     e o resultado final do jogo. Caso o ficheiro não exista, 
     ele deverá ser criado com o seguinte cabeçalho: 
     NJogo,JogadorVermelho,JogadorAzul.
    '''
    
    
    numero_total_jogos = 0
    
    if os.path.exists('historico_resultados.csv'):
        with open('historico_resultados.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            numero_total_jogos = sum(1 for row in reader)
    

    with open('historico_resultados.csv', 'a', newline='') as file:
        writer = csv.writer(file)
    
        if numero_total_jogos == 0:
            writer.writerow(['NJogo', 'JogadorVermelho', 'JogadorAzul'])
    
        numero_total_jogos += 1
        writer.writerow([numero_total_jogos, estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']])


    print("Adeus")
    estado_jogo['janela'].bye()    
    
    

def setup(estado_jogo, jogar):
    janela = cria_janela()
    #Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho') ,'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho') ,'s')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho') ,'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho') ,'d')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul') ,'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul') ,'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul') ,'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul') ,'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo) ,'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['bola'] = bola
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul


def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']),align="center",font=('Monaco',24,"normal"))

def movimenta_bola(estado_jogo):
    '''
    Função responsável pelo movimento da bola que deverá ser feito tendo em conta a
    posição atual da bola e a direção em xx e yy.
    '''
    
    bola = estado_jogo['bola']['bola']
    dir_x = estado_jogo['bola']['dir_x']
    dir_y = estado_jogo['bola']['dir_y']
    
    x, y = bola.position()
    
    nova_posicao = (x + dir_x/math.sqrt(dir_x**2 + dir_y**2), y + dir_y/math.sqrt(dir_x**2 + dir_y**2))
    
    estado_jogo['bola']['pos_ant'] = (x, y)
    
    bola.goto(nova_posicao)    

def verifica_colisoes_ambiente(estado_jogo):
    '''
    Função responsável por verificar se há colisões com os limites do ambiente, 
    atualizando a direção da bola. Não se esqueça de considerar que nas laterais, 
    fora da zona das balizas, a bola deverá inverter a direção onde atingiu o limite.
    '''

    bola = estado_jogo['bola']['bola']
    dir_x = estado_jogo['bola']['dir_x']
    dir_y = estado_jogo['bola']['dir_y']
    
    x, y = bola.position()
    

    if abs(x) >= LARGURA_JANELA / 2 - RAIO_BOLA:
        ang_entr = math.atan2(dir_y, dir_x)
        ang_saida = math.pi - ang_entr 
        estado_jogo['bola']['dir_x'] = math.cos(ang_saida)
        estado_jogo['bola']['dir_y'] = math.sin(ang_saida)
        
    
    if abs(y) >= ALTURA_JANELA / 2 - RAIO_BOLA:
        ang_entr = math.atan2(dir_y, dir_x)
        ang_saida = -ang_entr
        estado_jogo['bola']['dir_x'] = math.cos(ang_saida)
        estado_jogo['bola']['dir_y'] = math.sin(ang_saida)
        
    

    movimenta_bola(estado_jogo)    


def verifica_golo_jogador_vermelho(estado_jogo):
    '''
    Função responsável por verificar se um determinado jogador marcou golo. 
    Para fazer esta verificação poderá fazer uso das constantes: 
    LADO_MAIOR_AREA e 
    START_POS_BALIZAS. 
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador, 
    criar um ficheiro que permita fazer a análise da jogada pelo VAR, 
    e reiniciar o jogo com a bola ao centro. 
    O ficheiro para o VAR deverá conter todas as informações necessárias 
    para repetir a jogada, usando as informações disponíveis no objeto 
    estado_jogo['var']. O ficheiro deverá ter o nome 
    
    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt 
    
    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul] 
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho 
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas 
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;
    
    Em cada linha, os valores de xx e yy das coordenadas são separados por uma 
    ',', e cada coordenada é separada por um ';'.
    '''
    bola = estado_jogo['bola']['bola']
    x, y = bola.position()
   
    
    if 480 < x < 500 and -100 < y < 100:
        estado_jogo['pontuacao_jogador_vermelho'] += 1
        update_board(estado_jogo)
        ficheiro_var(estado_jogo)
        estado_jogo['var']['bola'].clear()
        estado_jogo['var']['jogador_vermelho'].clear()
        estado_jogo['var']['jogador_azul'].clear()
        move(0,0,bola)
        bola.penup()

    
def verifica_golo_jogador_azul(estado_jogo):
    '''
    Função responsável por verificar se um determinado jogador marcou golo. 
    Para fazer esta verificação poderá fazer uso das constantes: 
    LADO_MAIOR_AREA e 
    START_POS_BALIZAS. 
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador, 
    criar um ficheiro que permita fazer a análise da jogada pelo VAR, 
    e reiniciar o jogo com a bola ao centro. 
    O ficheiro para o VAR deverá conter todas as informações necessárias 
    para repetir a jogada, usando as informações disponíveis no objeto 
    estado_jogo['var']. O ficheiro deverá ter o nome 
    
    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt 
    
    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul] 
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho 
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas 
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;
    
    Em cada linha, os valores de xx e yy das coordenadas são separados por uma 
    ',', e cada coordenada é separada por um ';'.
    '''
    bola = estado_jogo['bola']['bola']
    x, y = bola.position()
    
    if -480 > x > -500 and -100 < y < 100:
        estado_jogo['pontuacao_jogador_azul'] += 1
        update_board(estado_jogo)
        ficheiro_var(estado_jogo)
        estado_jogo['var']['bola'].clear()
        estado_jogo['var']['jogador_vermelho'].clear()
        estado_jogo['var']['jogador_azul'].clear()
        move(0,0,bola)
        bola.penup()


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)
    
    

def verifica_toque_jogador(estado_jogo,jogador):
    
    x_j, y_j = estado_jogo[jogador].position()
    x_bola, y_bola = estado_jogo['bola']['bola'].position()
    
    aux = 0
    
    if math.sqrt(pow((x_bola-x_j),2) + pow((y_bola-y_j),2)) <= RAIO_BOLA + RAIO_JOGADOR:
        if x_bola>x_j:
            if y_bola>y_j: 
                aux = estado_jogo['bola']['dir_x'] 
                estado_jogo['bola']['dir_x'] = abs(estado_jogo['bola']['dir_y'])
                estado_jogo['bola']['dir_y'] = abs(aux)
            else:
                aux = estado_jogo['bola']['dir_x'] 
                estado_jogo['bola']['dir_x'] = abs(estado_jogo['bola']['dir_y'])
                estado_jogo['bola']['dir_y'] = -abs(aux)
        else:
            if y_bola>y_j: 
                aux = estado_jogo['bola']['dir_x'] 
                estado_jogo['bola']['dir_x'] = -abs(estado_jogo['bola']['dir_y'])
                estado_jogo['bola']['dir_y'] = abs(aux)
            else:
                aux = estado_jogo['bola']['dir_x'] 
                estado_jogo['bola']['dir_x'] = -abs(estado_jogo['bola']['dir_y'])
                estado_jogo['bola']['dir_y'] = -abs(aux)




        


def verifica_toque_jogador_azul(estado_jogo):
    '''
    Função responsável por verificar se o jogador tocou na bola. 
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''
    verifica_toque_jogador(estado_jogo,'jogador_azul')

           
def verifica_toque_jogador_vermelho(estado_jogo):
    '''
    Função responsável por verificar se o jogador tocou na bola. 
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''
    verifica_toque_jogador(estado_jogo,'jogador_vermelho')
    

def guarda_posicoes_para_var(estado_jogo):
    estado_jogo['var']['bola'].append(estado_jogo['bola']['bola'].pos())
    estado_jogo['var']['jogador_vermelho'].append(estado_jogo['jogador_vermelho'].pos())
    estado_jogo['var']['jogador_azul'].append(estado_jogo['jogador_azul'].pos())

def ficheiro_var(estado_jogo):
    
    f=open('replay_golo_jv_{}_ja_{}.txt'.format(estado_jogo['pontuacao_jogador_vermelho'],estado_jogo['pontuacao_jogador_azul']), 'w')

    formato_decimal = "{:.2f}"

    for idx, i in enumerate(estado_jogo['var']['bola']):
        if idx == 0:
            f.write('{},{}'.format(formato_decimal.format(i[0]), formato_decimal.format(i[1])))
        else:
            f.write(';{},{}'.format(formato_decimal.format(i[0]), formato_decimal.format(i[1])))
    f.write('\n')

    for idx, i in enumerate(estado_jogo['var']['jogador_vermelho']):
        if idx == 0:
            f.write('{},{}'.format(formato_decimal.format(i[0]), formato_decimal.format(i[1])))
        else:
            f.write(';{},{}'.format(formato_decimal.format(i[0]), formato_decimal.format(i[1])))
    f.write('\n')

    for idx, i in enumerate(estado_jogo['var']['jogador_azul']):
        if idx == 0:
            f.write('{},{}'.format(formato_decimal.format(i[0]), formato_decimal.format(i[1])))
        else:
            f.write(';{},{}'.format(formato_decimal.format(i[0]), formato_decimal.format(i[1])))
    f.write('\n')

    f.close()
    

    
def main():
        estado_jogo = init_state()
        setup(estado_jogo, True)
    
        while True:
            
            estado_jogo['janela'].update()
            
            if estado_jogo['bola'] is not None:
                movimenta_bola(estado_jogo)
            verifica_colisoes_ambiente(estado_jogo)
            verifica_golos(estado_jogo)
            
            if estado_jogo['jogador_vermelho'] is not None:
                verifica_toque_jogador_azul(estado_jogo)
            if estado_jogo['jogador_azul'] is not None:
                verifica_toque_jogador_vermelho(estado_jogo)
            guarda_posicoes_para_var(estado_jogo)
            time.sleep(0.01)


if __name__ == '__main__':
    main()