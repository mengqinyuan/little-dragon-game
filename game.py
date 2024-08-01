import pygame
import random
import sys
import time
# ./game.py
# init Pygame
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
DRAGON_MOVE_SPEED = 1
DRAGON_HP = 1000 
# dragon settings
DRAGON_IMAGE_PATH = "./Resource/Dragon.jpg"
DRAGON_INIT_X = 20
DRAGON_INIT_Y = WINDOW_HEIGHT // 4
DRAGON_JUMP_HEIGHT = 10
DRAGON_JUMP_WIDTH = 20
JUMP_DURATION = 10  # jump duration

# TO DEVELOPERS: You can add more obstacle images here. Don't forget to add if-elif block in Obstacle.
OBSTACLE_IMAGE_LIST = ["./Resource/Fire.jpg", "./Resource/Bomb.jpg", "./Resource/Ice.jpg"]
OBSTACLE_INIT_Y = DRAGON_INIT_Y + 100

# Text settings
HELP_ME_TEXT_COLOR = "blue"
HELP_ME_TEXT_SIZE = 30
HELP_ME_TEXT = "Help me please!"
HP_TEXT_COLOR = "black"


class Dragon:
    def __init__(self, speed, jump_height, jump_width):
        self.hp = DRAGON_HP
        self.speed = speed
        self.jump_height = jump_height
        self.jump_width = jump_width
        self.image = pygame.image.load(DRAGON_IMAGE_PATH)
        self.x = DRAGON_INIT_X
        self.y = DRAGON_INIT_Y
        self.jumping:bool = False
        self.jump_counter = 0
        self.collision_cooldown:int = 10

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def go_forward(self):
        self.x += self.speed
        if self.x > WINDOW_WIDTH:
            self.x = DRAGON_INIT_X

    def jump(self):
        self.jumping = True

    def update(self, window_height):
        if self.jumping:
            if self.jump_counter < JUMP_DURATION // 2:
                self.y -= self.jump_height
            elif self.jump_counter < JUMP_DURATION:
                self.y += self.jump_height
                self.x += self.jump_width
            self.jump_counter += 1
            if self.jump_counter >= JUMP_DURATION:
                self.jumping = False
                self.jump_counter = 0
        self.y = min(self.y, window_height - self.image.get_height())

        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def take_damage(self, obstacle_type):
        if self.collision_cooldown == 0:
            damage = 0
            if obstacle_type == "fire":
                damage = 50
            elif obstacle_type == "bomb":
                damage = 100
            elif obstacle_type == "ice":
                damage = 10
            self.hp -= damage
            self.collision_cooldown = 10
            if self.hp <= 0:
                raise GameOverException("You lose!")
        else:
            # TO DEVELOPERS: You can add more UI effects here
            pass

class Obstacle:
    images_cache = {}  # 用于缓存已加载的图像

    def __init__(self, image_paths, init_y, dragon, window_width):
        self.y = init_y
        self.x_ls = [random.randint(dragon.getX(), window_width) for _ in range(2)]
        if abs(self.x_ls[0] - self.x_ls[1]) <= 50:
            diff = abs(self.x_ls[0] - self.x_ls[1]) - 50
            self.x_ls[0] -= diff // 2
            self.x_ls[1] += diff // 2

        # 从缓存中获取图像，如果不在缓存中则加载并加入缓存
        self.images = []
        self.types = []  # 新增的列表，用于存储每个障碍物的类型
        for path in image_paths:
            self.images.append(self.load_image(path))
            if path == "./Resource/Fire.jpg":
                self.types.append("fire")
            elif path == "./Resource/Bomb.jpg":
                self.types.append("bomb")
            elif path == "./Resource/Ice.jpg":
                self.types.append("ice")

        self.rects = [pygame.Rect(x, self.y, img.get_width(), img.get_height()) for x, img in zip(self.x_ls, self.images)]
        self.move_speed = 3.5  # 设置障碍物的移动速度

    @classmethod
    def load_image(cls, path):
        """加载图像并缓存"""
        if path not in cls.images_cache:
            cls.images_cache[path] = pygame.image.load(path).convert_alpha()
        return cls.images_cache[path]

    def draw(self, screen):
        for rect, img in zip(self.rects, self.images):
            screen.blit(img, rect)

    def update(self, window_width, dragon):
        for i, rect in enumerate(self.rects):
            rect.x -= self.move_speed
            if rect.right < 0:
                # 当障碍物移出屏幕左侧时，重新生成位置和图像
                new_x = random.randint(dragon.getX(), window_width)
                self.x_ls[i] = new_x
                new_path = random.choice(OBSTACLE_IMAGE_LIST)
                self.images[i] = self.load_image(new_path)
                self.types[i] = "fire" if new_path == "./Resource/Fire.jpg" else "bomb"
                self.rects[i] = pygame.Rect(new_x, self.y, self.images[i].get_width(), self.images[i].get_height())

    def check_collision(self, dragon: Dragon) -> int:
        dragon_rect = pygame.Rect(dragon.x, dragon.y, dragon.image.get_width(), dragon.image.get_height())
        for i, rect in enumerate(self.rects):
            if dragon_rect.colliderect(rect):
                return i
        return -1

    def get_obstacle_type(self, index) -> str:
        # 根据索引返回障碍物类型
        return self.types[index]


class GameOverException(Exception):
    pass

def main():
    global OBSTACLE_IMAGE_LIST

    little_dragon = Dragon(DRAGON_MOVE_SPEED, DRAGON_JUMP_HEIGHT, DRAGON_JUMP_WIDTH)
    obstacle = Obstacle(OBSTACLE_IMAGE_LIST, OBSTACLE_INIT_Y, little_dragon, WINDOW_WIDTH)
    running = True

    font = pygame.font.SysFont("Arial", 30)

    while running:
        screen.fill((255, 255, 255))
        time.sleep(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    little_dragon.jump()

        little_dragon.update(WINDOW_HEIGHT)
        little_dragon.draw(screen)
        little_dragon.go_forward()

        if little_dragon.getX() > WINDOW_WIDTH:
            obstacle = Obstacle(OBSTACLE_IMAGE_LIST, OBSTACLE_INIT_Y, little_dragon, WINDOW_WIDTH)

        try:
            if obstacle.check_collision(little_dragon) != -1:
                index = obstacle.check_collision(little_dragon)
                little_dragon.take_damage(obstacle.get_obstacle_type(index))

        except GameOverException as e:
            print(e)
            running = False
            while running:
                time.sleep(2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:  # if pressed key 'y', restart the game
                            little_dragon = Dragon(DRAGON_MOVE_SPEED, DRAGON_JUMP_HEIGHT, DRAGON_JUMP_WIDTH)
                            obstacle = Obstacle(OBSTACLE_IMAGE_LIST, OBSTACLE_INIT_Y, little_dragon, WINDOW_WIDTH)
                            running = False
                        elif event.key == pygame.K_n:  # if pressed key 'n', quit the game
                            pygame.quit()
                            sys.exit()

        # redraw the obstacle
        obstacle.update(WINDOW_WIDTH, little_dragon)
        obstacle.draw(screen)

        # show text on the screen
        if not running:
            font = pygame.font.SysFont("Arial", HELP_ME_TEXT_SIZE)
            text = font.render("Game Over. Press 'y' to restart or 'n' to exit.", True, HELP_ME_TEXT_COLOR)
            screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))

        hp_text = font.render(f"HP: {little_dragon.hp}", True, HP_TEXT_COLOR)
        screen.blit(hp_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)  # target 60 FPS


if __name__ == "__main__":
    main()
    pygame.quit()
