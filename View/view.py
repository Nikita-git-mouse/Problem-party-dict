from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager


class ScreenManager(ScreenManager):
    def __init__(self):
        pass



Builder.load_file(os.path.join(os.path.dirname(__file__), "view.kv"))