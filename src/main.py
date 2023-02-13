import pyglet
from npcwar.game import Game

scale = 1
screenwidth = 1024
screenheight = 768

window = pyglet.window.Window(screenwidth * scale, screenheight * scale, resizable=False)
game = Game(width=screenwidth, height=screenheight, scale=scale)

@window.event
def on_draw():
    window.clear()
    game.draw()

@window.event
def on_mouse_release(x, y, button, modifiers):
    game.on_mouse_release(x, y, button, modifiers)

pyglet.app.run()
