import pyglet
from game import Game

screenwidth = 2048
screenheight = 1536

window = pyglet.window.Window(screenwidth, screenheight)
game = Game(width=screenwidth, height=screenheight)

@window.event
def on_draw():
    window.clear()
    game.draw()

@window.event
def on_mouse_release(x, y, button, modifiers):
    game.on_mouse_release(x, y, button, modifiers)

pyglet.app.run()
