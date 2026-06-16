from pygame.mixer import music as mx_music, get_init as mixer_get_init, init as mx_init
from random import randint
from Settings import Setting
from time import sleep
from threading import Thread

class Music:
    def __init__(self):
        self.path = self.random_music()
        self.stop_flag = False
        self.cont = 0
        mx_init()  # Initialize the mixer
        print("Mixer initialized:", mixer_get_init())

        self.main_thread = Thread(target=self.play_music_loop)

    def play_music_loop(self):
        mx_music.load(self.path)
        mx_music.set_volume(0.09)
        mx_music.play(loops=-1)
        while not self.stop_flag and mx_music.get_busy:
            self.cont += 1
            sleep(1)

    def start(self):
        self.main_thread.start()

    def stop(self):
        self.stop_flag = True
        mx_music.stop()

    def random_music(self):
        setting = Setting()
        path = setting.PATHS["musics"][randint(0, len(setting.PATHS["musics"]) - 1)]
        self.path = path
        return path

    def set_path_music(self, path):
        try:
            self.path = path
            return True
        except Exception as e:
            return False

    def set_volume_music(self, volume):
        mx_music.set_volume(volume)