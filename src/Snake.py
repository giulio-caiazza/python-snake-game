from random import randint

class Snake:
    def __init__(self, setting):
        self.setting = setting
        self.INITIAL_SIZE = self.setting.SNAKE_INITIAL_SIZE if not self.setting.SNAKE_INITIAL_SIZE > (self.setting.SCREEN_WIDTH / self.setting.BLOCK_SIZE)-1 else 3
        self.COLORS = self.random_headAndBody_color()
        self.body = []
        self.direction = "NULL"

        for i in range(-self.INITIAL_SIZE, 0):
            self.body.append((-1 * i * self.setting.BLOCK_SIZE, 3 * self.setting.BLOCK_SIZE))

    def random_headAndBody_color(self):
        color_head = randint(0, len(self.setting.COLORS["snake"])-1)
        continua = True
        while continua:
            color_body = randint(0, len(self.setting.COLORS["snake"])-1)
  
            if color_head != color_body:
                continua = False
        return (self.setting.COLORS["snake"][color_head], self.setting.COLORS["snake"][color_body])

    def setDirection(self, direction = 0):
        #print("QUI", direction.upper() in ("UP", "DOWN", "RIGHT", "LEFT") and ((direction == "UP" and self.direction != "DOWN") or (direction == "DOWN" and self.direction != "UP") or (direction == "LEFT" and self.direction != "RIGHT") or (direction == "RIGHT" and self.direction != "LEFT") or ((direction == "LEFT" and self.direction != "NULL"))))
        if direction == 0:
            direction = self.direction

        direction = direction.upper()
        opposites = {
            "UP" : "DOWN",
            "DOWN" : "UP",
            "LEFT" : "RIGHT",
            "RIGHT" : "LEFT"
        }
        if direction in opposites.keys() and (self.direction != opposites[direction] or self.direction == "NULL"):
            if direction == "LEFT" and self.direction == "NULL":
                direction = "RIGHT"
            self.direction = direction

    def movePoints(self, XOrY, valueOfDirection):
        temoralyPoint_Now = self.body[0]
        temoralyPoint_Before = self.body[0]

        if XOrY == "Y":
            self.body[0] = (self.body[0][0], self.body[0][1] + valueOfDirection)
            if self.body[0][1] < 0:
                self.body[0] = (self.body[0][0], self.setting.SCREEN_HEIGHT - self.setting.BLOCK_SIZE)
            if self.body[0][1] > (self.setting.SCREEN_HEIGHT - self.setting.BLOCK_SIZE):
                self.body[0] = (self.body[0][0], 0)
        if XOrY == "X":
            self.body[0] = (self.body[0][0] + valueOfDirection, self.body[0][1])
            if self.body[0][0] < 0:
                self.body[0] = (self.setting.SCREEN_WIDTH - self.setting.BLOCK_SIZE, self.body[0][1])
            if self.body[0][0] > (self.setting.SCREEN_WIDTH - self.setting.BLOCK_SIZE):
                self.body[0] = (0, self.body[0][1])

        for i in range(1, len(self.body)):
            temoralyPoint_Before = self.body[i]
            self.body[i] = temoralyPoint_Now
            temoralyPoint_Now = temoralyPoint_Before

    def detectCollision(self):
        return self.body[0] in self.body[1:]

    def move(self):
        if self.direction == "UP":
           self.movePoints("Y", self.setting.BLOCK_SIZE * (-1))
        elif self.direction == "DOWN":
            self.movePoints("Y", self.setting.BLOCK_SIZE)
        elif self.direction == "RIGHT":
            self.movePoints("X", self.setting.BLOCK_SIZE)
        elif self.direction == "LEFT":
            self.movePoints("X", self.setting.BLOCK_SIZE * (-1))
            
        return self.detectCollision()

    def grow(self):
        if self.direction == "RIGHT":
            self.body.append((self.body[-1][0] - self.setting.BLOCK_SIZE, self.body[-1][1]))
        elif self.direction == "LEFT":
            self.body.append((self.body[-1][0] + self.setting.BLOCK_SIZE, self.body[-1][1]))
        elif self.direction == "UP":
            self.body.append((self.body[-1][0], self.body[-1][1] - self.setting.BLOCK_SIZE))
        elif self.direction == "DOWN":
            self.body.append((self.body[-1][0], self.body[-1][1] + self.setting.BLOCK_SIZE))

    def getScore(self):
        return len(self.body) - self.INITIAL_SIZE