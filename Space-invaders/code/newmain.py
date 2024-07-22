import os, sys
from fcntl import ioctl
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

# Definições de valores dos displays de 7 segmentos
HEX_0 = 0xC0
HEX_1 = 0xF9
HEX_2 = 0xA4
HEX_3 = 0xB0
HEX_4 = 0x99
HEX_5 = 0x92
HEX_6 = 0x82
HEX_7 = 0xF8
HEX_8 = 0x80
HEX_9 = 0x90
HEX_A = 0x88
HEX_B = 0x83
HEX_C = 0xC6
HEX_D = 0xA1
HEX_E = 0x86
HEX_F = 0x8E

PB = 24930
SW = 24929
DIS_L = 24931
DIS_R = 24932
LED_R = 24933
LED_G = 24934

class IO:

    def __init__(self) -> None:
        self.fd = os.open('/dev/mydev', os.O_RDWR)
        self.dev = SW

    def __del__(self):
        os.close(self.fd)

    def get_SW(self, pos):
        ioctl(self.fd, SW)
        sw_pos = (0x1 << pos)
        os.read(self.fd, 4)
        ret_sw = os.read(self.fd, 4)
        return 1 if (sw_pos & int.from_bytes(ret_sw, 'little')) > 0 else 0
    
    def get_PB(self, pos):
        ioctl(self.fd, PB)
        pb_pos = (1 << pos)
        os.read(self.fd, 4)
        ret_pb = os.read(self.fd, 4)
        data_ret = 1 if (pb_pos & int.from_bytes(ret_pb, 'little')) > 0 else 0
        return data_ret

    def put_LD(self, val):
        ioctl(self.fd, LED_R)
        os.write(self.fd, val.to_bytes(4, 'little'))

    def put_ar_LD(self, list_pos):
        ioctl(self.fd, LED_R)
        data = 0
        for num in list_pos:
            data = (1 << num) | data
        os.write(self.fd, data.to_bytes(4, 'little'))

    def put_DP(self, pos, ar_num):
        if pos == 0:
            ioctl(self.fd, DIS_R)
        else:
            ioctl(self.fd, DIS_L)

        data = 0
        for num in ar_num:
            data = self.__aux_DP(data, num, 8)
        os.write(self.fd, data.to_bytes(4, 'little'))

    def __aux_DP(self, data, num, ind):
        data = data << ind
        if num == '0':
            data = data | HEX_0
        elif num == '1':
            data = data | HEX_1
        elif num == '2':
            data = data | HEX_2
        elif num == '3':
            data = data | HEX_3
        elif num == '4':
            data = data | HEX_4
        elif num == '5':
            data = data | HEX_5
        elif num == '6':
            data = data | HEX_6
        elif num == '7':
            data = data | HEX_7
        elif num == '8':
            data = data | HEX_8
        elif num == '9':
            data = data | HEX_9
        elif num == 'A':
            data = data | HEX_A
        elif num == 'B':
            data = data | HEX_B
        elif num == 'C':
            data = data | HEX_C
        elif num == 'D':
            data = data | HEX_D
        elif num == 'E':
            data = data | HEX_E
        elif num == 'F':
            data = data | HEX_F
        return data

class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('../graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('../font/Pixeled.ttf', 20)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        # Audio
        music = pygame.mixer.Sound('../audio/music.wav')
        music.set_volume(0.2)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

        # IO setup
        self.io = IO()

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):

        # player lasers 
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        # alien lasers 
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    self.update_lives_display()
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def update_lives_display(self):
        # Atualiza o display de 7 segmentos com o número de vidas
        self.io.put_DP(0, str(self.lives))

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won', False, 'white')
            victory_rect = victory_surf.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()

        # Leitura dos botões e switches
        self.read_controls()

    def read_controls(self):
        # Movimentação do jogador
        move_left = self.io.get_PB(0)  # Botão 0
        move_right = self.io.get_PB(1)  # Botão 1

        if move_left:
            self.player.sprite.move_left()
        if move_right:
            self.player.sprite.move_right()

        # Tiro do jogador
        shoot = self.io.get_PB(2)  # Botão 2
        if shoot:
            self.player.sprite.shoot()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()
        # crt.draw()

        pygame.display.flip()
        clock.tick(60)
