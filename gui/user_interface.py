import threading
import pygame
import pygetwindow
import win32api
import win32con
import win32gui
from PIL import Image, ImageSequence
from win32api import GetSystemMetrics

NAME: str = "Dream"
TRANSFLAG = win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW


class GIF():
    def __init__(self, frames: [pygame.surface.Surface]):
        self.frames = frames
        self.cursor = 0
        self.len = len(frames)

    def __len__(self):
        return self.len

    @staticmethod
    def pilImageToSurface(pilImage):
        mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
        return pygame.image.fromstring(data, size, mode).convert_alpha()

    @staticmethod
    def loadGIF(filename):
        pilImage = Image.open(filename)
        frames = []
        if pilImage.format == 'GIF' and pilImage.is_animated:
            for frame in ImageSequence.Iterator(pilImage):
                pygameImage = __class__.pilImageToSurface(frame.convert('RGBA'))
                frames.append(pygameImage)
        else:
            frames.append(filename.pilImageToSurface(pilImage))
        return GIF(frames)

    def next(self):
        out = self.frames[self.cursor]
        self.cursor = self.cursor + 1 if self.cursor + 1 < self.len else 0
        return out


def set_colorless(name: str):
    hwnd = win32gui.FindWindow(None, name)

    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, TRANSFLAG)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, win32con.WS_POPUP)

    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 255, 254), 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowPos(hwnd,
                          -1,
                          int((GetSystemMetrics(0) / 2)-48),
                          0,
                          96,
                          96,
                          win32con.SWP_SHOWWINDOW)


class Interface(threading.Thread):

    pygame.init()
    wnd = pygame.display.set_mode((1, 1))
    pygame.display.set_caption(NAME)
    set_colorless(NAME)
    CAT: GIF = GIF.loadGIF("gui/Dream.gif")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        wnd.fill((255, 255, 254))
        wnd.blit(CAT.next(), (0, 0))
        pygame.display.flip()

        pygame.time.delay(100)
