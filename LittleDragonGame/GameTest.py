import unittest
from unittest.mock import patch, MagicMock
from game import main, Dragon, Obstacle, GameOverException
import sys

# Mock pygame and its modules
pygame = MagicMock()
pygame.font = MagicMock()
pygame.font.SysFont = MagicMock(return_value=MagicMock())
pygame.event = MagicMock()
pygame.QUIT = pygame.KEYDOWN = MagicMock()
pygame.K_SPACE = pygame.K_y = pygame.K_n = MagicMock()
pygame.quit = MagicMock()
sys.exit = MagicMock()

# Mock global variables
DRAGON_MOVE_SPEED = 5
DRAGON_JUMP_HEIGHT = 100
DRAGON_JUMP_WIDTH = 50
OBSTACLE_IMAGE_LIST = ['./Resource/Fire.jpg', './Resource/Ice.jpg， ‘./Resource/Bomb.jpg']
OBSTACLE_INIT_Y = 0
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
HELP_ME_TEXT_SIZE = 48
HELP_ME_TEXT_COLOR = (255, 255, 255)
HP_TEXT_COLOR = (255, 0, 0)

class TestMainFunction(unittest.TestCase):
    def main(self):
        pass
    # Write test here.

if __name__ == '__main__':
    unittest.main()
