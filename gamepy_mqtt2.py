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

mqttBroker = "localhost"
porta = 1883
client = mqtt.Client("Jogador2")
client.connect(mqttBroker)
client.loop_start()
client.subscribe([("POS_JOGADOR1", 0)])

vermelho = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)

screen_width = 700
screen_height = 400
tam = 10

cor_jogador2 = vermelho
cor_jogador1 = verde

pos_X_jogador2 = 680
pos_Y_jogador2 = 380
pos_X_jogador1 = random.randint(-20, -20)
pos_Y_jogador1 = random.randint(-20, -20)

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

            if not (pos_X_jogador1 - 2 * tam <= nova_pos_X <= pos_X_jogador1 + 2 * tam and
                    pos_Y_jogador1 - 2 * tam <= nova_pos_Y <= pos_Y_jogador1 + 2 * tam):
                pos_X_jogador2 = nova_pos_X
                pos_Y_jogador2 = nova_pos_Y
                client.publish("POS_JOGADOR2", f"{pos_X_jogador2},{pos_Y_jogador2}")

    client.on_message = on_mensagem_jogador1

    tela.fill(azul)
    pygame.draw.circle(tela, cor_jogador2, [pos_X_jogador2, pos_Y_jogador2], tam + 10)
    pygame.draw.circle(tela, cor_jogador1, [pos_X_jogador1, pos_Y_jogador1], tam + 10)
    pygame.display.update()
    time.sleep(0.1)

pygame.display.quit()
