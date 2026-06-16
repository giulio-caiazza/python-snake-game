from threading import Thread
from pygame import init, Rect, quit
from pygame import event as pg_event, QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_w, K_UP, K_i, K_s, K_DOWN, K_k, K_a, K_LEFT, K_j, K_d, K_RIGHT, K_l, K_ESCAPE, K_RETURN, K_SPACE
from pygame.font import Font
from pygame.draw import circle, rect, line
from pygame.display import set_mode, flip
from pygame.mouse import get_pos
from pygame.time import Clock
from time import time
from Settings import Setting
from Snake import Snake
from Food import Food
from Music import Music

class Game:
    def __init__(self, path_score_record):
        self.path_score_record = path_score_record
        self.reset_game()

    def reset_game(self):
        # Reset of all game variables to start a new game
        self.time_start = time()
        self.score_record = self.readScoreRecord()
        self.setting = Setting()
        self.snake = Snake(self.setting)
        self.foods = [Food(self.setting) for _ in range(self.setting.NUMBER_OF_APPLES)]

        self.snake.direction = "NULL"
        self.gameStatus = True
        self.do_one_execution = True

        self.KEY_DIRECTION_MAP = {
            K_w: "UP", K_UP: "UP", K_i: "UP",
            K_s: "DOWN", K_DOWN: "DOWN", K_k: "DOWN",
            K_a: "LEFT", K_LEFT: "LEFT", K_j: "LEFT",
            K_d: "RIGHT", K_RIGHT: "RIGHT", K_l: "RIGHT"
        }

        self.button_rect = Rect(self.setting.SCREEN_WIDTH // 2 - 200, self.setting.SCREEN_HEIGHT // 2 - 35, 400, 70)

    def handle_events(self, music):
        for event in pg_event.get():
            if event.type == QUIT:
                music.stop()
                return False
            if event.type == KEYDOWN:
                if self.gameStatus:
                    # Change direction of the snake with W/A/S/D, Arrow Keys or I/J/K/L
                    if event.key in self.KEY_DIRECTION_MAP:
                        self.snake.setDirection(self.KEY_DIRECTION_MAP[event.key])
                    if event.key == K_ESCAPE:
                        self.gameStatus = False
                else:
                    # Restart con Space o Enter
                    if event.key in [K_RETURN, K_SPACE]:
                        self.reset_game()
                        return True
            elif event.type == MOUSEBUTTONDOWN and not self.gameStatus:
                if self.button_rect.collidepoint(*get_pos()):
                    self.reset_game()
                    return True
        return True

    def update(self):
        # Move the snake and check for collisions
        if self.snake.move():
            self.gameStatus = False
            return

        # Check if the snake has eaten any food
        for food in self.foods:
            if self.snake.body[0] == food.position:
                self.snake.grow()
                food.random_position()
                food.random_body_color()

    def draw(self):
        self.screen.fill(self.setting.COLORS["background"])

        # Snake
        head = self.snake.body[0]
        BLOCK_SIZE = self.setting.BLOCK_SIZE
        rect(self.screen, self.snake.COLORS[0], Rect(head[0], head[1], BLOCK_SIZE, BLOCK_SIZE))
        for x, y in self.snake.body[1:]:
            rect(self.screen, self.snake.COLORS[1], Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))

        # Apple
        for food in self.foods:
            pos_x, pos_y = food.position
            cx = pos_x + BLOCK_SIZE / 2 # Center x of the apple
            cy = pos_y + BLOCK_SIZE / 2 # Center y of the apple
            
            # Draw the apple as a circle with a stalk and a leaf
            RADIUS = 8
            APPLE_STALK_WIDTH = BLOCK_SIZE * 0.15
            APPLE_STALK_HEIGHT = BLOCK_SIZE * 0.25
            circle(self.screen, food.body_color, (cx, cy + 2), RADIUS)
            rect(self.screen, food.STALK_COLOR, (cx - APPLE_STALK_WIDTH / 2, pos_y, APPLE_STALK_WIDTH, APPLE_STALK_HEIGHT))
            line(self.screen, food.LEAVE_COLOR, (cx + APPLE_STALK_WIDTH / 2, pos_y + APPLE_STALK_HEIGHT), (pos_x + BLOCK_SIZE, pos_y), 2)

        # Timer
        timer_text = self.font.render(f"Timer: {int(time() - self.time_start)} s", True, self.setting.COLORS["score"])
        text_rect = timer_text.get_rect(topleft=(7, 10))
        self.screen.blit(timer_text, text_rect)

        # Score
        record_text = self.font.render(f"Record: {self.score_record}", False, self.setting.COLORS["score"])
        text_rect_record = record_text.get_rect(topright=(self.setting.SCREEN_WIDTH - 15, 10))
        self.screen.blit(record_text, text_rect_record)

        score_text = self.font.render(f"Score: {self.snake.getScore()}", True, self.setting.COLORS["score"])
        text_rect = score_text.get_rect(topright=(self.setting.SCREEN_WIDTH - 15, 30))
        self.screen.blit(score_text, text_rect)

    def end_button(self):
        font = Font(None, 70)
        text_surface = font.render("GAME OVER", True, self.setting.COLORS["game_over"])
        text_rect = text_surface.get_rect(center=self.button_rect.center)

        rect(self.screen, (255, 0, 0), self.button_rect, border_radius=15)
        self.screen.blit(text_surface, text_rect)

    def writeScoreRecord(self, value):
        try:
            with open(self.path_score_record, 'w', encoding='utf-8') as f:
                f.write(str(value))
        except:
            pass

    def readScoreRecord(self):
        try:
            with open(self.path_score_record, encoding='utf-8') as f:
                return int(f.read().strip())
        except:
            return 0

    def run(self):
        init()
        
        self.font = Font(None, 30)
        self.screen = set_mode((self.setting.SCREEN_WIDTH, self.setting.SCREEN_HEIGHT))
        self.clock = Clock()

        music = Music()
        music.start()

        running = True
        while running:
            running = self.handle_events(music)

            if self.gameStatus:
                self.update()
                self.draw()
                self.clock.tick(self.setting.FPS)
            else:
                if self.do_one_execution:
                    if self.score_record < self.snake.getScore():
                        Thread(target=self.writeScoreRecord, args=(self.snake.getScore(),)).start()
                    self.snake.setDirection("NULL")
                    self.end_button()
                    self.do_one_execution = False

            # refresh the display
            flip()

        quit()