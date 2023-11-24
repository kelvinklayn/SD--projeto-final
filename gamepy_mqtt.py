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

mqttBroker = "localhost"
porta = 1883
client = mqtt.Client("Jogador1")
client.connect(mqttBroker)
client.loop_start()
client.subscribe([("POS_JOGADOR2", 0)])

vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

screen_width = 700
screen_height = 400
tam = 10
cor_jogador1 = verde
cor_jogador2 = vermelho

pos_X_jogador1 = 20
pos_Y_jogador1 = 20
pos_X_jogador2 = random.randint(-20, -20)
pos_Y_jogador2 = random.randint(-20, -20)

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

            if not (pos_X_jogador2 - 2 * tam <= nova_pos_X <= pos_X_jogador2 + 2 * tam and
                    pos_Y_jogador2 - 2 * tam <= nova_pos_Y <= pos_Y_jogador2 + 2 * tam):
                pos_X_jogador1 = nova_pos_X
                pos_Y_jogador1 = nova_pos_Y
                client.publish("POS_JOGADOR1", f"{pos_X_jogador1},{pos_Y_jogador1}")

    client.on_message = on_mensagem_jogador2

    tela.fill(azul)
    pygame.draw.circle(tela, cor_jogador1, [pos_X_jogador1, pos_Y_jogador1], tam + 10)
    pygame.draw.circle(tela, cor_jogador2, [pos_X_jogador2, pos_Y_jogador2], tam + 10)
    pygame.display.update()
    time.sleep(0.1)

pygame.display.quit()
