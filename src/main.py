import pyglet
from npcwar.game import Game

scale = 1
screenwidth = 1024 * scale
screenheight = 768 * scale
show_graph = False

window = pyglet.window.Window(screenwidth, screenheight, resizable=False)
game = Game(width=screenwidth, height=screenheight, scale=scale, show_graph=show_graph)
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
