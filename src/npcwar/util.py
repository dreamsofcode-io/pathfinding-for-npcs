from pyglet import image
from pyglet import graphics
from pyglet import math as pmath
import math
import os

def load_npc_animation(sprite, color, weapon, state, duration=0.1):
    directory = './assets/sprites/{}/{}/{}/{}'.format(sprite, color, weapon, state)
    files = os.listdir(directory)

    frames = []

    for file in files:
        img = image.load('{}/{}'.format(directory, file))
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        frames.append(image.AnimationFrame(img, duration=duration))

    animation = image.Animation(frames)

    return animation

def load_tileset(path):
    return image.load(path)

def calculate_distance(pos1: pmath.Vec2, pos2: pmath.Vec2):
    a = (pos1.x - pos2.x)
    b = (pos1.y - pos2.y)
    return math.sqrt(a**2 + b**2)
