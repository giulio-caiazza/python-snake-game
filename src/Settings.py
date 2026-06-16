class Setting:
    def __init__(self):
        # IMPOSTAZIOMI DIMENSIONE FINESTRA
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600
        self.BLOCK_SIZE = 20
        # IMPOSTAZIONI AGGIORNAMENTO DELLO SCHERMO
        self.FPS = 15

        # IMPOSTAZIONI DI GIOCO
        self.SNAKE_INITIAL_SIZE = 12
        self.NUMBER_OF_APPLES = 1

        # IMPOSTAZIONI DI GESTIONE DI SISTEMA
        self.COLORS = {
            "background" : (0, 0, 0),
            # 4 elements snake = [fuchsia, bright green, blue violet, dodger blue]
            "snake" : [(255,0,255), (102, 255, 0), (138, 43, 226), (30, 144, 255)],
            "apple_stalk" : (88, 57, 39),
            "apple_leave" : (34, 139, 34),
            # 10 elements apple_body = [yellow, forest green, green yellow, cream, tangelo, bittersweet, crimson, red violet, red, dark red]
            "apple_body" : [(255, 255, 0), (34, 139, 34), (173, 255, 47), (250, 250, 210), (255, 69, 0), (255, 111, 97), (220, 20, 60), (199, 21, 133), (255, 0, 0), (139, 0, 0)],
            "score" : (255, 255, 255),
            "game_over" : (230, 230, 230)
        }
        self.PATHS = {
            "musics" : ("./audio/epic-cinematic-351310.mp3", "./audio/Walen - Play (freetouse.com).mp3")
        }
