from random import randint

class Food:
    def __init__(self, setting):
        self.setting = setting
        self.position = self.random_position()
        self.STALK_COLOR = self.setting.COLORS["apple_stalk"]
        self.LEAVE_COLOR = self.setting.COLORS["apple_leave"]
        self.body_color = self.random_body_color()



    def random_position(self):
        x = randint(0, self.setting.SCREEN_WIDTH // self.setting.BLOCK_SIZE - 1) * self.setting.BLOCK_SIZE
        y = randint(0, self.setting.SCREEN_HEIGHT // self.setting.BLOCK_SIZE - 1) * self.setting.BLOCK_SIZE
        self.position = (x, y)
        return (x, y)
    
    def random_body_color(self):
        random_number_color = randint(0, len(self.setting.COLORS["apple_body"])-1)
        self.body_color = self.setting.COLORS["apple_body"][random_number_color]
        return self.body_color
