import pyglet
from npcwar.game import Game

scale = 4
screenwidth = 1024 * 2
screenheight = 768 * 2

window = pyglet.window.Window(screenwidth, screenheight, resizable=False)
game = Game(width=screenwidth, height=screenheight, scale=scale)
fps_display = pyglet.window.FPSDisplay(window=window)

@window.event
def on_draw():
    window.clear()
    game.draw()
    fps_display.draw()

@window.event
def on_mouse_release(x, y, button, modifiers):
    game.on_mouse_release(x, y, button, modifiers)


pyglet.app.run()
