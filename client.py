import random
import pygame
import constants as c
import math
from network import Network

pygame.init()


class Gameplay:
    def __init__(self):
        self.width = c.WIDTH
        self.height = c.HEIGHT
        self.color = c.GAMEPLAY_BG
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gameplay")
        self.soldiers = []  # Danh sách các lính
        self.last_soldier_time = pygame.time.get_ticks()  # Thời điểm cuối cùng khi tạo ra lính mới
        self.spawn_interval = 3500  # Khoảng thời gian giữa các lần xuất hiện lính (ms)
        self.wall = Wall()
        self.cannon = Cannon()
        self.player_health = 15  # Máu của người chơi

    def spawn_soldiers(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_soldier_time >= self.spawn_interval:
            # Tạo ra lính mới
            y = random.randint(150, c.HEIGHT - 150)  # Chọn vị trí y ngẫu nhiên
            soldier = Soldier(y)
            self.soldiers.append(soldier)
            self.last_soldier_time = current_time
            if self.spawn_interval >= 1500:
                self.spawn_interval -= 180
            if self.spawn_interval <= 2000:
                soldier.speed = 2.5
            elif self.spawn_interval <= 1500:
                soldier.speed = 3

    def move_soldiers(self, network):
        current_time = pygame.time.get_ticks()
        for soldier in self.soldiers:
            soldier.draw_and_move(self.win)
            soldier.update_animation(current_time, soldier.is_attack)
            if not soldier.is_alive:
                self.soldiers.remove(soldier)
            for bullet in self.cannon.bullets:
                if bullet.is_explosion:  # Kiểm tra chỉ với các viên đạn đã nổ
                    soldier.check_collision(bullet)

            # Kiểm tra va chạm giữa lính và tường
            if soldier.rect.colliderect(self.wall.rect_edge):
                # Nếu lính va chạm vào tường lâu hơn 1 giây
                if current_time - soldier.last_wall_hit_time >= 1000:
                    soldier.is_attack = True
                    soldier.last_wall_hit_time = current_time
                    # Giảm máu của người chơi
                    if self.player_health > 0:
                        self.player_health = self.player_health - 1
                        print(self.player_health)
                        network.send(str(self.player_health))

    def screen_click_to_play(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            self.win.blit(c.start_bg, (0, 0))
            text = c.FONT_60_bold.render("Click to play", 1, c.WHITE)
            self.win.blit(text,
                          (self.width / 2 - text.get_width() / 2 - 330, self.height / 2 - text.get_height() / 2 - 250))
            text1 = c.FONT_30_bold.render("By QuynhThuanTram", 1, c.WHITE)
            self.win.blit(text1,
                          (self.width - 350, self.height - 90))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

    def main(self):
        self.screen_click_to_play()
        run = True
        clock = pygame.time.Clock()
        network = Network()
        player = int(network.getP())
        print("You are player", player)

        while run:
            clock.tick(60)
            try:
                game = network.send("get")
            except:
                run = False
                print("Couldn't get game")
                break

            if game.check_health():
                if (game.winner() == 0 and player == 0) or (game.winner() == 1 and player == 1):
                    text = c.FONT_80_bold.render("You Won!!!", 1, c.WHITE)
                else:
                    text = c.FONT_80_bold.render("You Lost...", 1, c.WHITE)
                self.win.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))
                run = False
                pygame.display.update()
                pygame.time.delay(3000)
                try:
                    game = network.send("reset")
                except:
                    run = False
                    print("Couldn't get game")
                    break
                self.draw_window(game, network, player)

            self.draw_window(game, network, player)

    def draw_window(self, game, network, player):
        if game.connected():
            self.win.fill(self.color)
            self.wall.draw(self.win)
            self.cannon.draw_and_move(self.win)
            self.spawn_soldiers()  # Tạo ra các lính mới
            self.move_soldiers(network)  # Di chuyển các lính
            self.draw_health(game, player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    self.cannon.image_index = 0
                    self.cannon.cannon_image = self.cannon.cannon_images[self.cannon.image_index]
                    self.cannon.shooting = True
                    self.cannon.start_time_keyup = pygame.time.get_ticks()  # Lưu thời điểm bắt đầu giữ nút Enter
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.cannon.image_index = 1
                    self.cannon.cannon_image = self.cannon.cannon_images[self.cannon.image_index]
                    self.cannon.aiming = True
                    self.cannon.start_time_keydown = pygame.time.get_ticks()
        else:
            self.win.blit(c.start_bg, (0, 0))
            text = c.FONT_60_bold.render("Waiting for Player...", 1, c.WHITE)
            self.win.blit(text,
                          (self.width / 2 - text.get_width() / 2 - 220, self.height / 2 - text.get_height() / 2 - 250))
            text1 = c.FONT_30_bold.render("By_QuynhThuanTram", 1, c.WHITE)
            self.win.blit(text1,
                          (self.width - 350, self.height - 90))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        pygame.display.update()

    def draw_health(self, game, player):
        center_x = self.width // 2
        center_y = 0
        radius = 70
        pygame.draw.circle(self.win, c.WHITE, (center_x, center_y), radius)

        if player == 0:
            text1 = c.FONT_25_bold.render(f"{game.get_health()[0]} - ", 1, c.PLAYER_2_COLOR)
            text2 = c.FONT_25_bold.render(f"{game.get_health()[1]}", 1, c.PLAYER_1_COLOR)
        else:
            text1 = c.FONT_25_bold.render(f"{game.get_health()[1]} - ", 1, c.PLAYER_2_COLOR)
            text2 = c.FONT_25_bold.render(f"{game.get_health()[0]}", 1, c.PLAYER_1_COLOR)
        self.win.blit(text1,
                      (self.width / 2 - text1.get_width() / 2 - 15, 10))
        self.win.blit(text2,
                      (self.width / 2 - text1.get_width() / 2
                       + text1.get_width() - 15, 10))


class Wall:
    def __init__(self):
        self.width = 210
        self.height = 640
        self.color = c.WALL_COLOR
        self.img_wall = c.img_wall
        # self.color_edge = c.WALL_EDGE_COLOR
        self.rect_edge = self.img_wall.get_rect(topleft=(self.width, 0))
        # self.rect_edge = pygame.Rect(self.width, 0, 40, self.height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        win.blit(self.img_wall, self.rect_edge)


class Cannon:
    def __init__(self):
        self.angle = 250
        self.clockwise = True
        self.bullets = []
        self.last_shot_time = 0
        self.shooting = False  # Biến để xác định khi nào đang bắn
        self.aiming = False  # Biến để xác định khi nào đang ngắm bắn
        self.start_time_keyup = 0  # Thời điểm bắt đầu giữ nút Enter
        self.start_time_keydown = 0
        self.became_idle_time = 0  # Thời điểm trở thành bất động
        self.cannon_images = c.images_cannon
        self.image_index = 0
        self.cannon_image = self.cannon_images[self.image_index]
        self.rect_width = self.cannon_image.get_width()
        self.rect_height = self.cannon_image.get_height()
        self.cannon_image = pygame.transform.scale(self.cannon_image, (self.rect_width, self.rect_height))

    def draw_and_move(self, win):

        angle = self.angle
        rotated_cannon = pygame.transform.rotate(self.cannon_image, angle)

        # Tính toán vị trí mới của hình chữ nhật sau khi xoay
        rotated_rect = rotated_cannon.get_rect(center=(self.rect_width / 4, self.rect_height / 2))

        win.blit(rotated_cannon, (100 - rotated_rect.width / 2 + 45, c.HEIGHT / 2 - rotated_rect.height / 2))

        # Nếu đang bắn và đã trôi qua ít nhất 1 giây từ lần bắn đạn trước đó
        if self.shooting:
            current_time = pygame.time.get_ticks()
            time_since_last_shot = current_time - self.last_shot_time
            if time_since_last_shot <= 1000:
                self.aiming = False
            else:
                self.aiming = True

            if time_since_last_shot >= 1000:
                self.shoot()
                self.last_shot_time = current_time
                self.shooting = False
                self.aiming = False
                self.became_idle_time = current_time

        if not self.aiming and not self.shooting and pygame.time.get_ticks() - self.became_idle_time >= 300:
            # Tăng góc quay
            if self.clockwise:
                self.angle += 2.5
                if self.angle >= 250:
                    self.clockwise = False
            else:
                self.angle -= 2.5
                if self.angle <= 110:
                    self.clockwise = True

        for bullet in self.bullets:
            bullet.draw(win)
            bullet.move(win)
            if bullet.explosion_time - bullet.explosion_timer <= 0:
                self.bullets.remove(bullet)

    def shoot(self):
        # Tính toán thời gian đã giữ nút Enter
        hold_time = self.start_time_keyup - self.start_time_keydown

        # Tính toán khoảng cách di chuyển của đạn dựa trên thời gian đã giữ nút Enter
        max_distance = 1000  # Khoảng cách tối đa (px) khi giữ nút Enter 1s
        min_distance = 10  # Khoảng cách tối thiểu (px) khi giữ nút Enter ngay lập tức
        hold_time = min(hold_time, 1000)  # Giới hạn thời gian giữ nút Enter là 1s
        distance = min_distance + (max_distance - min_distance) * (hold_time / 1000)

        # Tính toán tọa độ xuất phát của viên đạn từ chính giữa cạnh chiều cao bên phải của hình chữ nhật
        angle = self.angle
        bullet_x = 100 - math.cos(math.radians(angle)) * self.rect_width / 2
        bullet_y = c.HEIGHT / 2 + math.sin(math.radians(angle)) * self.rect_width / 2

        # Tạo một viên đạn mới với khoảng cách di chuyển tính được
        bullet = Bullet(bullet_x, bullet_y, angle, distance)
        self.bullets.append(bullet)  # Thêm viên đạn vào danh sách


class Bullet:
    def __init__(self, x, y, angle, distance):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.angle = angle
        self.max_distance = distance  # Khoảng cách tối đa mà viên đạn có thể đi được
        self.distance_traveled = 0  # Khoảng cách đã di chuyển của viên đạn
        self.end_x = self.start_x - math.cos(math.radians(self.angle)) * self.max_distance
        self.end_y = self.start_y + math.sin(math.radians(self.angle)) * self.max_distance
        self.is_draw = True
        self.is_explosion = False
        self.explosion_time = 20  # Thời gian tồn tại của hiệu ứng nổ (tính bằng số lượng frame, 60 frames ≈ 1 giây)
        self.explosion_timer = 0  # Biến đếm thời gian đã trôi qua sau khi viên đạn nổ
        self.img_explosion = c.img_bum_blue
        self.rect_explosion = self.img_explosion.get_rect(topleft=(int(self.x - 90), int(self.y - 85)))

    def draw(self, win):
        color = c.PLAYER_2_COLOR
        if self.is_draw:
            pygame.draw.circle(win, color, (int(self.x), int(self.y)), 40)  # Vẽ viên đạn là một hình tròn

        if self.is_explosion and self.explosion_time - self.explosion_timer >= 0:
            win.blit(self.img_explosion, (int(self.x - 90), int(self.y - 85)))
            self.explosion_timer += 1

    def move(self, win):
        # Kiểm tra nếu viên đạn đạt đến vị trí cuối cùng
        if abs(self.x - self.end_x) < 10 and abs(self.y - self.end_y) < 10:
            self.is_draw = False
            self.is_explosion = True
            self.rect_explosion = self.img_explosion.get_rect(topleft=(int(self.x - 90), int(self.y - 85)))
        else:
            # Di chuyển viên đạn theo hướng đã được xác định bởi góc
            self.x -= math.cos(math.radians(self.angle)) * 20
            self.y += math.sin(math.radians(self.angle)) * 20


class Soldier:
    def __init__(self, y):
        self.speed = 2
        self.is_alive = True
        self.last_wall_hit_time = pygame.time.get_ticks()  # Thời điểm cuối cùng khi lính va chạm vào tường
        self.images = c.images_solider_red
        self.image_index = 0  # Chỉ số của hình ảnh trong mảng images
        self.image_timer = 0  # Biến đếm thời gian để cập nhật hình ảnh
        self.x = c.WIDTH - self.images[0].get_width()
        self.y = y
        self.images = c.images_solider_red
        self.rect = self.images[self.image_index].get_rect(topleft=(self.x, self.y))
        self.is_attack = False

    def draw_and_move(self, win):

        if self.x >= 240:
            self.x -= self.speed
        color = c.PLAYER_2_COLOR

        if self.is_alive:
            win.blit(self.images[self.image_index], (self.x, self.y))
            self.rect = self.images[self.image_index].get_rect(topleft=(self.x, self.y))

    def check_collision(self, bullet):
        if self.rect.colliderect(bullet.rect_explosion):
            self.is_alive = False  # Đặt trạng thái của lính thành không còn sống

    def update_animation(self, current_time, is_attack):
        if not is_attack:
            if current_time - self.image_timer > 200:  # Thay đổi ảnh sau mỗi 200ms
                self.image_timer = current_time
                self.image_index = 0 if self.image_index == 1 else 1
        else:
            if current_time - self.image_timer > 500:
                self.image_timer = current_time
                self.image_index = 1 if self.image_index == 2 else 2


while True:
    Gameplay().main()
