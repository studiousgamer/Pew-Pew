import pygame
import network
import json
import math
from objects import Player, Enemy

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption("Pew Pew")
clock = pygame.time.Clock()
running = True
net = network.Network()
mapdata = net.send('{"type": "get", "payload": "map"}')
print(mapdata)


def render_players(player:dict, enemies:dict) -> (Player, []):
    _player = Player(player['id'], screen)
    _player.update(**player)
    _enemies = [Enemy(enemy['id']) for enemy in enemies.values() if enemy['id'] != player['id']]
    for enemy in _enemies:
        enemy.update(**enemies[enemy.id])
    return _player, _enemies


def get_rotation(player_pos: list) -> int:
    cursor_pos = list(pygame.mouse.get_pos())
    return int(
        math.atan2(player_pos[0] - cursor_pos[0], player_pos[1] - cursor_pos[1])
        * 180
        / math.pi
    )


def render_map() -> None:
    screen.fill((12, 151, 0))
    gameMap = json.loads(mapdata)
    walls = pygame.image.load("assets/map/wall.png")
    x, y = 0, 0
    for i in gameMap:
        for k in i:
            if k == 1:
                screen.blit(walls, (x, y))
            x += 32
        x = 0
        y += 32


allBullets = []

allUsers = json.loads(net.send(json.dumps({"type": "get", "payload": "all"})))
user = json.loads(net.send(json.dumps({"type": "get", "payload": "self"})))

player, enemies = render_players(user, allUsers)


while running:
    # global allUsers, user
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    render_map()

    pygame.display.flip()

pygame.quit()
