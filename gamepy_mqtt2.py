import pygame
import paho.mqtt.client as mqtt
import time
import random

global pos_X_jogador1, pos_Y_jogador1
def on_mensagem_jogador1(client, userdata, message):
    global pos_X_jogador1, pos_Y_jogador1
    pos_jogador1 = str(message.payload.decode("utf-8")).split(',')
    pos_X_jogador1 = int(pos_jogador1[0])
    pos_Y_jogador1 = int(pos_jogador1[1])
    print("Recebeu mensagem do Jogador 1 ->>", pos_X_jogador1, pos_Y_jogador1)

def desenhar_pista():
    # Desenha a pista com duas ruas ligadas
    pygame.draw.rect(tela, cinza, (0, 0, 120, 700))
    pygame.draw.rect(tela, cinza, (580, 0, 120, 700))
    pygame.draw.rect(tela, cinza, (120, 140, 480, 120))

def colisao_carros(x1, y1, largura1, altura1, x2, y2, largura2, altura2):
    # Bounding box do carro 1
    bb_carro1 = pygame.Rect(x1, y1, largura1, altura1)

    # Bounding box do carro 2
    bb_carro2 = pygame.Rect(x2, y2, largura2, altura2)

    # Verifica se as bounding boxes colidem
    return bb_carro1.colliderect(bb_carro2)

mqttBroker = "localhost"
porta = 1883
client = mqtt.Client("Jogador2")
client.connect(mqttBroker)
client.loop_start()
client.subscribe([("POS_JOGADOR1", 0)])

vermelho = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)
cinza = (169, 169, 169)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

screen_width = 700
screen_height = 400
tam = 10

cor_jogador2 = vermelho
cor_jogador1 = azul

pos_X_jogador2 = 680
pos_Y_jogador2 = 380
pos_X_jogador1 = -40
pos_Y_jogador1 = -70

largura_carro = 80
altura_carro = 40
raio_roda = 15

pygame.init()

tela = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(" Meu Jogo: Jogador 2 ")

sair = True
val_jogador2 = 0

while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False
        if event.type == pygame.KEYDOWN:
            nova_pos_X = pos_X_jogador2
            nova_pos_Y = pos_Y_jogador2

            if event.key == pygame.K_LEFT:
                nova_pos_X -= 10
            elif event.key == pygame.K_RIGHT:
                nova_pos_X += 10
            elif event.key == pygame.K_UP:
                nova_pos_Y -= 10
            elif event.key == pygame.K_DOWN:
                nova_pos_Y += 10

            dentro_da_pista = (0+60 < nova_pos_X < 120+30 and 60 < nova_pos_Y < 400) or (580+60 < nova_pos_X < 700 and 60 < nova_pos_Y < 400) or (115 < nova_pos_X < 645 and 140 < nova_pos_Y < 260)
            
            if not colisao_carros(pos_X_jogador1, pos_Y_jogador1 - 25, largura_carro + 10, altura_carro + 40, nova_pos_X - largura_carro, nova_pos_Y - altura_carro - 25, largura_carro, altura_carro + 40):
                if dentro_da_pista:
                    pos_X_jogador2 = nova_pos_X
                    pos_Y_jogador2 = nova_pos_Y
                    client.publish("POS_JOGADOR2", f"{pos_X_jogador2},{pos_Y_jogador2}")

    client.on_message = on_mensagem_jogador1

    tela.fill(verde)
    desenhar_pista()
    
    pygame.draw.rect(tela, preto, [pos_X_jogador1 + 25, pos_Y_jogador1 - 20, largura_carro - 40, altura_carro - 20])
    pygame.draw.rect(tela, preto, [pos_X_jogador1, pos_Y_jogador1, largura_carro, altura_carro])
    pygame.draw.circle(tela, amarelo, (pos_X_jogador1 + 60, pos_Y_jogador1+ altura_carro), raio_roda)
    pygame.draw.circle(tela, amarelo, (pos_X_jogador1 + 25, pos_Y_jogador1 + altura_carro), raio_roda)
    pygame.display.update()

    pygame.draw.rect(tela, azul, [pos_X_jogador2 - largura_carro + 25, pos_Y_jogador2 - altura_carro - 20, largura_carro - 40, altura_carro - 20])
    pygame.draw.rect(tela, azul, [pos_X_jogador2 - largura_carro, pos_Y_jogador2 - altura_carro, largura_carro, altura_carro])
    pygame.draw.circle(tela, vermelho, (pos_X_jogador2 - 60, pos_Y_jogador2), raio_roda)
    pygame.draw.circle(tela, vermelho, (pos_X_jogador2 - 25, pos_Y_jogador2), raio_roda)

    pygame.display.update()
    time.sleep(0.1)

pygame.display.quit()
