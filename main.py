import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

class Snake:
    def __init__(self, parent_screen, player_num):
        self.parent_screen = parent_screen
        if player_num == 1:
            self.image = pygame.image.load("resources/block.jpg").convert()  # Change to the desired color
        else:
            self.image = pygame.image.load("resources/block2.png").convert()
        self.direction = 'down'
        self.speed = 15  # Initial speed
        self.length = 1
        self.x = [40]
        self.y = [40]
        self.player_num = player_num

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.speed += 1  # Increase speed as the snake grows
        self.x.append(-1)
        self.y.append(-1)

    def decrease_length(self):
        if self.length > 1:
            self.length -= 1
            self.x.pop()
            self.y.pop()

class MultiplayerGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Multiplayer Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.player1 = Snake(self.surface, player_num=1)
        self.player2 = Snake(self.surface, player_num=2)
        self.apples = [Apple(self.surface) for _ in range(2)]  # Two apples for both players

        self.apples[0].move()
        self.apples[1].move()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def reset(self):
        self.player1 = Snake(self.surface, player_num=1)
        self.player2 = Snake(self.surface, player_num=2)
        for apple in self.apples:
            apple.move()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def is_out_of_bounds(self, x, y):
        if x < 0 or x >= 1000 or y < 0 or y >= 800:
            return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()

        self.player1.walk()
        self.player2.walk()

        for apple in self.apples:
            apple.draw()

        self.display_score()

        pygame.display.flip()

        for i, player in enumerate([self.player1, self.player2]):
            # Check for collisions with apples
            for apple in self.apples:
                if self.is_collision(player.x[0], player.y[0], apple.x, apple.y):
                    player.increase_length()
                    apple.move()

            # Check for collisions with other player
            other_player = self.player2 if i == 0 else self.player1
            for j in range(3, other_player.length):
                if self.is_collision(player.x[0], player.y[0], other_player.x[j], other_player.y[j]):
                    self.show_winner(other_player.player_num)
                    raise "Collision Occurred"

            # Check if the snake is out of bounds
            if self.is_out_of_bounds(player.x[0], player.y[0]):
                self.show_winner(other_player.player_num)
                raise "Out of Bounds"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)

        score1 = font.render(f"Player 1 Score: {self.player1.length - 1}", True, (200, 200, 200))
        score2 = font.render(f"Player 2 Score: {self.player2.length - 1}", True, (200, 200, 200))

        self.surface.blit(score1, (700, 100))
        self.surface.blit(score2, (700, 50))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render("Game Over!", True, (255, 255, 255))
        self.surface.blit(line1, (400, 300))

        score1 = self.player1.length - 1
        score2 = self.player2.length - 1

        if score1 > score2:
            winner_line = font.render(f"Player 1 Wins!", True, (255, 255, 255))
        elif score1 < score2:
            winner_line = font.render(f"Player 2 Wins!", True, (255, 255, 255))
        else:
            winner_line = font.render("Match Tie!", True, (255, 255, 255))

        self.surface.blit(winner_line, (400, 500))

        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 400))

        pygame.mixer.music.pause()
        pygame.display.flip()

    def show_winner(self, winner):
        self.show_game_over(winner)
        time.sleep(5)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        # Player 1 controls
                        if event.key == K_LEFT:
                            self.player1.move_left()
                        if event.key == K_RIGHT:
                            self.player1.move_right()
                        if event.key == K_UP:
                            self.player1.move_up()
                        if event.key == K_DOWN:
                            self.player1.move_down()

                        # Player 2 controls
                        if event.key == K_a:
                            self.player2.move_left()
                        if event.key == K_d:
                            self.player2.move_right()
                        if event.key == K_w:
                            self.player2.move_up()
                        if event.key == K_s:
                            self.player2.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.6)

if __name__ == '__main__':
    game = MultiplayerGame()
    game.run()
