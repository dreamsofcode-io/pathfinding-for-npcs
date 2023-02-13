from pyglet import image
from pyglet import graphics
import os

def load_npc_animation(sprite, color, weapon, state):
    directory = './assets/sprites/{}/{}/{}/{}'.format(sprite, color, weapon, state)
    files = os.listdir(directory)

    frames = []

    for file in files:
        img = image.load('{}/{}'.format(directory, file))
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        frames.append(image.AnimationFrame(img, duration=0.1))

    animation = image.Animation(frames)

    return animation

def load_tileset(path):
    return image.load(path)
