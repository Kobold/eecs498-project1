from javax.swing import JFrame
from processing.core import PApplet

class HelloProcessing(PApplet):

    def setup(self):
        global p
        p = self
        p.size(350, 350)
    
    def draw(self):
        p.fill(p.random(255))
        p.rect(150, 150, 50, 50)

if __name__ == '__main__':
    frame = JFrame(title="Processing",
                   resizable=0,
                   defaultCloseOperation=JFrame.EXIT_ON_CLOSE)
    panel = HelloProcessing()
    frame.add(panel)
    panel.init()
    while panel.defaultSize and not panel.finished:
        pass
    frame.pack()
    frame.visible = 1