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
OBSTACLE_IMAGE_LIST = ['obstacle1.png', 'obstacle2.png']
OBSTACLE_INIT_Y = 0
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
HELP_ME_TEXT_SIZE = 48
HELP_ME_TEXT_COLOR = (255, 255, 255)
HP_TEXT_COLOR = (255, 0, 0)

class TestMainFunction(unittest.TestCase):
    @patch('game.screen')
    @patch('game.clock')
    def test_main(self, mock_clock, mock_screen):
        # Set up the initial conditions
        little_dragon = MagicMock(spec=Dragon)
        obstacle = MagicMock(spec=Obstacle)
        little_dragon.getX.return_value = 0

        # Mock pygame event loop
        pygame.event.get.side_effect = [
            [pygame.event.Event(pygame.QUIT), pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)],
            [pygame.event.Event(pygame.QUIT)]
        ]

        # Mock the methods called within the main loop
        little_dragon.update.return_value = None
        little_dragon.draw.return_value = None
        little_dragon.go_forward.return_value = None
        obstacle.check_collision.return_value = -1
        obstacle.update.return_value = None
        obstacle.draw.return_value = None

        # Run the main function
        main()

        # Assertions to ensure the game loop is functioning correctly
        self.assertEqual(pygame.event.get.call_count, 2)
        little_dragon.update.assert_called_once_with(WINDOW_HEIGHT)
        little_dragon.draw.assert_called_once_with(mock_screen)
        little_dragon.go_forward.assert_called_once()
        obstacle.check_collision.assert_called_once_with(little_dragon)
        obstacle.update.assert_called_once_with(WINDOW_WIDTH, little_dragon)
        obstacle.draw.assert_called_once_with(mock_screen)

        # Test for game over condition
        little_dragon.getX.return_value = WINDOW_WIDTH + 1
        obstacle.check_collision.return_value = 0
        little_dragon.take_damage = MagicMock()

        # Mock the game over event loop
        pygame.event.get.side_effect = [
            [pygame.event.Event(pygame.QUIT), pygame.event.Event(pygame.KEYDOWN, key=pygame.K_y)],
            [pygame.event.Event(pygame.QUIT)]
        ]

        # Run the main function again to trigger game over
        main()

        # Assertions to ensure the game over loop is functioning correctly
        self.assertEqual(pygame.event.get.call_count, 4)
        little_dragon.take_damage.assert_called_once_with(obstacle.get_obstacle_type(0))

if __name__ == '__main__':
    unittest.main()
