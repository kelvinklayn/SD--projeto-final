import pygame
import paho.mqtt.client as mqtt
import time
import random

def on_mensagem_jogador2(client, userdata, message):
    global pos_X_jogador2, pos_Y_jogador2
    pos_jogador2 = str(message.payload.decode("utf-8")).split(',')
    pos_X_jogador2 = int(pos_jogador2[0])
    pos_Y_jogador2 = int(pos_jogador2[1])
    print("Recebeu mensagem do Jogador 2 ->>", pos_X_jogador2, pos_Y_jogador2)

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
client = mqtt.Client("Jogador1")
client.connect(mqttBroker)
client.loop_start()
client.subscribe([("POS_JOGADOR2", 0)])

vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
cinza = (169, 169, 169)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

screen_width = 700
screen_height = 400
tam = 10
cor_jogador1 = azul
cor_jogador2 = vermelho

pos_X_jogador1 = 20
pos_Y_jogador1 = 20
pos_X_jogador2 = -70
pos_Y_jogador2 = -70

largura_carro = 80
altura_carro = 40
raio_roda = 15

pygame.init()

tela = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(" Meu Jogo: Jogador 1 ")

sair = True
val_jogador1 = 0

while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False
        if event.type == pygame.KEYDOWN:
            nova_pos_X = pos_X_jogador1
            nova_pos_Y = pos_Y_jogador1

            if event.key == pygame.K_LEFT:
                nova_pos_X -= 10
            elif event.key == pygame.K_RIGHT:
                nova_pos_X += 10
            elif event.key == pygame.K_UP:
                nova_pos_Y -= 10
            elif event.key == pygame.K_DOWN:
                nova_pos_Y += 10

            if not colisao_carros(nova_pos_X, nova_pos_Y - 25, largura_carro + 10, altura_carro + 40, pos_X_jogador2 - largura_carro, pos_Y_jogador2 - altura_carro - 25, largura_carro, altura_carro + 40):
                dentro_da_pista = (-30 < nova_pos_X < 80 and 0 < nova_pos_Y < 360) or (535 < nova_pos_X < 630 and 0 < nova_pos_Y < 360) or (75 < nova_pos_X < 545 and 110 < nova_pos_Y < 230)
                if dentro_da_pista:
                    pos_X_jogador1 = nova_pos_X
                    pos_Y_jogador1 = nova_pos_Y
                    client.publish("POS_JOGADOR1", f"{pos_X_jogador1},{pos_Y_jogador1}")


    client.on_message = on_mensagem_jogador2

    tela.fill(verde)
    desenhar_pista()
    pygame.draw.rect(tela, preto, [pos_X_jogador1 + 25, pos_Y_jogador1 - 20, largura_carro - 40, altura_carro - 20])
    pygame.draw.rect(tela, preto, [pos_X_jogador1, pos_Y_jogador1, largura_carro, altura_carro])
    pygame.draw.circle(tela, amarelo, (pos_X_jogador1 + 60, pos_Y_jogador1+ altura_carro), raio_roda)
    pygame.draw.circle(tela, amarelo, (pos_X_jogador1 + 25, pos_Y_jogador1 + altura_carro), raio_roda)
    
    pygame.draw.rect(tela, azul, [pos_X_jogador2 - largura_carro + 25, pos_Y_jogador2 - altura_carro - 20, largura_carro - 40, altura_carro - 20])
    pygame.draw.rect(tela, azul, [pos_X_jogador2 - largura_carro, pos_Y_jogador2 - altura_carro, largura_carro, altura_carro])
    pygame.draw.circle(tela, vermelho, (pos_X_jogador2 - 60, pos_Y_jogador2), raio_roda)
    pygame.draw.circle(tela, vermelho, (pos_X_jogador2 - 25, pos_Y_jogador2), raio_roda)

    pygame.display.update()
    time.sleep(0.1)

pygame.display.quit()
